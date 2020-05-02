import pytest
import random
import string

from infiniscribe.parsing.chars import (
    char_generator,
    CharStream,
    LOWER,
    UPPER,
    DIGIT,
    SYMBOL,
    SPACE,
    NEWLINE,
    OTHER
)


# HELPER FUNCTIONS ==================================

def char_list(text):
    return list(char_generator(text))


def char_type_at(text, index=0):
    return char_at(text, index).type


def char_at(text, index=0):
    chars = char_list(text)
    return chars[index]


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
    ('ab\t\r\n\nc', 6, 2),
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


def test_char_is_digit():
    test_input = random.choice(string.digits)
    assert char_at(test_input).is_digit()


def test_char_is_not_digit():
    choices = string.ascii_letters + string.punctuation + string.whitespace
    test_input = random.choice(choices)
    assert not char_at(test_input).is_digit()


def test_char_is_lower():
    test_input = random.choice(string.ascii_lowercase)
    assert char_at(test_input).is_lower()


def test_char_is_upper():
    test_input = random.choice(string.ascii_uppercase)
    assert char_at(test_input).is_upper()


def test_char_is_symbol():
    test_input = random.choice(string.punctuation)
    assert char_at(test_input).is_symbol()


def test_char_is_space():
    test_input = random.choice(' \t\x0b\x0c')
    assert char_at(test_input).is_space()


def test_char_is_not_space():
    negative_test_input = random.choice(string.ascii_letters)
    assert not char_at(negative_test_input).is_space()


def test_char_is_newline():
    assert char_at('\n').is_newline()


def test_char_is_not_newline():
    negative_test_input = random.choice(string.ascii_letters)
    assert not char_at(negative_test_input).is_newline()


def test_char_is_other():
    test_input = random.choice('éàõ¢£¬áï\r')
    assert char_at(test_input).is_other()


def test_char_is_not_other():
    choices = string.ascii_letters + string.digits
    negative_test_input = random.choice(choices)
    assert not char_at(negative_test_input).is_other()


# CHAR STREAM TESTS ===========================================

def test_char_stream():
    stream = CharStream('abc')
    assert stream.read().value == 'a'
