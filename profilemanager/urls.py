from django.urls import path

from profilemanager.views import ProfileDetail, ProfileCreate, StackCreate, ProjectCreate, StackDelete, ProjectDelete, \
    StackUpdate, ProfileIndex, ProfileUpdate, ProjectUpdate

app_name = "profilemanager"

urlpatterns = [
    path('all/', ProfileIndex.as_view(), name="index"),
    path('profile/<slug:slug>/', ProfileDetail.as_view(), name="detail"),
    path('profile/create/<str:username>/', ProfileCreate.as_view(), name="create"),
    path('profile/update/<slug:slug>/', ProfileUpdate.as_view(), name="update"),
    path('profile/stack/create/', StackCreate.as_view(), name="stack-create"),
    path('profile/stack/delete/<slug:slug>/<int:pk>/', StackDelete.as_view(), name="stack-delete"),
    path('profile/stack/update/<slug:slug>/<int:pk>/', StackUpdate.as_view(), name="stack-update"),
    path('profile/project/create/', ProjectCreate.as_view(), name="project-create"),
    path('profile/project/update/<slug:slug>/<int:pk>/', ProjectUpdate.as_view(), name="project-update"),
    path('profile/project/delete/<slug:slug>/<int:pk>/', ProjectDelete.as_view(), name="project-delete"),
]
