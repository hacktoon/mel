import pytest
import random
import string

from infiniscribe.parsing.chars import (
    CharStream,
    LOWER,
    UPPER,
    DIGIT,
    SYMBOL,
    SPACE,
    NEWLINE,
    OTHER,
    EOF
)


# HELPER FUNCTIONS ==================================

def create_stream(text):
    return CharStream(text)


# TESTS ==================================

def test_empty_text():
    stream = create_stream('')
    assert len(stream) == 0


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
    ('ã',  OTHER),
    ('',  EOF),
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


def test_char_read_many():
    stream = create_stream('abc 123')
    chars = stream.read_many([LOWER])
    token = ''.join(c.value for c in chars)
    assert token == 'abc'
