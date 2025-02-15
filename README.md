scanf: A small scanf implementation for python
==============================================

Python has powerful regular expressions but they can be totally
overkill for many simpler situations. Additionally, some common
numerical formats require quite complex regex's to match them
robustly. This python implementation of scanf internally translates the simple
scanf format into regular expressions, then returns the parsed values.

Usage
-------------

scanf.scanf(format, s=None, collapseWhitespace=True)

*Arguments*

- **format:** This is the format string comprised of plain text and tokens from the
  table below.
- **s:** String to be parsed
- **collapseWhitespace:** When True, tells scanf to perform a greedy match with
  whitespace in the input string, allowing for easy parsing of text that has
  been formatted to be read more easily. This enables better matching in log files where the data
  has been formatted for easier reading. These cases have variable
  amounts of whitespace between the columns, depending on the number of
  characters in the data itself.


scanf supports the following formats:

| Pattern  | Meaning                                  |
| :------- | :--------------------------------------- |
| %c       | One character                            |
| %5c      | 5 characters                             |
| %d, %i   | int value                                |
| %7d, %7i | int value with length 7                  |
| %f       | float value                              |
| %o       | octal value                              |
| %X, %x   | hex value                                |
| %s       | string terminated by whitespace          |

Any pattern with a * after the % (*e.g.*, '%*f') will result in scanf matching the pattern but
omitting the matched portion from the results.  This is helpful when parts of
the input string may change but should be ignored.

The underlying regex operation is performed using 'search' rather than 'match',
so scanf will return a match if the pattern string is matched anywhere in the line.


*Examples:*

```
>>> from scanf import scanf
>>> scanf("%s - %d errors, %d warnings", "/usr/sbin/sendmail - 0 errors, 4 warnings")
('/usr/sbin/sendmail', 0, 4)

>>> scanf("%o %x %d", "0123 0x123 123")
(83, 291, 123)

>>> pattern = 'Power: %f [%], %s, Stemp: %f'
>>> text = 'Power:   0.0 [%], Cool, Stemp: 23.73'
>>> scanf(pattern, text)
(0.0, 'Cool', 23.73)

>>> pattern = 'Power: %f [%], %*s, Stemp: %f'   # note the '*' in %*s
>>> scanf(pattern, text)
(0.0, 23.73)
```

scanf returns a tuple of parsed values if the input pattern is matched, or None if the format does not match.


Other resources
---------------------

For more information see:

- http://en.wikipedia.org/wiki/Scanf
- https://github.com/joshburnett/scanf

Original (pre-1.0) code from:
http://code.activestate.com/recipes/502213-simple-scanf-implementation/


Releases
--------

### 1.6.0: 2025-02-15

- Contributor improvements (thanks @ejeffrey!)
  - Add integer support
  - Convert regex strings to raw strings (fixes warnings in Python 3.13)
  - Update octal format
  - Add binary formats
  - Add tests
- Modernize project slightly: change from setup.py to pyproject.toml, move to src layout

### 1.5.2: 2018-10-04

- Fixed installation issue 

### 1.5.1: 2018-10-04

- Re-added Python 2.7 compatibility via backports.functools_lru_cache (thanks @eendebakpt!)

### 1.5: 2018-10-01

- Fixed Python 3.7 compatibility (scanf_compile broke in 3.7 due to differences in re.sub)
- Changed caching to functools.lru_cache (in Python 3 standard library)
- Dropping Python 2 support, as lru_cache is not in Python 2 standard library
- Caching now takes collapseWhitespace into account (thanks @prittenhouse!)

### 1.4.1: 2017-04-05

- Added $^| characters to the list of special characters to escape in 'scanf_compile'. Thanks @MichaelWedel!

### 1.4: 2016-12-03

- Small modification to scanf.py for Python3 compatibility. Thanks @Gattocrucco!
- Changed README.md to README.rst, removing pypandoc dependency in setup.py
- Removed most of the comments at the beginning of scanf.py, as they were
  redundant with those in the README.

### 1.3.1 - 1.3.3: 2016-06-23

- Initial release to PyPI
- Fixed various issues with metadata for PyPI

### 1.3: 2016-01-18

- Added 'extractdata' function.

### 1.2: 2013-05-30

- Added 'collapseWhitespace' flag (defaults to True) to take the search
  string and replace all whitespace with regex string to match repeated
  whitespace. This enables better matching in log files where the data
  has been formatted for easier reading. These cases have variable
  amounts of whitespace between the columns, depending on the number of
  characters in the data itself.

### 1.1: 2010-10-13

- Changed regex from 'match' (only matches at beginning of line) to
  'search' (matches anywhere in line)
- Bugfix - ignore cast for skipped fields

### 1.0: 2010-10-11

- Initial release (internal)

