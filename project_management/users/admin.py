from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Custom admin panel for managing users."""
    
    model = CustomUser
    list_display = ("id", "username", "email", "is_staff", "is_verified") 
    search_fields = ("username", "email") 
    list_filter = ("is_staff", "is_verified", "is_superuser") 
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Verification", {"fields": ("is_verified", "verification_code")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_verified"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
