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


def eval(text, context=Context()):
    stream = TokenStream(text)
    tree = Parser(stream).parse()
    context.var('tree', tree)
    return tree.eval(context)


def test_list_parsing():
    output = eval('(a 5) [1, 2.3, true, a "str" ]')
    a = {
        'name': 'a',
        'attributes': {},
        'references': {},
        'values': [5]
    }
    assert output[1] == [1, 2.3, True, a, "str"]


def test_EOF_while_parsing_list():
    with pytest.raises(UnexpectedTokenError):
        eval('[1, 2.3, 3, ')


def test_lists_cant_have_expression_subnodes():
    with pytest.raises(UnexpectedTokenError):
        eval('[(a 3)]')


def test_parsing_unexpected_value_node():
    with pytest.raises(UnexpectedTokenError):
        eval('(x :a :b)')


def test_EOF_while_parsing_reference():
    with pytest.raises(UnexpectedTokenError):
        eval('foo.bar.')


def test_parsing_simple_expression():
    output = eval('(name :id 1 "foo")')
    assert output == {
        'name': 'name',
        'attributes': {'id': 1},
        'references': {},
        'values': ['foo']
    }


def test_parsing_expression_with_named_ending():
    output = eval('(object :id 1 "foo" 3 ) object)')
    assert output == {
        'name': 'object',
        'attributes': {'id': 1},
        'references': {},
        'values': ['foo', 3]
    }


def test_parsing_expression_with_wrong_ending_name():
    with pytest.raises(UnexpectedTokenValueError):
        eval('(start  \t "foo")end)')


def test_attributes_parsing_using_comma_as_separator():
    output = eval('(x :a 1, :b 2, :c 3, "foo-bar")')
    assert output == {
        'name': 'x',
        'attributes': {'a': 1, 'b': 2, 'c': 3},
        'references': {},
        'values': ['foo-bar']
    }


def test_parsing_expression_with_multiple_children():
    output = eval('(kw :id 1, :title "foo" "bar" 34)')
    assert output == {
        'name': 'kw',
        'attributes': {'id': 1, 'title': 'foo'},
        'references': {},
        'values': ['bar', 34]
    }


def test_parsing_consecutive_expressions_with_sub_expressions():
    output = eval('(x "foo") (y (a 42))')
    a = {'name': 'a', 'attributes': {}, 'references': {}, 'values': [42]}
    assert output[0] == {
        'name': 'x',
        'attributes': {},
        'references': {},
        'values': ['foo']
    }
    assert output[1] == {
        'name': 'y',
        'attributes': {},
        'references': {'a': a},
        'values': [a]
    }


def test_parsing_expression_attributes():
    output = eval('(person :id -6.45 :show true)')
    assert output == {
        'name': 'person',
        'attributes': {'id': -6.45, 'show': True},
        'references': {},
        'values': []
    }


def test_parsing_expression_with_a_list_as_child():
    output = eval('(x (y 6)) (opts [4 x.y "foo"])')
    assert output[1] == {
        'name': 'opts',
        'attributes': {},
        'references': {},
        'values': [[4, {
            'name': 'y',
            'attributes': {},
            'references': {},
            'values': [6]
        }, 'foo']]
    }


def test_non_terminated_expression_raises_error():
    with pytest.raises(UnexpectedTokenError):
        eval('(test 4')


def test_unknown_single_reference():
    with pytest.raises(UnknownReferenceError):
        eval('(test x)')


def test_unknown_chained_reference():
    with pytest.raises(UnknownReferenceError):
        eval('(x 2) (test x.y)')


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
    output = eval('(foo $ SAMPLE_VAR)')
    assert output == {
        'name': 'foo',
        'attributes': {},
        'references': {},
        'values': ['sample_value']
    }
    del os.environ['SAMPLE_VAR']


def test_reading_undefined_environment_variable():
    output = eval('(foo $ NON_VAR)')
    assert output == {
        'name': 'foo',
        'attributes': {},
        'references': {},
        'values': ['']
    }
