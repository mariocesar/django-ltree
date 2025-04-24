from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="django_ltree",
    version="0.6.0",
    python_requires=">=3.10",
    url="https://github.com/mariocesar/django-ltree",
    author="Mario César Señoranis Ayala",
    author_email="mariocesar@humanzilla.com",
    description="Django app to support ltree postgres extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["django_ltree", "django_ltree.migrations"],
    extras_require={"develop": ["twine", "tox"]},
    install_requires=["django>=2.2"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    project_urls={
        "Source": "https://github.com/mariocesar/django_ltree",
        "Tracker": "https://github.com/mariocesar/django_ltree/issues",
    },
)
