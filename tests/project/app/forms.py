from django import forms

from file_validator.forms import ValidatedFileField
from tests.project.app.models import FileModel


class TestFileModelForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ["test_file"]


class TestFormWithAcceptAttribute(forms.Form):
    test_file = ValidatedFileField(
        accept="image/*",
    )


class TestFormWithoutAcceptAttribute(forms.Form):
    test_file = ValidatedFileField()


class TestFormWithCssClassAttribute(forms.Form):
    test_file = ValidatedFileField(
        custom_css_class="test-class",
    )


class TestForm(forms.Form):
    test_file = ValidatedFileField(
        accept="image/*",
        # => accept attribute
        custom_css_class="your-custom-css-class",
        # => custom css class
        multiple=True,
    )
