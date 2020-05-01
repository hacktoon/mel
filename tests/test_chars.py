import pytest

from infiniscribe.parsing.chars import parse
from infiniscribe.parsing.chars import (
    LOWER, UPPER, DIGIT, SYMBOL, SPACE, NEWLINE, OTHER
)


# HELPER FUNCTIONS ==================================

def char_list(text):
    return list(parse(text))


def char_type_at(text, index=0):
    chars = char_list(text)
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


@pytest.mark.parametrize('test_input, char, index', [
    ('a\nb', '\n', 1),
    ('a\nb', 'b', 2),
])
def test_char_index(test_input, char, index):
    chars = char_list(test_input)
    index = chars[index].index
    assert test_input[index] == char


@pytest.mark.parametrize('test_input, index, line', [
    ('a\nb',   1, 0),
    ('a\nb',   2, 1),
    ('a\r\nb', 3, 1),
])
def test_char_line(test_input, index, line):
    chars = char_list(test_input)
    assert chars[index].line == line


@pytest.mark.parametrize('test_input, index, column', [
    ('ab\nc',       0, 0),
    ('ab\nc',       3, 0),
    ('ab\t\r\n\nc', 6, 0),
    ('ab\nc',       1, 1),
])
def test_char_column(test_input, index, column):
    chars = char_list(test_input)
    assert chars[index].column == column
