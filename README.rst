==============
File Validator
==============


.. image:: https://img.shields.io/pypi/v/file_validator.svg?color=light
        :target: https://pypi.python.org/pypi/file_validator

.. image:: https://readthedocs.org/projects/file-validator/badge/?version=latest
        :target: https://file-validator.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg?color=light
        :target: https://python.org
        :alt: made with python

.. image:: https://img.shields.io/github/license/rzashakeri/file_validator?color=light
        :alt: GitHub
        :target: https://pypi.org/project/file-validator/

.. image:: https://img.shields.io/appveyor/build/rzashakeri/file-validator
        :alt: AppVeyor
        :target: https://ci.appveyor.com/api/projects/status/v8e1kr94a0259uw6?svg=true

.. image:: https://img.shields.io/codecov/c/github/rzashakeri/file_validator?token=13ZVSJWH8M
        :alt: Codecov
        :target: https://codecov.io/gh/rzashakeri/file_validator

.. image:: https://img.shields.io/pypi/pyversions/file-validator?color=light
        :alt: PyPI - Python Version
        :target: https://pypi.org/project/file-validator/

.. image:: https://static.pepy.tech/personalized-badge/file-validator?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads
        :target: https://pepy.tech/project/file-validator

.. image:: https://mperlet.github.io/pybadge/badges/10.svg
    :target: https://pypi.org/project/file-validator/
    :alt: pylint


.. image:: https://www.codefactor.io/repository/github/rzashakeri/file_validator/badge
   :target: https://www.codefactor.io/repository/github/rzashakeri/file_validator
   :alt: CodeFactor

.. image:: https://raw.githubusercontent.com/rzashakeri/file_validator/master/file_validator.png
        :target: https://raw.githubusercontent.com/rzashakeri/file_validator/master/file_validator.png


Features
--------
If you are looking for a safe way to validate your files,
the file validator library will do this for you, this
library also supports `Django <https://www.djangoproject.com/>`_. With this library you can
validate files based on extension, size, mimes and magic numbers

* File validation using the `filetype`_ library

.. _filetype: https://github.com/h2non/filetype.py

* File validation using the `python-magic`_ library

.. _python-magic: https://github.com/ahupp/python-magic

* File validation using the `mimetypes`_ library

.. _mimetypes: https://docs.python.org/3/library/mimetypes.html

* File validation using the `puremagic`_ library

.. _puremagic: https://github.com/cdgriffith/puremagic

.. | line |

* File validation with Size

.. |  line |

* Supporting for all `mimes`_

.. _mimes: https://www.iana.org/assignments/media-types/media-types.xhtml

.. |   line |

* File validation simultaneously with all four libraries



**installation**



To install File Validator, run this command in your terminal:

.. code-block:: console

    $ pip install file_validator


.. warning::
    After installing file validator, we need to install libmagic,
    which you need to install using the following command:

**for windows:**

.. code-block:: console

    $ pip install python-magic-bin


**for Debian/Ubuntu:**

.. code-block:: console

    $ sudo apt-get install libmagic1

**for OSX:**

When using Homebrew:

.. code-block:: console

    brew install libmagic


When using macports:

.. code-block:: console

    port install file



This is the preferred method to install File Validator, as it will always install the most recent stable release.




Documentation
--------------

* Read the `document`_ for more information

.. _document: https://file-validator.readthedocs.io

Credits
-------

This package was created By RezaShakeri_

.. _RezaShakeri: https://github.com/rzashakeri
