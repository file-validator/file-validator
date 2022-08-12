====================
Python Magic Library
====================
python-magic is a Python interface to the libmagic file type identification
library. libmagic identifies file types by checking their headers according
to a predefined list of file types. This functionality is exposed to the
command line by the Unix command file.
If you want to use File Validators made using the `python-magic <https://github.com/ahupp/python-magic>`_ library, you should add it to your program as follows:

.. code-block:: python

    from file_validator.validator import file_validator_by_python_magic

Just call this function and give the function path of the file and the mimes you want the files to be validated based on:


**Example** : 👇


.. code-block:: python

    from file_validator.validator import file_validator_by_python_magic

    file_validator_by_python_magic('image/png', 'image/jpeg', file_path='/path/to/file')


.. autofunction:: file_validator.validator.file_validator_by_python_magic


Django
--------------
To validate files in Django using python-magic we use the ``FileValidatorByPythonMagic`` class
In order to be able to use the validator written in `Django <https://www.djangoproject.com/>`_ using the
python-magic library, you must do the following:

1 .First, **import** the ``FileValidatorByPythonMagic`` to your Django model as follows:

.. code-block:: python

    from file_validator.django import FileValidatorByPythonMagic


2. Now add the ``FileValidatorByPythonMagic`` to your model validator like the
example below and give it the ``mimes`` you want the
file to be validated based on:

.. code-block:: python

    from django.db import models
    from file_validator.django import FileValidatorByPythonMagic


    class File(models.Model):
        file = models.FileField(validators=[FileValidatorByPythonMagic("image/png", "video/mp4")])

3. After this step, do a new migration to apply the changes

.. code-block::

        python manage.py makemigrations
        python manage.py migrate


.. autoclass:: file_validator.django.FileValidatorByPythonMagic
    :members: __init__, __call__
