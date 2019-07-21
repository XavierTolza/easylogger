from setuptools import setup

# All your settings
dir = "easylogger"
name = dir
description = "Wrapper for logging library for easier python logging"
author = 'Xavier Tolza'
email = 'tolza.xavier@gmail.com'

# Init
kwargs = {}

# Handle requirements
with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setup(
    name=name,
    version='1.0',
    description=description,
    author=author,
    author_email=email,
    packages=[name],  # same as name
    install_requires=requirements,
    **kwargs
)
