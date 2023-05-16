from django.urls import path

from interfacemanager.views import FAQHome

app_name = 'interfacemanager'

urlpatterns = [
    path('', FAQHome.as_view(), name="home"),
]