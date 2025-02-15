#!/usr/bin/env python
import scanf
import pytest

def scanf_star(fmt, data, *args):
    """Wrap a scanf call to also test null conversion"""

    
    result = scanf.scanf(fmt, data, *args)
    if result is None:
        return result
    null_fmt = fmt.replace('%', '%*')
    assert scanf.scanf(null_fmt, data, *args) == ()
    if "%r" not in fmt:
        result_w_rest = scanf.scanf(fmt + r"%r", data, *args)
        rest_only = scanf.scanf(null_fmt + r"%r", data, *args)
        assert result_w_rest[-1] == rest_only[0]
    return result


def test_float():
    assert scanf_star("%f", "32.1") == (32.1,)
    assert scanf_star("%f", "+32.1") == (32.1,)
    assert scanf_star("%f", "+032.1") == (32.1,)
    assert scanf_star("%f", "+32.10") == (32.1,)
    assert scanf_star("%e", "32.2abc") == (32.2,)
    assert scanf_star("%e", "-32.2") == (-32.2,)
    assert scanf_star("%g", "32") == (32.,)
    assert scanf_star("%f", ".3") == (0.3,)
    assert scanf_star("%f", "0.3") == (0.3,)

def test_skip_beginning():
    """Note, this behavior is different from C stdlib"""
    assert scanf_star("%e", "abc 321e-1") == (32.1,)

def test_literals():
    assert scanf_star("is: %d", "The number is: 52") == (52,)
    assert scanf_star("is: %d", "The number is 52") is None
    assert scanf_star("is: %d", "The number is: \n 52") == (52,)

def test_char():
    assert scanf_star("%c", "abc") == ('a',)
    assert scanf_star("%3c", "abc") == ('abc',)
    assert scanf_star("%5c", "abc") is None
    assert scanf_star("%s", "The first word") == ("The",)
    assert scanf_star("%s", "Including: punctuation") == ("Including:",)

def test_decimal():
    assert scanf_star("%d", "50")[0] == 50
    assert scanf_star("%d", "050")[0] == 50
    assert scanf_star("%d", "0x50")[0] == 0

def test_signed():
    assert scanf_star("%d", "-42")[0] == -42
    assert scanf_star("%d", "+42")[0] == +42
    assert scanf_star("%d %d", "-0 +42") == (0, 42)
    
def test_hex():
    assert scanf_star("%x", "0x50")[0]  == 0x50
    assert scanf_star("%x", "0X50")[0]  == 0x50
    assert scanf_star("%X", "0x50")[0]  == 0x50
    assert scanf_star("%X", "0X50")[0]  == 0x50
    assert scanf_star("%x", "50")[0]  == 0x50
    assert scanf_star("%X", "50")[0]  == 0x50

def test_octal():
    assert scanf_star("%o", "050")[0] == 0o50
    assert scanf_star("%o", "777")[0] == 0o777
    assert scanf_star("%o", "0o50")[0] == 0o50
    assert scanf_star("%o", "0O50")[0] == 0o50

def test_rest():
    n, r = scanf.scanf("%d %r", "99 bottles of beer on the wall")
    assert n == 99
    assert r == "bottles of beer on the wall"
    
def test_binary():
    assert scanf_star("%b", "1100")[0] == 12
    assert scanf_star("%b", "0b1100")[0] == 12
    
def test_integer():
    assert scanf_star("%i", "50")[0] == 50
    assert scanf_star("%i", "0x50")[0] == 0x50
    assert scanf_star("%i", "0o50")[0] == 0o50
    assert scanf_star("%i", "0b1100")[0] == 12

def test_multiple():
    assert scanf_star("%s %s", "hello, world") == ("hello,", "world")

    # Note that this illustrates the different behavior of
    # regular expressions: it is able to match the literal comma
    # rather than the preceding %s consuming it.
    assert scanf_star("%s, %s", "hello, world") == ("hello", "world")

    assert scanf_star("%d - %d", "52 - 11") == (52, 11)
    mac =  scanf_star("%X:%X:%X:%X:%X:%X", "04:23:AB:03:ef:01")
    assert mac == (0x4, 0x23, 0xab, 0x3, 0xef, 0x1)

    
