import pytest

from mel.scanning.stream import CharStream


# BEGIN  TESTS ==================================

def test_empty_text_is_eof():
    stream = CharStream()
    assert stream.get().is_eof()


def test_empty_text_has_zero_length():
    stream = CharStream()
    assert len(stream) == 0


def test_stream_length():
    stream = CharStream('abc')
    assert len(stream) == 3


def test_empty_text_char_type():
    stream = CharStream()
    assert stream.get().is_eof()


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
    stream = CharStream(test_input)
    ch = stream.get()
    assert getattr(ch, method)()


def test_char_line():
    text = 'ab\nc\n\nd'
    stream = CharStream(text)
    lines = [stream.get(i).line for i, _ in enumerate(text)]
    assert lines == [0, 0, 0, 1, 1, 2, 3]


def test_char_column():
    text = 'ab\nc\n\nd'
    stream = CharStream(text)
    lines = [stream.get(i).column for i, _ in enumerate(text)]
    assert lines == [0, 1, 2, 0, 1, 0, 0]


def test_char_values():
    text = 'i76hj-'
    stream = CharStream(text)
    values = ''.join([
        stream.get(i).value
        for i, _ in enumerate(text)
    ])
    assert values == text


def test_is_next_char():
    stream = CharStream('a3')
    assert stream.get(0).value == 'a'
    assert not stream.get(1).value == 'C'
    assert stream.get(1).value == '3'
