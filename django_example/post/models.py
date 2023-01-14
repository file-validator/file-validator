from django.db import models
from file_validator.file_validator.models import ValidatedFileField


class File(models.Model):
    file = ValidatedFileField(acceptable_mimes=["image/png", "audio/mpeg"], max_upload_file_size=10485760)
    name = models.TextField()
    reza = models.CharField(max_length=1212)

