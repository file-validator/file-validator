"""
this file provides forms for django
"""
from django import forms

from file_validator.widgets import FileInputWidget


class ValidatedFileFiled(forms.FileField):
    """
    validated file filed for django
    """
    widget = FileInputWidget

    def __init__(self, *, accept=None, **kwargs):
        self.accept = accept

        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        if self.accept:
            return {'accept': self.accept}
        return {}
