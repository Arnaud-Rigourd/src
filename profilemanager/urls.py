from django.urls import path

from profilemanager.views import ProfileDetail, ProfileCreate, StackCreate, ProjectCreate, StackDelete, ProjectDelete, \
    StackUpdate, ProfileIndex, ProfileUpdate

app_name = "profilemanager"

urlpatterns = [
    path('all/', ProfileIndex.as_view(), name="index"),
    path('profile/<str:username>', ProfileDetail.as_view(), name="detail"),
    path('profile/create/<str:username>', ProfileCreate.as_view(), name="create"),
    path('profile/update/<slug:slug>', ProfileUpdate.as_view(), name="update"),
    path('profile/create-stack/', StackCreate.as_view(), name="stack-create"),
    path('profile/delete-stack/<int:pk>', StackDelete.as_view(), name="stack-delete"),
    path('profile/update-stack/<int:pk>', StackUpdate.as_view(), name="stack-update"),
    path('profile/create-project/', ProjectCreate.as_view(), name="project-create"),
    path('profile/delete-project/<int:pk>', ProjectDelete.as_view(), name="project-delete"),
]
