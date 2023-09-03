from django.db import models

class Client(models.Model):
    Firstname = models.CharField(max_length=200)
    Lastname = models.CharField(max_length=200)
    Email = models.CharField(max_length=200, unique=True)
    Password = models.CharField(max_length=200)
    objects = models.Manager


class EmailModel(models.Model):
    Email = models.EmailField(max_length=50, unique=True)
    Otp = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager
