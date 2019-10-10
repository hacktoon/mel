import pytest

from mel.parsing import TokenStream, Parser, t, r
from mel.exceptions import ParsingError


# HELPERS

def create_parser(text):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text):
    return Parser(text).parse()


def create_stream(text):
    return TokenStream(text)


# BEGIN TESTS

def test_valid_token_texts():
    stream = create_stream('abc 24')
    assert stream.read('name').text == 'abc'
    assert stream.read('space')
    assert stream.read('int').text == '24'


def test_valid_symbols():
    stream = create_stream('[]{}')
    assert stream.read('open_list')
    assert stream.read('close_list')
    assert stream.read('open_query')
    assert stream.read('close_query')


def test_invalid_tokens():
    stream = create_stream('54')
    with pytest.raises(ParsingError):
        assert stream.read('name')


def test_save_restore():
    stream = create_stream('    ')
    index = stream.save()
    try:
        stream.read('string')
    except ParsingError:
        stream.restore(index)
    assert stream.read('space')


# PARSER ===========================================

def test_int_parser():
    parser = t('int')
    stream = TokenStream('42')
    assert parser(stream).value == '42'


def test_rule_parser():
    parser = r('tag')
    stream = TokenStream('#foo')
    return parser, stream
