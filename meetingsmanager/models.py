from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.models import CustomUser


class Meetings(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('declined', 'Annulé'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    title = models.CharField(max_length=100, default="Vous avez une nouvelle demande de rendez-vous")
    meeting_date = models.DateTimeField(default=timezone.now)
    # message = models.TextField()
    # message = models.OneToMany(Messages, on_delete=models.CASCADE)
    company = models.ForeignKey('profilemanager.Company', on_delete=models.CASCADE)
    dev = models.ForeignKey('profilemanager.Profile', on_delete=models.CASCADE)


    def __str__(self):
        return f"Meeting between : {self.company.user.username} - {self.dev.user.username}"


class Messages(models.Model):
    content = models.TextField()
    meeting = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')

    # def __str__(self):
        # return f"Message between {self.meeting.company.user.username} and {self.meeting.dev.user.username}"
        # pass
