from infiniscribe.parsing.chars import parse
from infiniscribe.parsing.chars import (
    LOWER, UPPER, DIGIT, SYMBOL, SPACE, NEWLINE, OTHER
)


# HELPER FUNCTIONS ==================================

def char_list(chars):
    return list(parse(chars))


def char_type_at(chars, index=0):
    chars = char_list(chars)
    return chars[index].type


# TESTS ==================================

def test_empty_text():
    chars = char_list('')
    assert len(chars) == 0


def test_lower_letters():
    assert char_type_at('a') == LOWER


def test_upper_letters():
    assert char_type_at('Y') == UPPER


def test_digits():
    assert char_type_at('5') == DIGIT


def test_space():
    assert char_type_at(' ') == SPACE


def test_symbol():
    assert char_type_at('$') == SYMBOL


def test_newline():
    assert char_type_at('\n') == NEWLINE


def test_other():
    assert char_type_at('\r') == OTHER
