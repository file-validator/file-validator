from django import forms

from file_validator.forms import ValidatedFileField
from tests.project.app.models import ModelWithValidatedFileField


class FileModelForm(forms.ModelForm):
    class Meta:
        model = ModelWithValidatedFileField
        fields = ["test_file"]


class FormWithAcceptAttribute(forms.Form):
    test_file = ValidatedFileField(
        accept="image/*",
    )


class FormWithoutAcceptAttribute(forms.Form):
    test_file = ValidatedFileField()


class FormWithCssClassAttribute(forms.Form):
    test_file = ValidatedFileField(
        custom_css_class="test-class",
    )


class FormWithValidatedFileField(forms.Form):
    test_file = ValidatedFileField(
        accept="image/*",
        # => accept attribute
        custom_css_class="your-custom-css-class",
        # => custom css class
        multiple=True,
    )
