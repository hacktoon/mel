import pytest
import random
import string

from infiniscribe.parsing.stream import (
    Stream,
    LOWER,
    UPPER,
    DIGIT,
    SYMBOL,
    SPACE,
    NEWLINE,
    OTHER
)


# HELPER FUNCTIONS ==================================

def create_stream(text=''):
    return Stream(text)


def concat_values(chars):
    return ''.join(ch.value for ch in chars)


# BEGIN  TESTS ==================================

def test_empty_text():
    stream = create_stream()
    assert len(stream) == 0


def test_eof():
    stream = create_stream()
    assert stream.read().is_eof()


def test_empty_stream_read_many():
    stream = create_stream()
    assert stream.read_many() == []


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
    (' s',  SPACE),
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
    ('ã',  OTHER)
])
def test_char_type(test_input, expected):
    stream = create_stream(test_input)
    assert stream.read().type == expected


def test_char_index():
    text = 'ab\r\nc\td '
    stream = create_stream(text)
    indexes = [stream.read().index for _ in text]
    assert indexes == list(range(8))


def test_char_line():
    text = 'ab\nc\n\nd'
    stream = create_stream(text)
    lines = [stream.read().line for _ in text]
    assert lines == [0, 0, 0, 1, 1, 2, 3]


def test_char_column():
    text = 'ab\nc\n\nd'
    stream = create_stream(text)
    lines = [stream.read().column for _ in text]
    assert lines == [0, 1, 2, 0, 1, 0, 0]


def test_char_values():
    text = 'i76hj-'
    stream = create_stream(text)
    values = [stream.read().value for _ in text]
    assert values == list(text)


def test_char_is_digit():
    text = random.choice(string.digits)
    stream = create_stream(text)
    assert stream.read().is_digit()


def test_char_is_not_digit():
    choices = string.ascii_letters + string.punctuation + string.whitespace
    text = random.choice(choices)
    stream = create_stream(text)
    assert not stream.read().is_digit()


def test_char_is_lower():
    text = random.choice(string.ascii_lowercase)
    stream = create_stream(text)
    assert stream.read().is_lower()


def test_char_is_upper():
    text = random.choice(string.ascii_uppercase)
    stream = create_stream(text)
    assert stream.read().is_upper()


def test_char_is_symbol():
    text = random.choice(string.punctuation)
    stream = create_stream(text)
    assert stream.read().is_symbol()


def test_char_is_space():
    text = random.choice(' \t\x0b\x0c')
    stream = create_stream(text)
    assert stream.read().is_space()


def test_char_is_not_space():
    text = random.choice(string.ascii_letters)
    stream = create_stream(text)
    assert not stream.read().is_space()


def test_char_is_newline():
    stream = create_stream('\n')
    assert stream.read().is_newline()


def test_char_is_not_newline():
    text = random.choice(string.ascii_letters)
    stream = create_stream(text)
    assert not stream.read().is_newline()


def test_char_is_other():
    text = random.choice('éàõ¢£¬áï\r')
    stream = create_stream(text)
    assert stream.read().is_other()


def test_char_is_not_other():
    text = random.choice(string.ascii_letters + string.digits)
    stream = create_stream(text)
    assert not stream.read().is_other()


def test_char_read_by_type():
    stream = create_stream('abc 123')
    char = stream.read(LOWER)
    assert char.value == 'a'


def test_char_read_by_unexpected_type_returns_none():
    stream = create_stream('22')
    char = stream.read(LOWER)
    assert char is None


def test_read_one_lower():
    stream = create_stream('z')
    assert stream.read_one(DIGIT, LOWER).value == 'z'


def test_sequence_read_one_digit():
    stream = create_stream('4a')
    assert stream.read_one(LOWER, DIGIT).value == '4'
    assert stream.read_one(DIGIT, LOWER).value == 'a'


def test_char_read_many():
    stream = create_stream('abc 123')
    chars = stream.read_many(LOWER)
    token = concat_values(chars)
    assert token == 'abc'


def test_char_read_many_alnum():
    expected = 'a6bXc92A30'
    stream = create_stream(expected + '_12ab')
    chars = stream.read_many(LOWER, UPPER, DIGIT)
    token = concat_values(chars)
    assert token == expected


def test_char_read_many_digits():
    stream = create_stream('abc')
    chars = stream.read_many(DIGIT)
    assert chars == []


def test_char_read_many_symbols():
    text = '$%@*('
    stream = create_stream(text)
    chars = stream.read_many(SYMBOL)
    token = concat_values(chars)
    assert token == text


# def test_char_read_whitespace():
#     stream = create_stream(' \n\t   t \r  a ')
#     stream.read_whitespace()
#     nonws = stream.read()
#     assert nonws.index == 7
#     assert nonws.type == SPACE


# def test_char_read_integers():
#     text = '634'
#     stream = create_stream(text)
#     integers = [int(c.value) for c in stream.read_integers()]
#     assert integers == [6, 3, 4]
