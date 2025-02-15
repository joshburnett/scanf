"""
A small pure-Python scanf implementation

Python has powerful regular expressions but sometimes they are totally overkill
when you just want to parse a simple-formatted string.
C programmers use the scanf-function for these tasks (see link below).

This implementation of scanf translates the simple scanf-format into
regular expressions. Unlike C you can be sure that there are no buffer overflows
possible.

For more information see
  * https://docs.python.org/3/library/re.html
  * http://en.wikipedia.org/wiki/Scanf

Original (pre-1.0) code from:
    http://code.activestate.com/recipes/502213-simple-scanf-implementation/

Modified original to make the %f more robust, as well as added %* modifier to
skip fields. Other improvements over time as well.
"""
import re
import sys
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

__version__ = '1.6.0'

__all__ = ["scanf", 'extractdata', 'scanf_translate', 'scanf_compile']


DEBUG = False


# As you can probably see it is relatively easy to add more format types.
# Make sure you add a second entry for each new item that adds the extra
#   few characters needed to handle the field ommision.
scanf_translate = [
    (re.compile(_token), _pattern, _cast) for _token, _pattern, _cast in [
        (r"%c", r"(.)", lambda x:x),
        (r"%\*c", r"(?:.)", None),

        (r"%(\d)c", r"(.{%s})", lambda x:x),
        (r"%\*(\d)c", r"(?:.{%s})", None),

        (r"%(\d)d", r"([+-]?\d{%s})", int),
        (r"%\*(\d)d", r"(?:[+-]?\d{%s})", None),

        (r"%d", r"([+-]?\d+)", int),
        (r"%\*d", r"(?:[+-]?\d+)", None),

        (r"%u", r"(\d+)", int),
        (r"%\*u", r"(?:\d+)", None),

        (r"%[fgeE]", r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)", float),
        (r"%\*[fgeE]", r"(?:[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)", None),

        (r"%s", r"(\S+)", lambda x:x),
        (r"%\*s", r"(?:\S+)", None),

        (r"%[xX]", r"((?:0[xX])?[\dA-Za-f]+)", lambda x:int(x, 16)),
        (r"%\*[xX]", r"(?:(?:0[xX])?[\dA-Fa-f]+)", None),

        (r"%o", r"(?:0[oO])?([0-7]+)", lambda x:int(x, 8)),
        (r"%\*o", r"(?:(?:0[oO])?[0-7]+)", None),

        (r"%b", r"(?:0[bB])?([01]+)", lambda x: int(x, 2)),
        (r"%\*b", r"(?:0[bB])?(?:[01]+)", None),

        (r"%i", r"([+-]?(?:0[xXoObB])?[0-9a-fA-F]+)", lambda x: int(x, 0)),
        (r"%\*i", r"(?:[+-]?(?:0[xXoObB])?[0-9a-fA-F]+)", None),
        
        (r"%r", r"(.*$)", lambda x: x),
        (r"%\*r", r"(?:.*$)", None),
    ]]


# Cache formats
SCANF_CACHE_SIZE = 1000


@lru_cache(maxsize=SCANF_CACHE_SIZE)
def scanf_compile(format, collapseWhitespace=True):
    """
    Translate the format into a regular expression

    For example:
    >>> format_re, casts = scanf_compile('%s - %d errors, %d warnings')
    >>> print format_re.pattern
    (\\S+) \\- ([+-]?\\d+) errors, ([+-]?\\d+) warnings

    Translated formats are cached for faster reuse
    """

    format_pat = ""
    cast_list = []
    i = 0
    length = len(format)
    while i < length:
        found = None
        for token, pattern, cast in scanf_translate:
            found = token.match(format, i)
            if found:
                if cast: # cast != None
                    cast_list.append(cast)
                groups = found.groupdict() or found.groups()
                if groups:
                    pattern = pattern % groups
                format_pat += pattern
                i = found.end()
                break
        if not found:
            char = format[i]
            # escape special characters
            if char in "|^$()[]-.+*?{}<>\\":
                format_pat += "\\"
            format_pat += char
            i += 1
    if DEBUG:
        print("DEBUG: %r -> %s" % (format, format_pat))
    if collapseWhitespace:
        format_pat = re.sub(r'\s+', r'\\s+', format_pat)

    format_re = re.compile(format_pat)
    return format_re, cast_list


def scanf(format, s=None, collapseWhitespace=True):
    """
    scanf supports the following formats:
      %c        One character
      %5c       5 characters
      %d, %i    int value
      %7d, %7i  int value with length 7
      %f        float value
      %o        octal value
      %X, %x    hex value
      %s        string terminated by whitespace
    Examples:
    >>> scanf("%s - %d errors, %d warnings", "/usr/sbin/sendmail - 0 errors, 4 warnings")
    ('/usr/sbin/sendmail', 0, 4)
    >>> scanf("%o %x %d", "0o123 0x123 123")
    (83, 291, 123)
    scanf.scanf returns a tuple of found values
    or None if the format does not match.
    """

    if s is None:
        s = sys.stdin

    if hasattr(s, "readline"):
        s = s.readline()

    format_re, casts = scanf_compile(format, collapseWhitespace)

    found = format_re.search(s)
    if found:
        groups = found.groups()
        return tuple([casts[i](groups[i]) for i in range(len(groups))])


def extractdata(pattern, text=None, filepath=None):
    """
    Read through an entire file or body of text one line at a time. Parse each line that matches the supplied
    pattern string and ignore the rest.

    If *text* is supplied, it will be parsed according to the *pattern* string.
    If *text* is not supplied, the file at *filepath* will be opened and parsed.
    """
    y = []
    if text is None:
        textsource = open(filepath, 'r')
    else:
        textsource = text.splitlines()

    for line in textsource:
        match = scanf(pattern, line)
        if match:
            if len(y) == 0:
                y = [[s] for s in match]
            else:
                for i, ydata in enumerate(y):
                    ydata.append(match[i])

    if text is None:
        textsource.close()

    return y


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, report=True)
