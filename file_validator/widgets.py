"""
widget for django
"""

from django.forms import ClearableFileInput


class FileInputWidget(ClearableFileInput):
    """
    file input widget
    """
    template_name = ""
