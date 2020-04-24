# coding=utf-8
import os

from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths)) as f:
        return f.read()


setup(
    name='covid',
    version='0.0.2',
    packages=['covid'],
    url='https://github.com/strizhechenko/covid',
    license='MIT',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    description='Getting latest covid-19 stats in World, Russia and Ekaterinburg to your cli',
    # long_description=(read('README.rst')),
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
        'covid-ru',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'covid=covid.__init__:main',
        ],
    },
)
