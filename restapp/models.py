from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserRegistration(AbstractUser):
    age = models.PositiveIntegerField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
