from django.urls import path

from profilemanager.views import ProfileDetail, ProfileCreate

app_name = "profilemanager"

urlpatterns = [
    path('profile/<str:username>', ProfileDetail.as_view(), name="detail"),
    path('profile/create/<str:username>', ProfileCreate.as_view(), name="create"),
]
