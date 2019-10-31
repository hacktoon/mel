import pytest

from mel.nodes import Node
from mel.parsing import (
    Stream, Parser, one_of, zero_many, seq, r
)
from mel.exceptions import ParsingError


# HELPERS =========================================

def create_parser(text):
    stream = Stream(text)
    return Parser(stream)


def parse(text):
    return Parser(text).parse()


def create_stream(text):
    return Stream(text)


# BEGIN TESTS ========================================

def test_valid_pattern_texts():
    stream = create_stream('abc 24')
    text, _ = stream.read_pattern(r'[a-z]+')
    assert text == 'abc'


def test_valid_pattern_index():
    stream = create_stream('foo')
    _, index = stream.read_pattern(r'[a-z]+')
    assert index == (0, 3)


def test_invalid_pattern():
    stream = create_stream('54')
    with pytest.raises(ParsingError):
        assert stream.read_pattern(r'4')


def test_valid_symbols():
    stream = create_stream('[]{}')
    assert stream.read_string('[')
    assert stream.read_string(']')
    assert stream.read_string('{')
    assert stream.read_string('}')


def test_save_restore():
    stream = create_stream('    ')
    index = stream.save()
    try:
        stream.read_pattern(r'foo')
    except ParsingError:
        stream.restore(index)
    assert stream.read_pattern(r'\s+')


# PARSER ===========================================

def test_token_parser():
    parser = r('int')
    stream = Stream('42')
    assert str(parser(stream)) == '42'


def test_read_pattern_advances_index():
    stream = Stream('    \n         ')
    stream.read_pattern(r'\s+')
    assert stream.index == len(stream.text)


def test_rule_parser():
    parser = r('tag')
    stream = Stream('#foo')
    assert parser(stream)


def test_token_parser_node():
    parser = r('name')
    stream = Stream('foo')
    assert isinstance(parser(stream), Node)


def test_string_token_parser():
    parser = r('string')
    stream = Stream('"test"')
    assert parser(stream)


def test_seq_parser():
    parser = seq(r('string'), r('name'))
    stream = Stream('"test"foo')
    assert parser(stream)


def test_seq_parser_children_count():
    parser = seq(r('string'), r('name'))
    stream = Stream('"test"foo')
    assert len(parser(stream)) == 2


def test_zero_many_children_count():
    parser = zero_many(r('keyword'))
    stream = Stream('!foo@test')
    assert len(parser(stream)) == 2


def test_one_of_parser():
    parser = one_of(r('name'), r('int'), r('string'))
    assert parser(Stream('556'))
    assert parser(Stream('foo'))
    assert parser(Stream('"abc"'))


def test_space_skip():
    parser = r('int')
    assert parser(Stream('    556'))
