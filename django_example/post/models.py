from django.db import models
from file_validator.django import FileValidatorByMimeTypes, FileValidatorByFileType


class Post(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    file = models.FileField(validators=[FileValidatorByFileType("image/png", "video/mp4")])
