from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


class PasswordEntry(models.Model):
    def __str__(self):
        return f'{self.service} | {self.login}'

    service = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
