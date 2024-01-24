from django.contrib import admin
from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone", "user_id", "is_active")
    list_filter = ("is_active",)
    search_fields = ("username", "phone", "user_id")
    list_editable = ("is_active",)
    list_display_links = ("id", "username")
