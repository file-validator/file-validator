====================
FileType Library
====================
filetype a Python package to infer file type and MIME type checking the magic numbers signature of a file or buffer.
we also support the `filetype <https://github.com/h2non/filetype.py>`_ library, and you can import it to your project as follows:

.. code-block:: python

    from file_validator.validator import file_validator_by_filetype

To use this function, just call the function like the previous example and give it the path of the file and the mimes you want the file to be validated based on.

**Example** : 👇


.. code-block:: python

    from file_validator.validator import file_validator_by_filetype

    file_validator_by_filetype('audio/mpeg', 'video/mp4', file_path='/path/to/file')


.. autofunction:: file_validator.validator.file_validator_by_filetype


.. note::
    To see what types the filetype library supports,
    you can refer to the `link <https://github.com/h2non/filetype.py#supported-types>`_ below

Django
--------------
In order to be able to use the file validator that uses the filetype library to validate files
in `Django <https://www.djangoproject.com/>`_, you must do the following:

1 .First, **import** the ``FileValidatorByFileType`` to your Django model as follows:

.. code-block:: python

    from file_validator.django import FileValidatorByFileType



2. Now add the ``FileValidatorByFileType`` to your model validator like the
example below and give it the ``mimes`` you want the
file to be validated based on:

.. code-block:: python

    from django.db import models
    from file_validator.django import FileValidatorByFileType


    class File(models.Model):
        file = models.FileField(validators=[FileValidatorByFileType("image/png", "video/mp4")])

3. After this step, do a new migration to apply the changes

.. code-block:: console

        python manage.py makemigrations
        python manage.py migrate



.. autoclass:: file_validator.django.FileValidatorByFileType
    :members: __init__, __call__
