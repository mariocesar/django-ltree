# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="django_ltree",
    version="0.5.3",
    python_requires=">=2.7",
    url="https://github.com/mariocesar/django-ltree",
    author="Mario César Señoranis Ayala",
    author_email="mariocesar@humanzilla.com",
    description="Django app to support ltree postgres extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("example",)),
    extras_require={"develop": ["twine", "tox"]},
    install_requires=["django>=1.11", "six"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Source": "https://github.com/mariocesar/django_ltree",
        "Tracker": "https://github.com/mariocesar/django_ltree/issues",
    },
)
