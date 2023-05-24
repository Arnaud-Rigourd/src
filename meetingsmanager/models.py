from django.db import models


class Meetings(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('declined', 'Annulé'),
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='pending',
    )
    message = models.TextField(blank=False)
    company = models.ForeignKey('profilemanager.Company', on_delete=models.CASCADE)
    dev = models.ForeignKey('profilemanager.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"Meeting between : {self.company.user.username} - {self.dev.user.username}"
