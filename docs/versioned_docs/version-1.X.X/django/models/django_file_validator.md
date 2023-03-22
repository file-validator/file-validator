---
sidebar_position: 2
---

# Django File Validator

Django File Validator falls into the Validators category and another feature provided for file validation in Django

## Parameters
:::info


| Parameters           | Type                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----------------------|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| libraries            | `list`  `optional`         | The value of libraries should be a list of libraries with which you want to perform the validation operation. <br/> **Example** :     `libraries=["filetype","python_magic", "filetype"]` <br/> defaults If you do not select any library, it will perform the validation operation with `django` by default, Supported libraries for validation operations: `python_magic`, `pure_magic`, `filetype`, `mimetypes`, `all`, `default` <br/> If you use `all`, validation operations will be performed with all libraries and if you use `default`, validation operations will only be done with `Django` |
| acceptable_mimes     | `list`                      | The mimes you want the file to be checked based on. <br/> **example**: `acceptable_mimes=['audio/mpeg', 'video/mp4']`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| acceptable_types     | `list`                      | The types you want the file to be checked based on. <br/> **example**: `acceptable_types=['audio', 'video']`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| max_upload_file_size | `int`    `optional`         | If you want the file size to be checked, the file size must be in bytes, <br/> **example**: `max_upload_file_size=1048576`  (1MB) <br/> defaults to `None`                                                                                                                                                                                                                                                                                                                                                                                                                                              |

:::

## Returns

:::info

| Returns:                                                                                                                                                                                                         |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| If the mime list is **empty**, raised a `value error`                                                                                                                                                            |
| If the library you entered is not supported, raised a` value error`, <br/> **Supported library:** `filetype`, `mimetypes`, `pure_magic`, `python_magic`, `all`, `default`                                        |
| if file not valid raises `ValidationError`                                                                                                                                                                       |
| At least one of the parameters of `acceptable_mimes` or `acceptable_types` must be filled else `EmptyParametersException` error occurs                                                                           |
| If the type you enter in `acceptable_types` is not supported by the file-validator library, it will cause `TypeNotSupportedException` error, supported types are `audio`, `video`, `image`, `font` and `archive` |

:::

## Size conversion table

:::note

To choose the size you want the files to be validated based
on, you can take help from the table below or enter your
desired size in bytes:


| Size   |              Bytes              |
|--------|:-------------------------------:|
|        |                                 |
| 1 MB   | 1048576 B - 1024**2 B - 2**20 B |
| 2.5 MB |            2621440 B            |
| 5 MB   |            5242880 B            |
| 10 MB  |           10485760 B            |
| 20 MB  |           20971520 B            |
| 50 MB  |           52428800 B            |
| 100 MB |           104857600 B           |
| 250 MB |           262144000 B           |
| 500 MB |           524288000 B           |
| 1 GB   |          1073741824 B           |
| 2 GB   |          2147483648 B           |
|        |                                 |




:::


## How Use DjangoFileValidator?


To use FileValidator you must act as follows:

1.First, import the `DjangoFileValidator` to your Django model as follows:

```python
from django.db import models
from file_validator.models import DjangoFileValidator
```
2. In the next step we have to give it to our model as follows:

```python
from django.db import models
from file_validator.models import DjangoFileValidator

class TestFileModel(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=["python_magic", "filetype"], # => validation operations will be performed with all libraries
                acceptable_mimes=['audio/mpeg', 'video/mp4', 'image/png'], # => The mimes you want the file to be checked based on.
                acceptable_types=['audio', 'video', 'image'], # => The types you want the file to be checked based on.
                max_upload_file_size=10485760  # => 10 MB
            )
        ]
    )
```

3. Finally run with the following commands:

```
python manage.py makemigrations
```
```
python manage.py migrate
```

Done ✅

From now on, get the files safely from users.
