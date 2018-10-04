import scanf
from setuptools import setup

with open('README.md') as readme:
    scanf_long_description = readme.read()


setup(
    name = "scanf",
    version = scanf.__version__,

    py_modules=["scanf"],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # metadata for upload to PyPI
    author = "Josh Burnett",
    author_email = "scanf@burnettsonline.org",
    description = "A small scanf implementation",
    long_description=scanf_long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    keywords = "scanf",
    install_requires=['backports.functools_lru_cache;python_version<"2.9"'],
    platform = "any",
    url = "https://github.com/joshburnett/scanf",
)
