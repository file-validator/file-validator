from django.shortcuts import render

from tests.project.app.forms import TestFormWithAcceptAttribute


def test_form_with_accept_attribute_view(request):
    form = TestFormWithAcceptAttribute()
    context = {
        "form": form,
    }
    return render(
        request,
        context=context,
        template_name="app/form_with_accept_attribute.html",
    )
