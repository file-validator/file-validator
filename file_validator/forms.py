"""
this file provides forms for django
"""
from django import forms

from file_validator.widgets import FileInputWidget


class ValidatedFileField(forms.FileField):
    """
    validated file filed for django
    """
    widget = FileInputWidget

    def __init__(self, *, accept=None, custom_css_class=None, **kwargs):
        self.accept = accept
        self.custom_css_class = custom_css_class
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        attrs = {}

        if self.accept:
            attrs['accept'] = self.accept

        if self.custom_css_class:
            attrs['class'] = self.custom_css_class

        return attrs
