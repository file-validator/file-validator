from django.urls import path

from tests.project.app.views import test_form_with_accept_attribute_view

urlpatterns = [
    path('/form/accept/attribute', test_form_with_accept_attribute_view, name='index')
]
