====================
django
====================

To validate files in Django we use the ``FileValidator`` class
In order to be able to use the validator written in `Django <https://www.djangoproject.com/>`_ , you must do the following:


1 .First, **import** the ``FileValidator`` to your Django model as follows:

.. code-block:: python

    from file_validator.django import FileValidator


2. Now add the ``FileValidator`` to your model validator like the
example below and give it the ``mimes`` you want the
file to be validated based on and, ``libraries`` with which you want to validate files
and ``file_size`` is the size you want the file to be validated against

.. note::
    ``file_size`` and ``libraries`` are optional and if you don't specify a
    value for libraries, the validation operation is performed with
    all the libraries that are supported, i.e. ``filetype``, ``mimetypes``,
    ``pure magic``, ``python magic``.


.. code-block:: python

    from django.db import models
    from file_validator.django import FileValidatorByPythonMagic


    class File(models.Model):
        file = models.FileField(validators=[
            FileValidator(
                libraries=["filetype", "pure_magic", "mimetypes"],
                mimes=["audio/mpeg", "image/png"],
                file_size=10485760
                )
            ]
        )


.. warning::
    Since the `python-magic <https://github.com/ahupp/python-magic>`_ library may treat audio files
    like mp3 as programs or application/octet-stream and it's a bit
    annoying, I suggest when you want to validate audio files from
    three libraries (`filetype <https://github.com/h2non/filetype.py>`_, `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_, `pure magic <https://github.com/cdgriffith/puremagic>`_) or use the safe mode method.



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
