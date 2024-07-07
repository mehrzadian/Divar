# main_app/admin.py

from django.contrib import admin
from .models import User, Profile, Product, Advertisement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'date_posted')
    search_fields = ('title', 'description')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email')
    search_fields = ('username', 'phone_number', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'is_approved', 'date_created')
    list_filter = ('is_approved', 'date_created')
    search_fields = ('product__title', 'user__username')
