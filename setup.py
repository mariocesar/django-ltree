from setuptools import setup, find_packages

setup(
    name='django_ltree',
    version='0.3',
    python_requires='>=3.6',
    url='https://github.com/mariocesar/django-ltree',
    author='Mario César Señoranis Ayala',
    description='A django that implements in a model the ltree postgres extension',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    project_urls={
        'Source': 'https://github.com/mariocesar/django_ltree',
        'Tracker': 'https://github.com/mariocesar/django_ltree/issues',
    },
)
