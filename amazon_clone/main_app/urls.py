from django.urls import path
from .views import RegisterView, LoginOTPView, AdvertisementCreateView, AdminAdvertisementApproveView, Last10AdvertisementsView, ProfileUpdateView, ProductDetailView
from .views import index
from .views import home, sign_up, sign_in, my_profile, sign_out
urlpatterns = [
    path('', home, name='home'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('my_profile/', my_profile, name='my_profile'),
    path('sign_out/', sign_out, name='sign_out'),
]
