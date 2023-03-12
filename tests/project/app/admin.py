from django.contrib import admin

from tests.project.app.models import ModelWithValidatedFileField

admin.site.register(ModelWithValidatedFileField)
