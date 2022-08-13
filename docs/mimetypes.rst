====================
MimeTypes Library
====================

The good news is that we also support the native Python library, `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_, and you can add it to your project as follows:

.. code-block:: console

    $ from file_validator.validator import file_validator_by_mimetypes

For the mimetypes library, you must do exactly as above:


**Example** : 👇


.. code-block:: python

    from file_validator.validator import file_validator_by_mimetypes

    file_validator_by_mimetypes('audio/mpeg', 'video/mp4', file_path='/path/to/file')


.. autofunction:: file_validator.validator.file_validator_by_mimetypes

Django
--------------
To validate files in Django using `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_ module we use the ``FileValidatorByMimeTypes`` class
In order to be able to use the validator written in `Django <https://www.djangoproject.com/>`_ using the
`MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_ library, you must do the following:

1 .First, **import** the ``FileValidatorByMimeTypes`` to your Django model as follows:

.. code-block:: python

    from file_validator.django import FileValidatorByMimeTypes


2. Now add the ``FileValidatorByMimeTypes`` to your model validator like the
example below and give it the ``mimes`` you want the
file to be validated based on:

.. code-block:: python

    from django.db import models
    from file_validator.django import FileValidatorByMimeTypes


    class File(models.Model):
        file = models.FileField(validators=[FileValidatorByMimeTypes("image/png", "video/mp4")])

3. After this step, do a new migration to apply the changes

.. code-block:: console

        python manage.py makemigrations
        python manage.py migrate



.. autoclass:: file_validator.django.FileValidatorByMimeTypes
    :members: __init__, __call__
