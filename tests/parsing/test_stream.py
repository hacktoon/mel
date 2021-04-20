import pytest

from mel.parsing.stream import (
    Char,
    Stream,
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

def create_stream(text=''):
    return Stream(text)


def as_string(chars):
    return ''.join(ch.value for ch in chars)


# BEGIN  TESTS ==================================

def test_empty_text_eof():
    stream = create_stream()
    assert stream.eof
    assert stream.read().type == EOF


def test_empty_text_char_type():
    stream = create_stream()
    assert isinstance(stream.read(), Char)


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
    (' ',  SPACE),
    ('\t', SPACE),
    ('\a', SPACE),
    ('\b', SPACE),
    ('\v', SPACE),
    ('\r', SPACE),
    ('%',  SYMBOL),
    ('*',  SYMBOL),
    ('_',  SYMBOL),
    ('"',  SYMBOL),
    ('\n', NEWLINE),
    ('é',  OTHER),
    ('ó',  OTHER),
    ('¨',  OTHER),
    ('£',  OTHER),
    ('ã',  OTHER)
])
def test_char_type(test_input, expected):
    stream = create_stream(test_input)
    assert stream.read().type == expected


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
    assert as_string(stream.read_one(DIGIT, LOWER)) == 'z'


def test_sequence_read_one_digit():
    stream = create_stream('4a')
    assert as_string(stream.read_one(LOWER, DIGIT)) == '4'
    assert as_string(stream.read_one(DIGIT, LOWER)) == 'a'


def test_char_read_many():
    stream = create_stream('abc 123')
    chars = stream.read_many(LOWER)
    assert as_string(chars) == 'abc'


def test_char_read_many_alnum():
    expected = 'a6bXc92A30'
    stream = create_stream(expected + '_12ab')
    chars = stream.read_many(LOWER, UPPER, DIGIT)
    assert as_string(chars) == expected


def test_char_read_many_digits():
    stream = create_stream('abc')
    chars = stream.read_many(DIGIT)
    assert chars == []


def test_char_read_many_symbols():
    text = '$%@*('
    stream = create_stream(text)
    chars = stream.read_many(SYMBOL)
    assert as_string(chars) == text
