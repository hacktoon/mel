import pytest

from mel.lexing import TokenStream
from mel.exceptions import ParsingError


def create_stream(text):
    return TokenStream(text)


def test_valid_token_texts():
    stream = create_stream('abc 24')
    assert stream.parse('name').text == 'abc'
    assert stream.parse('space')
    assert stream.parse('int').text == '24'


def test_invalid_tokens():
    stream = create_stream('54')
    with pytest.raises(ParsingError):
        assert stream.parse('name')


def test_save_restore():
    stream = create_stream('    ')
    index = stream.save()
    try:
        stream.parse('string')
    except ParsingError:
        stream.restore(index)
    assert stream.parse('space')
