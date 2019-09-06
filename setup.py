# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="django_ltree",
    version="0.4",
    python_requires=">=2.7",
    url="https://github.com/boryszef/django-ltree",
    author="Borys Szefczyk (original code: Mario César Señoranis Ayala)",
    author_email="boryszef@gmail.com",
    description="django implemention of the ltree postgres extension - this is a backport to Python 2.7/Django 1.11",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("example",)),
    install_requires=[
        "django>=1.11",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Source": "https://github.com/boryszef/django_ltree",
        "Tracker": "https://github.com/boryszef/django_ltree/issues",
    },
)
