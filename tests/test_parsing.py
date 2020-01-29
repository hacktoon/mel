import pytest

from mel.parsing import Stream
from mel.exceptions import ParsingError


# STREAM TESTS ========================================

def test_valid_pattern_texts():
    stream = Stream('abc 24')
    text, _ = stream.read_pattern(r'[a-z]+')
    assert text == 'abc'


def test_valid_pattern_index():
    stream = Stream('foo')
    _, index = stream.read_pattern(r'[a-z]+')
    assert index == (0, 3)


def test_invalid_pattern():
    stream = Stream('54')
    with pytest.raises(ParsingError):
        stream.read_pattern(r'4')


def test_valid_symbols():
    stream = Stream('[]{}')
    assert stream.read_string('[')
    assert stream.read_string(']')
    assert stream.read_string('{')
    assert stream.read_string('}')


def test_save_restore():
    stream = Stream('    ')
    index = stream.save()
    try:
        stream.read_pattern(r'foo')
    except ParsingError:
        stream.restore(index)
    assert stream.read_pattern(r'\s+')


def test_read_pattern_advances_index():
    stream = Stream('    \n         ')
    stream.read_pattern(r'\s+')
    assert stream.index == len(stream.text)


def test_read_eof():
    stream = Stream('a')
    stream.read_string('a')
    assert stream.read_eof() == None


def test_read_eof_in_unfinished_file():
    stream = Stream('abc')
    stream.read_string('ab')
    with pytest.raises(ParsingError):
        stream.read_eof()


# PARSER TESTS ========================================

# def test_rule_parser():
#     g = Language()
#     g.rule('foo', g.p(r'\d+'))
#     parser = Parser(g)
#     assert str(parser.parse('42')) == '42'


# def test_parser_returns_node():
#     g = Language()
#     g.rule('foo', g.p(r'-\d+'))
#     parser = Parser(g)
#     assert isinstance(parser.parse('-333'), Node)


# def test_seq_parser():
#     g = Language()
#     g.rule('foo', g.seq(g.r('int'), g.p(r'foo')))
#     g.rule('int', g.p(r'\d+'))
#     assert Parser(g).parse('42foo')


# def test_seq_parser_children_count():
#     g = Language()
#     g.rule('foo', g.seq(g.r('abc'), g.s('--')))
#     g.rule('abc', g.p(r'[abc]+'))
#     node = Parser(g).parse('abbbcaa--')
#     assert len(node) == 2


# def test_zero_many_children_count():
#     g = Language()
#     g.rule('foo', g.zero_many(g.r('digit')))
#     g.rule('digit', g.p(r'[0-9]'))
#     node = Parser(g).parse('145')
#     assert len(node) == 3


# def test_one_of_rule_parser():
#     g = Language()
#     g.rule('foo', g.one_of(g.r('tag'), g.r('name')))
#     g.rule('tag', g.seq(g.s('#'), g.r('name')))
#     g.rule('name', g.p(r'[a-z]+'))
#     node = Parser(g).parse('#etc')
#     assert node.id == 'tag'


# def test_one_many_rule_parser():
#     g = Language()
#     g.rule('foo', g.one_many(g.r('tag')))
#     g.rule('tag', g.seq(g.s('#'), g.r('name')))
#     g.rule('name', g.p(r'[a-z]+'))
#     node = Parser(g).parse('#abc #etc')
#     assert node[0].id == 'tag'


# def test_space_skip():
#     g = Language()
#     g.rule('foo', g.r('name'))
#     g.skip('space', r'\s+')
#     g.rule('name', g.p(r'\w+'))
#     assert Parser(g).parse('    556   ')


# def test_space_skip_between_rules():
#     g = Language()
#     g.rule('foo', g.zero_many(g.r('name')))
#     g.skip('space', r'\s+')
#     g.rule('name', g.p(r'\w+'))
#     node = Parser(g).parse('   foo  bar ')
#     assert node[0].text == 'foo'
#     assert node[1].text == 'bar'
