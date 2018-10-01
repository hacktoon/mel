import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale import nodes
from dale.utils.context import Context
from dale.exceptions import UnexpectedTokenError


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context_class=Context):
    context = context_class()
    context.tree = tree = create_tree(text)
    return tree.eval(context)


def test_node_type():
    tree = create_tree('(foo bar)')
    assert isinstance(tree, nodes.Node)


def test_object_representation():
    tree = create_tree('(a 5)')
    assert repr(tree) == 'Node'


@pytest.mark.parametrize('test_input, expected', [
    ('56.75', '56.75'),
    ('-0.75', '-0.75'),
    ('-.099999', '-.099999'),
    ('-0.75e10', '-0.75e10'),
    ('+1.45e-10', '+1.45e-10'),
    ('True', 'True'),
    ('False', 'False'),
    ('"string"', '"string"'),
    ("'string'", "'string'"),
    ("@name", '@name'),
    ('?foo', '?foo')
])
def test_string_representation(test_input, expected):
    tree = create_tree(test_input)
    assert str(tree) == expected


def test_unclosed_scope_raises_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree('(')
