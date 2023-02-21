"""
widget for django
"""

from django.forms import ClearableFileInput


class FileInputWidget(ClearableFileInput):
    """
    file input widget
    """

    template_name = "file_validator/file_input_widget.html"
