from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class Profile(models.Model):
    JOBS_CHOICES = (
        ('front-end', 'Front-end'),
        ('back-end', 'Back-end'),
        ('full-stack', 'Full-stack'),
    )

    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    job = models.CharField(
        max_length=250,
        choices=JOBS_CHOICES,
        blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
