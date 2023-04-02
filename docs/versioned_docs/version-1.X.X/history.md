---
sidebar_position: 8
---

# 📄 History


## 0.0.1 (2022-08-04)

* First release on PyPI.

## 0.0.2 (2022-08-06)

* Added django file validator

## 0.0.3 (2022-08-07)

* Added File Validator With File Type Library
* Added File Validator With Python Magic Library

## 0.0.4 (2022-08-07)

* Added File Validator

## 0.0.5 (2022-08-08)

* Added validator for pure python project
* Added get_mime_type_with_python_magic function
* Added get_extension_with_filetype_lib function
* Added get_mime_type_with_filetype_lib function
* Added file_validator_with_filetype_lib function

## 0.0.6 (2022-08-10)

* Refactoring project files

## 0.0.7 (2022-08-10)

* Adding Test To Project (file validator for pure python)
* Deleting get_mime_type_with_python_magic
* Deleting get_extension_with_filetype_lib
* Deleting get_mime_type_with_filetype_lib

## 0.0.8 (2022-08-11)

* Adding error message function for customization error messages
* Adding constants.py

## 0.0.9 (2022-08-11)

* Refactoring error message function

## 0.1.0 (2022-08-12)

* Fixing Minor Bug

## 0.1.1 (2022-08-12)

* Fixing python magic installation problem

## 0.1.2 (2022-08-14)

* Fixing installation problem

## 0.1.3 (2022-08-14)

* Adding installation guide for lib magic

## 0.1.4 (2022-08-15)

* Refactoring imports
* Refactoring error message
* Adding __eq__ to class
* Refactoring docstring
* Error handling when the mime type not found
* Adding the exception module
* Adding constant error message
* Refactor error_message function
* Fix get the extension problem with the mimetypes library

## 0.1.5 (2022-08-18)

* Adding File Size Validation
* Adding File Validation using Pure Magic Library
* Fix Minor Problem

## 0.1.6 (2022-08-23)

* In this version of file validator, instead of considering a separate class for each library that we want to use for file validation, we considered a whole class and left it to the administrator to choose the library that is going to perform the validation operation. From one class, you can perform validation operations by one or more libraries
* Adding Constants
* Fix AttributeError When Mime Not Found
* Fix Value Error When Selected One Mime
* Fix Minor Problem


0.1.7 (2023-02-05)
------------------
* add `ValidatedFileField` (django)
* reach test `100%`
* add size validator
* add file validator by django
* refactoring validators
* Improved code and performance
* add new documentation

0.1.8 (2023-02-05)
------------------
* improve and refactoring code

0.1.9 (2023-02-07)
------------------
* add file size validator (django)
* refactor and improve code

0.2.0 (2023-02-08)
------------------
* Fix Bug [error message function](https://github.com/file-validator/file-validator/commit/6a351bef661f3ffeabd1787574e0421f8035cda0)


0.2.1 (2023-02-08)
------------------
* Fix Bug [ValidatedFileField](https://github.com/file-validator/file-validator/commit/94b263d03034e8e8053bdac310a371d30be10a1b)

0.2.2 (2023-02-09)
------------------
* Error Handling when size is not valid in `size_validator` in `ValidatedFileField` ([#reference](https://github.com/file-validator/file-validator/commit/b4f1ce35140f9a91393f37d33588bd0ead32710d))

0.2.3 (2023-02-14)
------------------
* add validation in forms level (by Using `ValidatedFilefield` can you say which type of files are allowed)

0.2.4 (2023-02-15)
------------------
* providing custom css class for `ValidatedFilefield`

0.2.5 (2023-02-16)
------------------
* add return statements to `file_validator_by_python_magic` and providing information about the file

0.2.6 (2023-02-18)
------------------
* refactoring `validators` and now validators return validation data such `file_mime`, `file_extension`, `file_name` etc…

0.2.7 (2023-02-20)
------------------
* added `file_validator_by_type` : file validator for validation of the overall type of files such `image`, `audio`, `video`, `archive`, `font`
* added `guess_the_type` : This function is used to guess the overall type of file such `image`, `audio`, `video`, `font` and archive

0.2.8 (2023-02-23)
------------------
* refactored error message function
* added `current file mime` and `file name` to models error message


0.2.9 (2023-02-24)
------------------
* when mimes is empty returned MimesEmptyException instead of ValueError [#28](https://github.com/file-validator/file-validator/pull/28)
* added multiple attribute to forms [#33](https://github.com/file-validator/file-validator/pull/33)


0.3.0 (2023-02-25)
------------------
*  added file type such `image`, `audio` and `video` to result of validation

0.3.1, 0.3.2, 0.3.3 (2023-03-02)
------------------
*  fixed bug for installation python-magic [#71](https://github.com/file-validator/file-validator/pull/71)

0.3.4 (2023-03-03)
------------------
* refactored and improved code [#75](https://github.com/file-validator/file-validator/pull/75)

1.0.0
------------------
* In the 0.X.X version, each of the File Validats was a separate function but in this version they are all become a class  In the new version you can validate files based on extension, mime and size separately

1.0.1
------------------
* fixing to wrong use acceptable_mimes instead of guessed_mimes in [#166](https://github.com/file-validator/file-validator/pull/166)

1.0.2
------------------
* fix and modified error message for validate extension method in [#167](https://github.com/file-validator/file-validator/pull/168)

1.0.3
------------------
* fixing error message parameters name in [#169](https://github.com/file-validator/file-validator/pull/169)
