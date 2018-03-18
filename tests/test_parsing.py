import os

import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context

from dale.exceptions import (
    UnexpectedTokenError,
    UnexpectedTokenValueError,
    UnknownReferenceError,
    FileError
)


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context=Context()):
    tree = create_tree(text)
    context.tree = tree
    return tree.eval(context)


def test_list_parsing():
    output = eval('{a 5} [1, 2.3, true, a "str" ]')
    a = {
        'name': 'a',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': [5]
    }
    assert output[1] == [1, 2.3, True, a, "str"]


def test_EOF_while_parsing_list():
    with pytest.raises(UnexpectedTokenError):
        eval('[1, 2.3, 3, ')


def test_lists_cant_have_scope_values():
    with pytest.raises(UnexpectedTokenError):
        eval('[{a 3}]')


def test_parsing_unexpected_value_node():
    with pytest.raises(UnexpectedTokenError):
        eval('{x :a :b}')


def test_EOF_while_parsing_reference():
    with pytest.raises(UnexpectedTokenError):
        eval('foo.bar.')


def test_parsing_simple_scope():
    output = eval('{name :id 1 "foo"}')
    assert output == {
        'name': 'name',
        'flags': [],
        'attrs': {'id': 1},
        'refs': {},
        'values': ['foo']
    }


def test_parsing_scope_with_named_ending():
    output = eval('{object :id 1 "foo" 3 } object}')
    assert output == {
        'name': 'object',
        'flags': [],
        'attrs': {'id': 1},
        'refs': {},
        'values': ['foo', 3]
    }


def test_parsing_scope_with_wrong_ending_name():
    with pytest.raises(UnexpectedTokenValueError):
        eval('{start  \t "foo"}end}')


def test_attributes_parsing_using_comma_as_separator():
    output = eval('{x :a 1, :b 2, :c 3, "foo-bar"}')
    assert output == {
        'name': 'x',
        'flags': [],
        'attrs': {'a': 1, 'b': 2, 'c': 3},
        'refs': {},
        'values': ['foo-bar']
    }


def test_parsing_scope_with_multiple_children():
    output = eval('{kw :id 1, :title "foo" "bar" 34}')
    assert output == {
        'name': 'kw',
        'flags': [],
        'attrs': {'id': 1, 'title': 'foo'},
        'refs': {},
        'values': ['bar', 34]
    }


def test_parsing_consecutive_scopes_with_sub_scopes():
    output = eval('{x "foo"} {y {a 42}}')
    a = {
        'name': 'a',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': [42]
    }
    assert output[0] == {
        'name': 'x',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': ['foo']
    }
    assert output[1] == {
        'name': 'y',
        'attrs': {},
        'flags': [],
        'refs': {'a': a},
        'values': [a]
    }


def test_parsing_scope_identifiers_and_attributes():
    output = eval('{person :id 45 :weight 63.5 :show true}')
    assert output == {
        'name': 'person',
        'flags': [],
        'attrs': {'id': 45, 'weight': 63.5, 'show': True},
        'refs': {},
        'values': []
    }


def test_parsing_scope_flags():
    output = eval('{person !active}')
    assert output['name'] == 'person'
    assert 'active' in output['flags']


def test_parsing_multi_scope_flags():
    output = eval('{person !active !woman}')
    assert output['name'] == 'person'
    assert 'active' in output['flags']


def test_parsing_scope_with_a_list_as_child():
    output = eval('{x {y 6}} {opts [4 x.y "foo"]}')
    assert output[1] == {
        'name': 'opts',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': [[4, {
            'name': 'y',
            'attrs': {},
            'flags': [],
            'refs': {},
            'values': [6]
        }, 'foo']]
    }


def test_non_terminated_scope_raises_error():
    with pytest.raises(UnexpectedTokenError):
        eval('{test 4')


def test_unknown_single_reference():
    with pytest.raises(UnknownReferenceError):
        eval('{test x}')


def test_unknown_chained_reference():
    with pytest.raises(UnknownReferenceError):
        eval('{x 2} {test x.y}')


def test_file_node_value_is_file_content(temporary_file):
    content = 'foobar 123'
    with temporary_file(content) as file:
        output = eval('< "{}"'.format(file.name))
        assert output == content


def test_missing_file_parsing():
    with pytest.raises(FileError):
        eval('< "this_file_is_missing.jpg"')


def test_reading_environment_variable():
    os.environ['SAMPLE_VAR'] = 'sample_value'
    output = eval('{foo $ SAMPLE_VAR}')
    assert output == {
        'name': 'foo',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': ['sample_value']
    }
    del os.environ['SAMPLE_VAR']


def test_reading_undefined_environment_variable():
    output = eval('{foo $ NON_VAR}')
    assert output == {
        'name': 'foo',
        'attrs': {},
        'flags': [],
        'refs': {},
        'values': ['']
    }


def test_value_node_repr_with_sub_scopes():
    output = create_tree('"string"')
    assert repr(output[0]) == '"string"'


def test_scope_node_repr_returns_original_code():
    output = create_tree('{foo "bar" 3 5}')
    assert repr(output) == '{foo "bar" 3 5}'


def test_node_repr_with_sub_scopes():
    output = create_tree('{bar "example" {sub 20}}')
    assert repr(output[0]['sub']) == '{sub 20}'


def test_node_repr_with_file_value():
    output = create_tree('{file < "example.txt"}')
    assert repr(output['file'][0]) == '< "example.txt"'
