import pytest
from dale.parsing import Parser
from dale.data import tokens
from dale.data.errors import LexingError, ParsingError


def test_value_rule_for_float_token():
    tree = Parser('56.72').parse()
    assert tree.value() == 56.72


def test_value_parsing_as_string():
    tree = Parser(r'"foo"').parse()
    assert tree.value() == 'foo'


def test_simple_expression_parsing():
    tree = Parser('(name :id 1 "foo")').parse()
    assert tree[0].keyword.value() == 'name'
    assert tree[0].parameters.value() == {'id': 1}


def test_expression_named_closing():
    tree = Parser('(name :id 1 "foo")name)').parse()
    assert tree[0].value() == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': 'foo'
    }


def test_named_expression_closing_with_wrong_keyword():
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


def test_non_terminated_expression_raises_error():
    with pytest.raises(ParsingError):
        Parser(r'(test 4').parse()


def test_parsing_documentation_keyword_expression():
    tree = Parser(r'(? "help me")').parse()
    assert tree.value() == {'keyword': '?', 'values': 'help me'}