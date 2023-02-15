---
sidebar_position: 1
---

# Validated File Field
Using `ValidatedFilefield` can you say which type of files are allowed

Before we go to the `Validatedfilefield` tutorial, let's first get acquainted with `ValidatedFilefield` parameters

## Parameters
:::info


| Parameters       | Type  | Description                                                                                                                                                                                                                                                                |
|------------------|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| accept           | `str` | The accept attribute takes as its value a comma-separated list of one or more file types, or unique file type specifiers, [describing which file types to allow. See this guide for more familiarity](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept) |
| custom_css_class | `str` | A custom class to customize input                                                                                                                                                                                                                                          |

:::


## How Use ValidatedFilefield?


To use `ValidatedFilefield` you must act as follows:

1.First, import the `ValidatedFilefield` to your Django forms as follows:

```python
from django import forms
from file_validator.forms import ValidatedFileField
```
2. In the next step we have to give it to our form as follows:

```python
from django import forms
from file_validator.forms import ValidatedFileField

class TestForm(forms.Form):
    test_file = ValidatedFileField(
        accept='image/*' # => accept attribute
    )

```

