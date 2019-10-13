import pytest

from mel.nodes import Node
from mel.parsing import (
    TokenStream, Parser, one_of, zero_many, seq, t, r
)
from mel.exceptions import ParsingError


# HELPERS =========================================

def create_parser(text):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text):
    return Parser(text).parse()


def create_stream(text):
    return TokenStream(text)


# BEGIN TESTS ========================================

def test_valid_token_texts():
    stream = create_stream('abc 24')
    assert stream.read('name').text == 'abc'
    assert stream.read('space')
    assert stream.read('int').text == '24'


def test_valid_symbols():
    stream = create_stream('[]{}')
    assert stream.read('[')
    assert stream.read(']')
    assert stream.read('{')
    assert stream.read('}')


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

def test_token_parser():
    parser = t('int')
    stream = TokenStream('42')
    assert parser(stream).value == '42'


def test_rule_parser():
    parser = r('tag')
    stream = TokenStream('#foo')
    assert parser(stream)


def test_token_parser_node():
    parser = t('name')
    stream = TokenStream('foo')
    assert isinstance(parser(stream), Node)


def test_string_token_parser():
    parser = t('string')
    stream = TokenStream('"test"')
    assert parser(stream)


def test_seq_parser():
    parser = seq(t('string'), t('name'))
    stream = TokenStream('"test"foo')
    assert parser(stream)


def test_zero_many_parser():
    # TODO: grammar = '''
    # INT = \d+
    # NAME = [a-z]+
    # value = INT | NAME
    # '''
    parser = zero_many(r('keyword'))
    stream = TokenStream('!foo')
    assert parser(stream)


def test_one_of_parser():
    parser = one_of(t('name'), t('int'), t('string'))
    assert parser(TokenStream('556'))
    assert parser(TokenStream('foo'))
    assert parser(TokenStream('"abc"'))
