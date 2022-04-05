import pytest

from mel.scanning import char


# HELPER FUNCTIONS ==================================


# BEGIN  TESTS ==================================

def test_empty_base_char():
    ch = char.BaseChar()
    assert ch.value is None


def test_empty_char():
    ch = char.DigitChar()
    assert ch.value is None


def test_char_eq_type():
    d1 = char.DigitChar()
    d2 = char.DigitChar()
    assert d1 == d2


def test_char_eq_with_value():
    a_char = char.LowerChar('a')
    a2_char = char.LowerChar('a')
    assert a_char == a2_char


def test_char_ne():
    lw = char.LowerChar()
    up = char.UpperChar()
    assert lw != up


def test_char_ne_with_value():
    a_char = char.LowerChar('a')
    b_char = char.LowerChar('b')
    assert a_char != b_char
