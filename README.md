# scanf: A small scanf implementation for python

Python has powerful regular expressions but sometimes they are totally overkill when you just want to parse a simple-formatted string. C programmers use the scanf-function for these tasks (see link below).

This implementation of scanf translates the simple scanf-format into regular expressions. Unlike C you can be sure that there are no buffer overflows possible.

For more information see:

  * http://www.python.org/doc/current/lib/node49.html
  * http://en.wikipedia.org/wiki/Scanf

Original code from:
	http://code.activestate.com/recipes/502213-simple-scanf-implementation/

Modified original to make the %f more robust, as well as added %* modifier to skip fields.

## Releases

### 1.0: 2010-10-11
  * Initial release

### 1.1: 2010-10-13
  * Changed regex from 'match' (only matches at beginning of line)
        to 'search' (matches anywhere in line)
  * Bugfix - ignore cast for skipped fields

### 1.2: 2013-05-30
  * Added 'collapseWhitespace' flag (defaults to True) to take the search
      string and replace all whitespace with regex string to match repeated
      whitespace.  This enables better matching in log files where the data
      has been formatted for easier reading.  These cases have variable
      amounts of whitespace between the columns, depending on the number
      of characters in the data itself.
      
### 1.3: 2016-01-18
  * Added 'extractdata' function.
    
### 1.3.1 - 1.3.3: 2016-06-23
  * Fixed various issues with metadata for PyPI