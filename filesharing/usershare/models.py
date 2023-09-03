from django.db import models


class OpsUser(models.Model):
    Firstname = models.CharField(max_length=200)
    Lastname = models.CharField(max_length=200)
    Email = models.CharField(max_length=200, unique=True)
    Password = models.CharField(max_length=200)
    objects = models.Manager

class UploadedFile(models.Model):
    user = models.ForeignKey(OpsUser, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False)
    file_content = models.BinaryField()
    objects = models.Manager

