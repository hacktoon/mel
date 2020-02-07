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
