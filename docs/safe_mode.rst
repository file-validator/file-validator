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

    file_validator('image/png', 'image/jpeg', file_path='/path/to/file')

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
        file = models.FileField(validators=[FileValidator("image/png", "video/mp4")])

3. After this step, do a new migration to apply the changes

.. code-block:: console

        python manage.py makemigrations
        python manage.py migrate



.. autoclass:: file_validator.django.FileValidator
    :members: __init__, __call__
