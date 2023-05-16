from django.db import models

class FAQClient(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


class FAQDev(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
