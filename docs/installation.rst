.. highlight:: shell

============
Installation
============


Stable release
--------------

To install File Validator, run this command in your terminal:

.. code-block:: console

    $ pip install file_validator


.. warning::
    After installing file validator, we need to install libmagic,
    which you need to install using the following command:

**for windows:** 👇

.. code-block:: console

    $ pip install python-magic-bin


**for Debian/Ubuntu:**  👇

.. code-block:: console

    $ sudo apt-get install libmagic1

**for OSX:**  👇

When using Homebrew:

.. code-block:: console

    brew install libmagic


When using macports:

.. code-block:: console

    port install file



This is the preferred method to install File Validator, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for File Validator can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/rzashakeri/file_validator

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/rzashakeri/file_validator/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/rzashakeri/file_validator
.. _tarball: https://github.com/rzashakeri/file_validator/tarball/master
