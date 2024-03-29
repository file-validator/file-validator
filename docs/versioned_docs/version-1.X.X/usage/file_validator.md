---
sidebar_position: 1
---

# File Validator

In the [0.X.X](https://file-validator.github.io/docs/0.X.X/intro) version, each of the File Validats was a separate function but in this version they are all become a class

In the new version you can validate files based on extension, mime and size separately

## How Used?

### First Imported
You must first import `FileValidator` to use:
```python
from file_validator.validators import FileValidator
```


### Create Instance
At this point you should make an instance from the `FileValidator` class:
```python
file_validator = FileValidator(
    acceptable_extensions=[".png"],
    max_upload_file_size=1000000,
    acceptable_types=["image", "audio"],
    acceptable_mimes=["image/png"],
    file_path="path/to/file",
)
```

#### Parameters explanation
:::info


| Parameters            | Type                | Description                                                                                                                                                |
|-----------------------|:--------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| max_upload_file_size  | `int`    `optional` | If you want the file size to be checked, the file size must be in bytes, <br/> **example**: `max_upload_file_size=1048576`  (1MB) <br/> defaults to `None` |
| acceptable_extensions | `list`  `optional`  | The extensions you want the file to be checked based on. <br/> **example**: `acceptable_extensions=[".png"]`                                               |
| acceptable_types      | `list`              | The types you want the file to be checked based on. <br/> **example**: `acceptable_types=['audio', 'video']`                                               |
| acceptable_mimes      | `list`              | The mimes you want the file to be checked based on. <br/> **example**: `acceptable_mimes=['audio/mpeg', 'video/mp4']`                                      |
| file_path             | `string`            | The file path that you want to be validated                                                                                                                |

:::

### python-magic Library
If you want to perform file validation operations by the `python-magic` Library, you should use the `python_magic()` method as follows:

```python
file_validator.python_magic()
```


### pure-magic Library
If you want to perform file validation operations by the `pure-magic` Library, you should use the `pure_magic()` method as follows:

```python
file_validator.pure_magic()
```

### mimetypes Library
If you want to perform file validation operations by the `mimetypes` Library, you should use the `mimetypes()` method as follows:

```python
file_validator.mimetypes()
```


### filetype Library
If you want to perform file validation operations by the `filetype` Library, you should use the `filetype()` method as follows:

```python
file_validator.filetype()
```


### All Library
If you want to perform file validation operations by the `All` libraries , you should use the `validate()` method as follows:

```python
file_validator.validate()
```

### File Validation Based On The **Extension**
If you want to validate the files based on their `extension`, you should use the `validate_extension()` method:
```python
file_validator.validate_extension()
```


### File Validation Based On The **Mime**
If you want to validate the files based on their `MIME` and their `magic numbers`, you should use the `validate_mime()` method:
```python
file_validator.validate_mime()
```


### File Validation Based On The **type**
If you want to validate the files based on their `type` such `image`, `audio`, `video` and etc..., you should use the `validate_type()` method:
```python
file_validator.validate_type()
```


### File Validation Based On The **Size**
If you want to validate the files based on their `size`, you should use the `validate_size()` method:
```python
file_validator.validate_size()
```

### Size conversion table

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
