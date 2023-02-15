from django import forms

from file_validator.forms import ValidatedFileField
from tests.project.app.models import TestFileModel


class TestFileModelForm(forms.ModelForm):
    class Meta:
        model = TestFileModel
        fields = ['test_file']


class TestFormWithAcceptAttribute(forms.Form):
    test_file = ValidatedFileField(
        accept='image/*'
    )


class TestFormWithoutAcceptAttribute(forms.Form):
    test_file = ValidatedFileField()


class TestFormWithCssClassAttribute(forms.Form):
    test_file = ValidatedFileField(
        custom_css_class='test-class'
    )
