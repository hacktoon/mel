import pytest

from mel.lexing.stream import Char, CharStream


# HELPER FUNCTIONS ==================================

def create_stream(text=''):
    return CharStream(text)


def as_string(chars):
    return ''.join(ch.value for ch in chars)


# BEGIN  TESTS ==================================

def test_empty_text_eof():
    stream = create_stream()
    assert stream.eof
    assert stream.read().type == Char.EOF


def test_empty_text_char_type():
    stream = create_stream()
    assert isinstance(stream.read(), Char)


def test_empty_stream_read_many():
    stream = create_stream()
    assert stream.read_many() == []


@pytest.mark.parametrize('test_input, expected', [
    ('a',  Char.LOWER),
    ('h',  Char.LOWER),
    ('z',  Char.LOWER),
    ('A',  Char.UPPER),
    ('M',  Char.UPPER),
    ('Z',  Char.UPPER),
    ('0',  Char.DIGIT),
    ('1',  Char.DIGIT),
    ('5',  Char.DIGIT),
    ('9',  Char.DIGIT),
    (' ',  Char.SPACE),
    ('\t', Char.SPACE),
    ('\a', Char.SPACE),
    ('\b', Char.SPACE),
    ('\v', Char.SPACE),
    ('\r', Char.SPACE),
    ('%',  Char.SYMBOL),
    ('*',  Char.SYMBOL),
    ('_',  Char.SYMBOL),
    ('"',  Char.SYMBOL),
    ('\n', Char.NEWLINE),
    ('é',  Char.OTHER),
    ('ó',  Char.OTHER),
    ('¨',  Char.OTHER),
    ('£',  Char.OTHER),
    ('ã',  Char.OTHER)
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
    char = stream.read(Char.LOWER)
    assert char.value == 'a'


def test_char_read_by_unexpected_type_returns_none():
    stream = create_stream('22')
    char = stream.read(Char.LOWER)
    assert char is None


def test_read_one_lower():
    stream = create_stream('z')
    assert as_string(stream.read_one(Char.DIGIT, Char.LOWER)) == 'z'


def test_sequence_read_one_digit():
    stream = create_stream('4a')
    assert as_string(stream.read_one(Char.LOWER, Char.DIGIT)) == '4'
    assert as_string(stream.read_one(Char.DIGIT, Char.LOWER)) == 'a'


def test_char_read_many():
    stream = create_stream('abc 123')
    chars = stream.read_many(Char.LOWER)
    assert as_string(chars) == 'abc'


def test_char_read_many_alnum():
    expected = 'a6bXc92A30'
    stream = create_stream(expected + '_12ab')
    chars = stream.read_many(Char.LOWER, Char.UPPER, Char.DIGIT)
    assert as_string(chars) == expected


def test_char_read_many_digits_wrong_text():
    stream = create_stream('abc')
    chars = stream.read_many(Char.DIGIT)
    assert chars == []


def test_char_read_many_symbols():
    text = '$%@*('
    stream = create_stream(text)
    chars = stream.read_many(Char.SYMBOL)
    assert as_string(chars) == text
