import os

import pytest

from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser
from dale.utils.context import Context

from dale.exceptions import (
    UnexpectedTokenError,
    UnexpectedTokenValueError,
    FileError
)


def eval(text, context=Context()):
    tokens = Lexer(text).tokenize()
    stream = TokenStream(tokens)
    tree = Parser(stream).parse()
    context.var('tree', tree)
    return tree.eval(context)


def test_list_parsing():
    output = eval('(a 5) [1, 2.3, true, a "str" ]')
    assert output[1] == [1, 2.3, True, 5, "str"]


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
    assert output == 'foo'


def test_parsing_expression_with_named_ending():
    output = eval('(name :id 1 "foo" ) name )')
    assert output == 'foo'


def test_parsing_expression_with_wrong_ending_name():
    with pytest.raises(UnexpectedTokenValueError):
        eval('(start  \t "foo")end)')


def test_attributes_parsing_using_comma_as_separator():
    output = eval('(x :a 1, :b 2, :c 3, "foo-bar")')
    assert output == 'foo-bar'


def test_parsing_expression_with_multiple_children():
    output = eval('(kw :id 1, :title "foo" "bar" 34)')
    assert output == ['bar', 34]


def test_parsing_consecutive_expressions_with_sub_expressions():
    output = eval('(x "foo") (y (a 42))')
    assert output[0] == 'foo'
    assert output[1] == 42


def test_parsing_expression_with_a_list_as_child():
    output = eval('(x (y 6)) (opts [3 x.y "str"])')
    assert output[1] == [3, 6, "str"]


def test_non_terminated_expression_raises_error():
    with pytest.raises(UnexpectedTokenError):
        eval('(test 4')


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
    assert output == 'sample_value'
    del os.environ['SAMPLE_VAR']


def test_reading_undefined_environment_variable():
    output = eval('(foo $ NON_VAR)')
    assert output == ''
