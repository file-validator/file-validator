====================
Safe Mode
====================
By using Safe Mode, you can perform validation
operations using all three libraries at the same time
To use, first import as in the example below:

.. code-block:: console

    from file_validator.validator import file_validator

Then just call the file_validator function:

.. code-block:: python

    from file_validator.validator import file_validator

    file_validator(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')

.. autofunction:: file_validator.validator.file_validator

Django
--------------
To validate files in Django using Safe Mode we use the ``FileValidator`` class
In order to be able to use the validator written in `Django <https://www.djangoproject.com/>`_ using the
safe mode library, you must do the following:


1 .First, **import** the ``FileValidator`` to your Django model as follows:

.. code-block:: python

    from file_validator.django import FileValidator


2. Now add the ``FileValidator`` to your model validator like the
example below and give it the ``mimes`` you want the
file to be validated based on:

.. code-block:: python

    from django.db import models
    from file_validator.django import FileValidator


    class File(models.Model):
        file = models.FileField(validators=[FileValidator(mimes=['audio/mpeg', 'video/mp4'],python_magic=True ,file_size=1048576)])


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



.. autoclass:: file_validator.django.FileValidator
    :members: __init__, __call__
