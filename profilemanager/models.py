from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

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
    visible = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Stacks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)
    used_stacks = models.TextField(blank=True) # changer en CharField
    link = models.URLField(blank=True, default="")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

