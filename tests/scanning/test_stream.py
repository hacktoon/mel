import pytest

from mel.scanning.char import Char
from mel.scanning.stream import CharStream


# HELPER FUNCTIONS ==================================

def create_stream(text=''):
    return CharStream(text)


def as_string(chars):
    return ''.join(ch.value for ch in chars)


# BEGIN  TESTS ==================================

def test_empty_text_is_eof():
    stream = create_stream()
    assert stream.peek().is_eof()


def test_empty_text_has_zero_length():
    stream = create_stream()
    assert len(stream) == 0


def test_stream_length():
    stream = create_stream('abc')
    assert len(stream) == 3


def test_empty_text_char_type():
    stream = create_stream()
    assert stream.read().is_eof()


@pytest.mark.parametrize('test_input, method', [
    ('a',  'is_lower'),
    ('h',  'is_lower'),
    ('z',  'is_lower'),
    ('A',  'is_upper'),
    ('M',  'is_upper'),
    ('Z',  'is_upper'),
    ('0',  'is_digit'),
    ('1',  'is_digit'),
    ('5',  'is_digit'),
    ('9',  'is_digit'),
    (' ',  'is_space'),
    ('\t', 'is_space'),
    ('\a', 'is_space'),
    ('\b', 'is_space'),
    ('\v', 'is_space'),
    ('\r', 'is_space'),
    ('%',  'is_symbol'),
    ('*',  'is_symbol'),
    ('_',  'is_symbol'),
    ('"',  'is_symbol'),
    ('\n', 'is_newline'),
    ('é',  'is_other'),
    ('ó',  'is_other'),
    ('¨',  'is_other'),
    ('£',  'is_other'),
    ('ã',  'is_other')
])
def test_char_type(test_input, method):
    stream = create_stream(test_input)
    ch = stream.read()
    assert getattr(ch, method)()


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


def test_is_next_char():
    stream = create_stream('a3')
    assert stream.peek().value == 'a'
    assert not stream.peek().value == 'C'
    stream.read()
    assert stream.peek().value == '3'
