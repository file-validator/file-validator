---
sidebar_position: 1
---

# file validator

In the [0.X.X](https://file-validator.github.io/docs/0.X.X/intro) version, each of the File Validats was a separate function but in this version they are all become a class

In the new version you can validate files based on extension, mime and size separately


You must first import `FileValidator` to use
```python
from file_validator.validators import FileValidator
```


```python
file_validator = FileValidator(
    acceptable_mimes=["image/png"],
    file_path="path/to/file",
)
result_of_validation = file_validator.python_magic()
```
