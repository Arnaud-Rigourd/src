from django.urls import path

from profilemanager.views import index

app_name = "profilemanager"

urlpatterns = [
    path('profilemanager/index/', index, name="home"),
]
