====================
Python Magic Library
====================
python-magic is a Python interface to the libmagic file type identification
library. libmagic identifies file types by checking their headers according
to a predefined list of file types. This functionality is exposed to the
command line by the Unix command file.


.. warning::
    Since the `python-magic <https://github.com/ahupp/python-magic>`_ library may treat audio files
    like mp3 as programs or application/octet-stream and it's a bit
    annoying, I suggest when you want to validate audio files from
    two libraries (`filetype <https://github.com/h2non/filetype.py>`_, `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_) or use the safe mode method.



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
        file = models.FileField(validators=[FileValidatorByPythonMagic(mimes=['audio/mpeg', 'video/mp4'],file_size=1048576)])



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



.. autoclass:: file_validator.django.FileValidatorByPythonMagic
    :members: __init__, __call__
