# coding=utf-8
import os

from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths)) as f:
        return f.read()


setup(
    name='covid-ru',
    version='0.0.6',
    packages=['covid_ru'],
    url='https://github.com/strizhechenko/covid-ru',
    license='MIT',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    description='Getting latest covid-19 stats in Russia to your cli',
    long_description=(read('README.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'covid-ru=covid_ru.__init__:main',
        ],
    },
)
