from django.db import models
from file_validator.file_validator.django import FileValidator


class ValidFile(models.Model):
    file = models.FileField(validators=[FileValidator(mimes=["image/jpeg", "video/mp4"])])

    class Meta:
        app_label = 'post'


class BadFile(models.Model):
    file = models.FileField(validators=[FileValidator(mimes=["bad/mime"])])

    class Meta:
        app_label = 'post'
