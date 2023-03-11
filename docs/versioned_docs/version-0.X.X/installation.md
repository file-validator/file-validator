---
sidebar_position: 2
---

# 💡 Installation

## Install Stable release

In this section we start installing File Validator

To install File Validator, run this command in your terminal:

```
pip install file-validator
```

:::caution

After installing file validator, we need to install **libmagic**, which you need to install using the following command:

for windows:
```
pip install python-magic-bin
```
for Debian/Ubuntu:
```
sudo apt-get install libmagic1
```
for OSX:

When using Homebrew:
```
brew install libmagic
```
When using macports:
```
port install file
```
:::



This is the preferred method to install File Validator, as it will always install the most recent stable release

If you don’t have [pip](https://pip.pypa.io/) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

## From sources

The sources for File Validator can be downloaded from the Github repo.

You can either clone the public repository:
```
git clone git://github.com/file-validator/file-validator
```

Or download the tarball:
```
curl -OJL https://github.com/file-validator/file-validator/tarball/master
```

Once you have a copy of the source, you can install it with:
```
python setup.py install
```
