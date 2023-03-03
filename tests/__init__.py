"""Unit test package for file_validator."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.project.project.settings")

django.setup()
