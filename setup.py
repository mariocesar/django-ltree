# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="django_ltree_fork",
    version="0.4.3",
    python_requires=">=2.7",
    url="https://github.com/boryszef/django-ltree",
    author="Borys Szefczyk",
    author_email="boryszef@gmail.com",
    description="django implemention of the ltree postgres extension - this is a backport to Python 2.7/Django 1.11",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("example",)),
    install_requires=[
        "django>=1.11",
        "six"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    project_urls={
        "Source": "https://github.com/boryszef/django_ltree",
        "Tracker": "https://github.com/boryszef/django_ltree/issues",
    },
)
