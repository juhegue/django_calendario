import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_calendario',
    version='1.1',
    packages=['calendario'],
    include_package_data=True,
    license='BSD License',
    description='Calendario',
    long_description=README,
    url='',
    author='juhegue',
    author_email='juhegue@hotmail.es',
    install_requires=[
        'Django',   # ==3.2.16
        'requests',
        'APScheduler',
        'django-post-office',
        'MonthDelta',
        'mysqlclient',
        'pyfcm',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Calendario',
    ],
)