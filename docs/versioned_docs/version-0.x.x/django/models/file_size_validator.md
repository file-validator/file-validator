---
sidebar_position: 3
---

# File Size Validator

You can use `Filesizevalidator` for when you just want to validate the **file size**

## Parameters
:::info


| Parameters           | Type                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----------------------|:----------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| max_upload_file_size | `int`                 | If you want the file size to be checked, the file size must be in bytes, <br/> **example**: `max_upload_file_size=1048576`  (1MB)                                                                                                                                                                                                                                                                                                                                                                                                                                          |

:::

## Returns

:::info

| Returns:                                                                              |
|:--------------------------------------------------------------------------------------|
| If everything is OK, it will return None, otherwise it will return a `ValidationError`. |

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


## How Use FileSizeValidator?


To use FileSizeValidator you must act as follows:

1.First, import the `FileSizeValidator` to your Django model as follows:

```python
from django.db import models
from file_validator.models import FileSizeValidator
```
2. In the next step we have to give it to our model as follows:

```python
from django.db import models
from file_validator.models import FileSizeValidator

class TestFileModel(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
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
