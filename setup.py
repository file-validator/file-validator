#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "filetype>=1.1.0",
    "termcolor>=1.1.0",
    "python-magic>=0.4.27",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Reza Shakeri",
    author_email="rzashakeri@outlook.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A library for validating files in Python",
    entry_points={
        "console_scripts": [
            "file_validator=file_validator.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords=[
        "file_validator",
        "file",
        "validator",
        "image_validator",
        "audio_validator",
        "video_validator",
        "django"
    ],
    name="file_validator",
    packages=find_packages(include=["file_validator", "file_validator.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/rzashakeri/file_validator",
    version="0.1.3",
    zip_safe=False,
)
