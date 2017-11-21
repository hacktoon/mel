import pytest
from dale.parsing import Parser
from dale.data import tokens
from dale.data.errors import LexingError, ParsingError


@pytest.mark.parametrize('test_input, expected', [
    ('56.75', 56.75),
    ('-0.75', -0.75),
    ('-.099999', -.099999),
    ('-0.75e10', -0.75e10),
    ('+1.45e-10', 1.45e-10),
    ('true', True),
    ('false', False),
    ('-56', -56),
    ('45', 45),
    ('"string"', 'string'),
    ("'string'", 'string'),
    ('@"/foo/bar"', '/foo/bar'),
    ('@"/foo/\nbar"', '/foo/\nbar'),
    ('@foo.bar', ['foo', 'bar']),
    ('@foo .\n bar', ['foo', 'bar']),
])
def test_parsing_single_values(test_input, expected):
    tree = Parser(test_input).parse()
    assert tree.value() == expected


@pytest.mark.parametrize('test_input', [
    ('%foo'),
    ('.bar'),
    (':orphan-param'),
    ('orphan-keyword'),
    ('@/foo/bar'),
])
def test_parsing_invalid_single_values_will_raise_errors(test_input):
    with pytest.raises(ParsingError):
        Parser(test_input).parse()


def test_list_parsing():
    tree = Parser('[1, 2.3, 3, @foo.bar "str" ]').parse()
    assert tree.value() == [1, 2.3, 3, ['foo', 'bar'], "str"]


def test_parsing_simple_expression():
    tree = Parser('(name :id 1 "foo")').parse()
    assert tree.value() == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': 'foo'
    }


def test_parsing_expression_with_named_closing():
    tree = Parser('(name :id 1 "foo")name)').parse()
    assert tree.value() == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': 'foo'
    }


def test_parsing_expression_with_wrong_closing_keyword():
    with pytest.raises(ParsingError):
        Parser('(start  \t "foo")end)').parse()


def test_parameters_parsing_using_comma_as_separator():
    tree = Parser('(x :a 1, :b 2, :c 3, "foo-bar")').parse()
    assert tree.value() == {
        'keyword': 'x',
        'parameters': {'a': 1, 'b': 2, 'c': 3},
        'values': 'foo-bar'
    }


def test_parsing_expression_with_multiple_children():
    tree = Parser(r'(kw :id 1, :title "foo" "bar" 34)').parse()
    assert tree.value() == {
        'keyword': 'kw',
        'parameters': {'id': 1, 'title': 'foo'},
        'values': ['bar', 34]
    }


def test_parsing_consecutive_expressions_with_sub_expressions():
    tree = Parser(r'(x "foo") (y (a 42))').parse()
    assert tree[0].value() == {'keyword': 'x', 'values': 'foo'}
    assert tree[1].value() == {
        'keyword': 'y', 'values': {
            'keyword': 'a', 'values': 42
        }
    }


def test_parsing_expression_with_a_list_as_child():
    tree = Parser('(opts [3 @foo.bar "str"])').parse()
    assert tree.value() == {
        'keyword': 'opts',
        'values': [3, ['foo', 'bar'], "str"]
    }


def test_parsing_expression_with_a_nested_expression_as_child():
    tree = Parser('(out [3 (in [4])])').parse()
    assert tree.value() == {
        'keyword': 'out',
        'values': [3, {'keyword': 'in', 'values': 4}]
    }


def test_non_terminated_expression_raises_error():
    with pytest.raises(ParsingError):
        Parser(r'(test 4').parse()


def test_parsing_help_expression():
    tree = Parser(r'(? "help me")').parse()
    assert tree.value() == {'keyword': '?', 'values': 'help me'}


@pytest.mark.skip
def test_help_expression_is_set_as_parent_nodes_help_property():
    tree = Parser(r'(? "help me")').parse()
    assert tree.value() == {'keyword': '?', 'values': 'help me'}