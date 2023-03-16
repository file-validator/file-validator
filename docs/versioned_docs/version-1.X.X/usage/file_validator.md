---
sidebar_position: 1
---

# file validator

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

### File Validation Using The **python-magic** Library
If you want to perform validation operations by the `python-magic` Library, you should use the `python_magic()` method as follows:

```python
file_validator.python_magic()
```


### File Validation Using The **pure-magic** Library
If you want to perform validation operations by the `pure-magic` Library, you should use the `pure_magic()` method as follows:

```python
file_validator.pure_magic()
```

### File Validation Using The **mimetypes** Library
If you want to perform validation operations by the `mimetypes` Library, you should use the `mimetypes()` method as follows:

```python
file_validator.mimetypes()
```


### File Validation Using The **filetype** Library
If you want to perform validation operations by the `filetype` Library, you should use the `filetype()` method as follows:

```python
file_validator.filetype()
```


### File Validation Using The **All** Library
If you want to perform validation operations by the `All` libraries , you should use the `filetype()` method as follows:

```python
file_validator.validate()
```


### File Validation Based On The Mime
If you want to validate the files based on their `MIME` and their `magic numbers`, you should use the `validate_mime()` method:
```python
file_validator.validate_mime()
```

### File Validation Based On The Extension
If you want to validate the files based on their `extension`, you should use the `validate_extension()` method:
```python
file_validator.validate_extension()
```

### File Validation Based On The Size
If you want to validate the files based on their `size`, you should use the `validate_size()` method:
```python
file_validator.validate_size()
```

### File Validation Based On The type
If you want to validate the files based on their `type` such `image`, `audio`, `video` and etc..., you should use the `validate_type()` method:
```python
file_validator.validate_type()
```
