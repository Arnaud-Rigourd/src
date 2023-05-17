from django.urls import path

from profilemanager.views import ProfileDetail, ProfileCreate, StackCreate, ProjectCreate, StackDelete

app_name = "profilemanager"

urlpatterns = [
    path('profile/<str:username>', ProfileDetail.as_view(), name="detail"),
    path('profile/create/<str:username>', ProfileCreate.as_view(), name="create"),
    path('profile/create-stack/', StackCreate.as_view(), name="stack-create"),
    path('profile/delete-stack/<int:pk>', StackDelete.as_view(), name="stack-delete"),
    path('profile/create-project/', ProjectCreate.as_view(), name="project-create"),
]
