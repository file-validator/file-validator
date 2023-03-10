from django.contrib import admin

from tests.project.app.models import TestModelWithValidatedFileField

admin.site.register(TestModelWithValidatedFileField)
