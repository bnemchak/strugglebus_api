
from django.db import models
from django.db.models.deletion import CASCADE


class Tasks(models.Model):
    name = models.CharField(max_length=75)
    completed = models.BooleanField()

    def __str__(self):
        return self.name
