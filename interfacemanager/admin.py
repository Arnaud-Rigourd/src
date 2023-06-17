from django.contrib import admin
from interfacemanager.models import FAQClient, FAQDev


@admin.register(FAQClient)
class FAQClientAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
        'position',
    )

    list_per_page = 10


@admin.register(FAQDev)
class FAQDevAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
        'position',
    )

    list_per_page = 10
