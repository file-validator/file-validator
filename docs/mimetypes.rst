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
        file = models.FileField(validators=[FileValidatorByMimeTypes(mimes=['audio/mpeg', 'video/mp4'],file_size=1048576)])


.. note::
    To choose the size you want the files to be validated based
    on, you can take help from the table below or enter your
    desired size in bytes:

    ==========  ========================================
    Size        Bytes
    ==========  ========================================
    1 MB        1048576 B - 1024**2 B - 2**20 B
    2.5 MB      2621440 B
    5 MB        5242880 B
    10 MB       10485760 B
    20 MB       20971520 B
    50 MB       52428800 B
    100 MB      104857600 B
    250 MB      262144000 B
    500 MB      524288000 B
    1 GB        1073741824 B
    2 GB        2147483648 B
    ==========  ========================================


3. After this step, do a new migration to apply the changes

.. code-block:: console

        python manage.py makemigrations
        python manage.py migrate



.. autoclass:: file_validator.django.FileValidatorByMimeTypes
    :members: __init__, __call__
