import pytest

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


@pytest.mark.parametrize('test_input, expected', [
    ('a',  LOWER),
    ('h',  LOWER),
    ('z',  LOWER),
    ('A',  UPPER),
    ('M',  UPPER),
    ('Z',  UPPER),
    ('0',  DIGIT),
    ('1',  DIGIT),
    ('5',  DIGIT),
    ('9',  DIGIT),
    (' ',  SPACE),
    ('\t', SPACE),
    ('%',  SYMBOL),
    ('*',  SYMBOL),
    ('"',  SYMBOL),
    ('\n', NEWLINE),
    ('\r', OTHER),
    ('é',  OTHER),
    ('ó',  OTHER),
    ('¨',  OTHER),
    ('£',  OTHER),
    ('ã',  OTHER),
])
def test_char_type(test_input, expected):
    assert char_type_at(test_input) == expected


# Test char index in a text
@pytest.mark.parametrize('test_input, char, index', [
    ('a\nb', '\n', 1),
])
def test_char_index(test_input, char, index):
    chars = char_list(test_input)
    index = chars[index].index
    assert test_input[index] == char
