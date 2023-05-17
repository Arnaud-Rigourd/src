from django.contrib import admin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'password',
        'username',
        'first_name',
        'last_name',
        'category',
        'company_name',
        'is_active',
        'last_name',
        'is_staff',
    )

    list_per_page = 10
