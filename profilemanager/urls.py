from django.urls import path

from profilemanager.views import ProfileDetail

app_name = "profilemanager"

urlpatterns = [
    path('profile/<str:username>', ProfileDetail.as_view(), name="home"),
]
