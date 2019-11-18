from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="django_ltree",
    version="0.4",
    python_requires=">=3.6",
    url="https://github.com/mariocesar/django-ltree",
    author="Mario César Señoranis Ayala",
    author_email="mariocesar@humanzilla.com",
    description="A django that implements in a model the ltree postgres extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("example",)),
    install_requires=["django>=2.0"],
    extras_require={"develop": ["pytest"]},
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
        "Source": "https://github.com/mariocesar/django_ltree",
        "Tracker": "https://github.com/mariocesar/django_ltree/issues",
    },
)
