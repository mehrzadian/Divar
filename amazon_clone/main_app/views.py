# main_app/views.py

from rest_framework import generics, status
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from rest_framework.response import Response
from django_otp.oath import TOTP
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SignInForm, ProfileForm
from django_otp.util import random_hex
from .models import User, Profile, Product, Advertisement
from .serializers import UserSerializer, ProfileSerializer, ProductSerializer, AdvertisementSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_otp.oath import TOTP
from django_otp.util import random_hex
from rest_framework.views import APIView
from twilio.rest import Client
from django.conf import settings

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.create(user=user)

class LoginOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Generate OTP
        totp = TOTP(key=random_hex().encode(), step=300)
        otp = totp.token()

        # Send OTP via Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP code is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # Store OTP in user session (or a more secure method)
        request.session['otp'] = otp
        return JsonResponse({"message": "OTP sent successfully"})

    def put(self, request):
        phone_number = request.data.get("phone_number")
        input_otp = request.data.get("otp")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Verify OTP
        stored_otp = request.session.get('otp')
        if input_otp == stored_otp:
            return JsonResponse({"message": "OTP verified successfully"})
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)

class AdvertisementCreateView(generics.CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdminAdvertisementApproveView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        advertisement = self.get_object()
        advertisement.is_approved = request.data.get("is_approved", advertisement.is_approved)
        advertisement.save()
        return Response(AdvertisementSerializer(advertisement).data)

class Last10AdvertisementsView(generics.ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(is_approved=True).order_by('-date_created')[:10]

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def index(request):
    return render(request, 'main_app/index.html')

def verify_otp(request):
    otp = request.GET.get("otp")
    if otp == request.session.get("otp"):
        return HttpResponse("OTP verified")
    return HttpResponse("OTP verification failed")

def generate_otp(request):
    totp = TOTP(random_hex(), step=300)
    otp = totp.token()
    request.session["otp"] = otp
    return HttpResponse("OTP generated")

def base(request):
    return render(request, 'main_app/base.html')

def register(request):
    return render(request, 'main_app/register.html')

def login(request):
    return render(request, 'main_app/login.html')

def base_site(request):
    return render(request, 'main_app/base_site.html')


def home(request):
    return render(request, 'main_app/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main_app/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        username_or_phone = request.POST.get('username')
        try:
            # Check if the user exists
            User.objects.get(username=username_or_phone)  # Assuming username or phone_number is used as username
        except User.DoesNotExist:
            return redirect('sign_up')
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'main_app/sign_in.html', {'form': form})

@login_required
def my_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'main_app/my_profile.html', {'form': form})

def sign_out(request):
    auth_logout(request)
    return redirect('home')