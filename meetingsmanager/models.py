

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


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
    title = models.CharField(max_length=100, default="Demande de rendez-vous")
    meeting_date = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    company = models.ForeignKey('profilemanager.Company', on_delete=models.CASCADE)
    dev = models.ForeignKey('profilemanager.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"Meeting between : {self.company.user.username} - {self.dev.user.username}"

    # def clean(self):
    #     existing_meeting = Meetings.objects.filter(
    #         Q(dev=self.dev, meeting_date=self.meeting_date) |
    #         Q(company=self.company, dev=self.dev, meeting_date=self.meeting_date)
    #     ).exclude(pk=self.pk)
    #
    #     if existing_meeting.exists():
    #         raise ValidationError('A meeting with the same developer at the same time already exists.')

    def save(self, *args, **kwargs):
        # self.full_clean()
        return super().save(*args, **kwargs)
