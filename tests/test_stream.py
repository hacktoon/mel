import pytest

from mel.parsing import CharStream
from mel.exceptions import ParsingError


# STREAM TESTS ========================================

def test_valid_pattern_texts():
    stream = CharStream('abc 24')
    text, _ = stream.read_pattern(r'[a-z]+')
    assert text == 'abc'


def test_valid_pattern_index():
    stream = CharStream('foo')
    _, index = stream.read_pattern(r'[a-z]+')
    assert index == (0, 3)


def test_invalid_pattern():
    stream = CharStream('54')
    with pytest.raises(ParsingError):
        stream.read_pattern(r'4')


def test_valid_symbols():
    string = '[]{}'
    stream = CharStream(string)
    for s in string:
        assert stream.read_string(s)


def test_save_restore():
    stream = CharStream('    ')
    index = stream.save()
    try:
        stream.read_pattern(r'foo')
    except ParsingError:
        stream.restore(index)
    assert stream.read_pattern(r'\s+')


def test_read_pattern_advances_index():
    stream = CharStream('    \n         ')
    stream.read_pattern(r'\s+')
    assert stream.index == len(stream.text)


def test_closing_stream():
    stream = CharStream('a')
    stream.read_string('a')
    assert stream.close() is None


def test_closing_unfinished_file():
    stream = CharStream('abc')
    stream.read_string('ab')
    with pytest.raises(ParsingError):
        stream.close()
