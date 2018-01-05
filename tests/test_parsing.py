import os

import pytest

from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser
from dale.exceptions import (
    UnexpectedTokenError,
    UnexpectedTokenValueError,
    FileError
)


def eval(text):
    tokens = Lexer(text).tokenize()
    stream = TokenStream(tokens)
    tree = Parser(stream).parse()
    return tree.eval({})


def test_list_parsing():
    tree = eval('[1, 2.3, true, foo.bar "str" ]')
    assert tree[0] == [1, 2.3, True, ['foo', 'bar'], "str"]


def test_EOF_while_parsing_list():
    with pytest.raises(UnexpectedTokenError):
        eval('[1, 2.3, 3, ')


def test_parsing_wrong_value_node():
    with pytest.raises(UnexpectedTokenError):
        tree = eval('(x :a :b)')


def test_EOF_while_parsing_reference():
    with pytest.raises(UnexpectedTokenError):
        eval('foo.bar.')


def test_parsing_simple_expression():
    tree = eval('(name :id 1 "foo")')
    assert tree[0] == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': ['foo']
    }


def test_parsing_expression_with_named_ending():
    tree = eval('(name :id 1 "foo" ) name )')
    assert tree[0] == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': ['foo']
    }


def test_parsing_expression_with_wrong_ending_keyword():
    with pytest.raises(UnexpectedTokenValueError):
        eval('(start  \t "foo")end)')


def test_parameters_parsing_using_comma_as_separator():
    tree = eval('(x :a 1, :b 2, :c 3, "foo-bar")')
    assert tree[0] == {
        'keyword': 'x',
        'parameters': {'a': 1, 'b': 2, 'c': 3},
        'values': ['foo-bar']
    }


def test_parsing_expression_with_multiple_children():
    tree = eval('(kw :id 1, :title "foo" "bar" 34)')
    assert tree[0] == {
        'keyword': 'kw',
        'parameters': {'id': 1, 'title': 'foo'},
        'values': ['bar', 34]
    }


def test_parsing_consecutive_expressions_with_sub_expressions():
    tree = eval('(x "foo") (y (a 42))')
    assert tree[0] == {
        'keyword': 'x',
        'parameters': {},
        'values': ['foo']
    }
    assert tree[1] == {
        'keyword': 'y',
        'parameters': {},
        'values': [{'keyword': 'a', 'parameters': {}, 'values': [42]}]
    }


def test_parsing_expression_with_a_list_as_child():
    tree = eval('(opts [3 foo.bar "str"])')
    assert tree[0] == {
        'keyword': 'opts',
        'parameters': {},
        'values': [[3, ['foo', 'bar'], "str"]]
    }


def test_non_terminated_expression_raises_error():
    with pytest.raises(UnexpectedTokenError):
        eval('(test 4')


def test_file_node_value_is_file_content(temporary_file):
    content = 'foobar 123'
    with temporary_file(content) as file:
        tree = eval('< "{}"'.format(file.name))
        assert tree[0] == content


def test_missing_file_parsing():
    with pytest.raises(FileError):
        eval('< "this_file_is_missing.jpg"')


def test_reading_environment_variable():
    os.environ['SAMPLE_VAR'] = 'sample_value'
    tree = eval('(foo $ SAMPLE_VAR)')
    assert tree[0] == {
        'keyword': 'foo',
        'parameters': {},
        'values': ['sample_value']
    }
    del os.environ['SAMPLE_VAR']


def test_reading_undefined_environment_variable():
    tree = eval('(foo $ NON_VAR)')
    assert tree[0] == {
        'keyword': 'foo',
        'parameters': {},
        'values': ['']
    }
