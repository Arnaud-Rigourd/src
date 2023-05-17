from django.contrib import admin

from profilemanager.models import Profile, Stacks, Projects


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'job',
        'description',
    )
    list_filter = ('job',)

@admin.register(Stacks)
class StacksAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'profile',
    )
    list_filter = ('profile',)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'used_stacks',
        'link',
        'profile',
    )
    list_filter = ('profile',)


