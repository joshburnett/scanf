from setuptools import setup
import pypandoc

scanf_long_description = pypandoc.convert('README.md', 'rst')

import scanf

setup(
    name = "scanf",
    version = scanf.__version__,

    py_modules=["scanf"],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # metadata for upload to PyPI
    author = "Josh Burnett",
    author_email = "scanf@burnettsonline.org",
    description = "A small scanf implementation",
    long_description=scanf_long_description,
    license = "MIT",
    keywords = "scanf",
    platform = "any",
    url = "https://github.com/joshburnett/scanf",
)