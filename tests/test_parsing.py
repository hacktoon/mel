import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context
from dale.exceptions import ExpectedValueError, UnexpectedTokenError


def create_parser(text):
    stream = TokenStream(text)
    return Parser(stream)


def create_tree(text):
    return create_parser(text).parse()


def eval(text, context_class=Context):
    context = context_class()
    context.tree = tree = create_tree(text)
    return tree.eval(context)


def test_empty_input_string():
    node = create_tree('')
    assert node.id == 'root'


def test_root_node_with_many_child_nodes():
    node = create_tree('(a) (@b 2) 223 "foo"/2')
    assert len(node) == 4


def test_node_children_index():
    node = create_tree('44 12')
    assert node[0].index == (0, 2)
    assert node[1].index == (3, 5)


def test_list_index():
    _list = create_tree('[1, 2]')
    assert _list.index == (0, 6)


def test_scope_index():
    scope = create_tree('(a 2)')
    assert scope.index == (0, 5)


@pytest.mark.parametrize('test_input', [
    ('56.75 (a b)'),
    ('!flag -0.75'),
    ('#id -.099999'),
    ('-0.75e10/55 etc'),
    ('+1.45e-10'),
    ('True  False'),
    ('"string"'),
    ("'string'"),
    ("@name 2"),
    ('?foo "test"')
])
def test_string_representation(test_input):
    tree = create_tree(test_input)
    assert str(tree) == test_input


@pytest.mark.parametrize('test_input, expected', [
    ('-215', 'int(-215)'),
    ('56.75', 'float(56.75)'),
    ('#id', 'uid(id)'),
    ('$path', 'variable(path)'),
    ('(bar 42)', 'scope(bar 42)'),
    ('[bar "etc"]', 'list(bar "etc")'),
    ('!active', 'flag(active)'),
    ('bar/42', 'path(bar/42)')
])
def test_object_representation(test_input, expected):
    tree = create_tree(test_input)
    assert repr(tree[0]) == expected


#  SCOPE TESTS

def test_empty_scope():
    parser = create_parser('()')
    node = parser.parse_scope()
    assert not node.key
    assert len(node) == 0
    assert repr(node) == 'scope()'


def test_nested_scopes():
    parser = create_parser('(a (b 2))')
    node = parser.parse_scope()
    subscope = node[0]
    assert str(node[0]) == '(b 2)'
    assert str(subscope.key) == 'b'
    assert str(subscope.nodes[0]) == '2'


def test_scope_key_with_attribute_by_token_value():
    parser = create_parser('(a (@b 2))')
    node = parser.parse_scope()
    assert node[0].key.name.value == 'b'


def test_unclosed_scope_raises_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree('(')


def test_scope_key_assumes_first_reference():
    parser = create_parser('(foo 42)')
    node = parser.parse_scope()
    assert str(node.key) == 'foo'


#  LIST TESTS

def test_empty_list():
    parser = create_parser('[]')
    node = parser.parse_list()
    assert len(node) == 0
    assert repr(node) == 'list()'


def test_one_sized_list_node_always_returns_list():
    parser = create_parser('[3]')
    node = parser.parse_list()
    assert node.id == 'list'


#  REFERENCE TESTS

def test_simple_reference():
    parser = create_parser('name/6')
    node = parser.parse_value()
    assert len(node) == 2


def test_unexpected_finished_reference_error():
    with pytest.raises(ExpectedValueError):
        create_tree('name/')


def test_unexpected_separator_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree('/')
