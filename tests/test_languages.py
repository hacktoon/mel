import pytest

from mel.languages import Language
from mel.exceptions import ParsingError
from mel.parsing import Stream, Grammar


def test_base_rule():
    g = Grammar()
    g.root(g.zero_many(g.r('rule')))
    g.rule('rule', g.seq(
        g.r('name'), g.s('='), g.r('sequence'), g.NEWLINE
    ))
    # g.rule('alternative', g.seq(
    #     g.r('sequence'),
    #     g.zero_many(g.seq(g.s('|'), g.r('sequence')))
    # ))
    g.rule('sequence', g.zero_many(g.r('name')))
    g.rule('name', g.p(r'[a-z]+'))

    g.skip('space', r'[ \t]+')
    g.skip('comment', r'--[^\n\r]*')

    lang = Language('Foo', g)
    node = lang.parse('address = street num')
    breakpoint()
    assert node


# def test_language_name():
#     lang = Language('Foo', 'etc')
#     assert lang.name == 'Foo'


# def test_grammar_text_attribute():
#     grammar = 'number = INT'
#     lang = Language('Foo', grammar)
#     assert lang.grammar.text == grammar


# def test_int_parser_grammar():
#     lang = Language('Bar', '')
#     stream = Stream('  42  ')
#     node = lang.grammar.match(stream)
#     assert str(node) == '42'


# def test_invalid_eof_parser_grammar():
#     lang = Language('Bar', '')
#     stream = Stream('42   u')
#     with pytest.raises(ParsingError):
#         node = lang.grammar.match(stream)


# @mel.rule("object")
# def object_parser(node):
#     key = node.key
#     children = node.body
#     return ObjectNode(key, children)