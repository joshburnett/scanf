from setuptools import setup

# string generated using pypandoc.convert_file('README.md', 'rst')
scanf_long_description = "scanf: A small scanf implementation for python\n==============================================\n\nPython has powerful regular expressions but sometimes they are totally\noverkill when you just want to parse a simple-formatted string. C\nprogrammers use the scanf-function for these tasks (see link below).\n\nThis implementation of scanf translates the simple scanf-format into\nregular expressions. Unlike C you can be sure that there are no buffer\noverflows possible.\n\nFor more information see:\n\n-  http://www.python.org/doc/current/lib/node49.html\n-  http://en.wikipedia.org/wiki/Scanf\n\nOriginal code from:\nhttp://code.activestate.com/recipes/502213-simple-scanf-implementation/\n\nModified original to make the %f more robust, as well as added %\\*\nmodifier to skip fields.\n\nReleases\n--------\n\n1.0: 2010-10-11\n~~~~~~~~~~~~~~~\n\n-  Initial release\n\n1.1: 2010-10-13\n~~~~~~~~~~~~~~~\n\n-  Changed regex from 'match' (only matches at beginning of line) to\n   'search' (matches anywhere in line)\n-  Bugfix - ignore cast for skipped fields\n\n1.2: 2013-05-30\n~~~~~~~~~~~~~~~\n\n-  Added 'collapseWhitespace' flag (defaults to True) to take the search\n   string and replace all whitespace with regex string to match repeated\n   whitespace. This enables better matching in log files where the data\n   has been formatted for easier reading. These cases have variable\n   amounts of whitespace between the columns, depending on the number of\n   characters in the data itself.\n\n1.3: 2016-01-18\n~~~~~~~~~~~~~~~\n\n-  Added 'extractdata' function.\n\n1.3.1 - 1.3.3: 2016-06-23\n~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Fixed various issues with metadata for PyPI\n"

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
        'Programming Language :: Python :: 3',
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
