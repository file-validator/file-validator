from django import forms

from tests.project.app.models import TestFileModel


class TestFileModelForm(forms.ModelForm):
    class Meta:
        model = TestFileModel
        fields = ['test_file']
