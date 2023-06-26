from django.urls import path

from meetingsmanager.views import MeetingsCreate, MeetingsIndex, MeetingsUpdate, MeetingsDelete, MessagesCreate

app_name = 'meetingsmanager'

urlpatterns = [
    path('meetings/create/<int:company_pk>/<int:dev_pk>/', MeetingsCreate.as_view(), name="create"),
    path('meetings/my_meetings/<int:company_pk>/', MeetingsIndex.as_view(), name="index"),
    path('meetings/my_meetings/update/<int:meeting_pk>/', MeetingsUpdate.as_view(), name="update"),
    path('meetings/my_meetings/delete/<int:meeting_pk>/', MeetingsDelete.as_view(), name="delete"),
    path('meetings/my_meetings/messages/create/<int:meeting_pk>/', MessagesCreate.as_view(), name="message-create"),
]
