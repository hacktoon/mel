import pytest
from dale.parser import Parser
from dale.token import TokenType
from dale.error import SyntaxError, ParserError


def test_value_rule_for_float_token():
    tree = Parser('56.72 ').parse()
    assert tree.children[0] == 'FLOAT(56.72)'


def test_value_parsing_as_identifier():
    tree = Parser(r'name ').parse()
    assert tree.children[0] == 'IDENTIFIER(name)'


def test_value_parsing_as_string():
    tree = Parser(r'"foo"').parse()
    assert tree.children[0] == 'STRING(foo)'


def test_tree_children_with_multiple_values():
    tree = Parser(r'identifier "str" 3').parse()
    assert len(tree.children) == 3


def test_list_parsing():
    tree = Parser(r'[1, 2, 3]').parse()
    items = tree.children[0].children
    assert items[0] == 'INT(1)'
    assert items[1] == 'INT(2)'
    assert items[2] == 'INT(3)'


def test_list_specific_node_parsing():
    tree = Parser(r'[1, true, {{/site/title}}, name]').parse()
    items = tree.children[0].children
    assert items[0] == 'INT(1)'
    assert items[1] == 'BOOLEAN(True)'
    assert items[2] == 'QUERY(/site/title)'
    assert items[3] == 'IDENTIFIER(name)'


def test_list_specific_node_parsing_with_different_items():
    tree = Parser(r'[1, [2, 3.34], "foo"]').parse()
    items = tree.children[0].children
    assert items[0] == 'INT(1)'
    assert items[1] == 'LIST([INT(2), FLOAT(3.34)])'
    assert items[2] == 'STRING(foo)'


def test_parsing_invalid_syntax_list():
    with pytest.raises(ParserError):
        Parser(r'[1, 2 3]').parse()


def test_parsing_non_terminated_list():
    with pytest.raises(ParserError):
        Parser(r'[1, 2, 5').parse()


def test_parsing_list_with_duplicated_commas():
    with pytest.raises(ParserError):
        Parser(r'[1, 2,, 3]').parse()


def test_parameter_list_parsing():
    tree = Parser(r'(x {a:1, b:2, c:3})').parse()
    items = tree.children[0].parameter_list.children
    assert items[0] == 'PARAMETER(IDENTIFIER(a):INT(1))'
    assert items[1] == 'PARAMETER(IDENTIFIER(b):INT(2))'
    assert items[2] == 'PARAMETER(IDENTIFIER(c):INT(3))'


def test_parsing_parameter_list_without_comma():
    with pytest.raises(ParserError):
        Parser(r'{a:1, b:2 c:3}').parse()


def test_parsing_parameter_list_without_colon():
    with pytest.raises(ParserError):
        Parser(r'{a:1, b 2, c:3}').parse()


def test_parsing_parameter_list_with_duplicated_commas():
    with pytest.raises(ParserError):
        Parser(r'{a:1, b 2,, c:3}').parse()


def test_simple_expression_parsing():
    tree = Parser(r'(name {id:1} "foo")').parse()
    exp = tree.children[0]
    parameter_list = 'PARAMETERLIST(PARAMETER(IDENTIFIER(id):INT(1)))'
    assert exp.identifier == 'IDENTIFIER(name)'
    assert exp.parameter_list == parameter_list
    assert exp.children == 'STRING(foo)'


def test_parsing_expression_with_multiple_children():
    tree = Parser(r'(x {id:1, title:"foo"} "bar" 34)').parse()
    exp = tree.children[0]
    assert exp.identifier == 'IDENTIFIER(x)'
    parameter_list = (
        'PARAMETERLIST(PARAMETER(IDENTIFIER(id):INT(1)), '
        'PARAMETER(IDENTIFIER(title):STRING(foo)))'
    )
    assert exp.parameter_list == parameter_list
    assert exp.children == 'STRING(bar) INT(34)'


def test_parsing_expression_with_parameters_and_query():
    tree = Parser(r'(etc {id:1} {{/foo/bar}})').parse()
    exp = tree.children[0]
    assert exp.identifier == 'IDENTIFIER(etc)'
    assert exp.children == 'QUERY(/foo/bar)'


def test_parsing_expression_with_sub_expressions():
    tree = Parser(r'(foo-bar (bar 34))').parse()
    exp = tree.children[0]
    assert exp.identifier == 'IDENTIFIER(foo-bar)'
    assert exp.parameter_list == 'PARAMETERLIST()'
    inner_exp = 'EXPRESSION(IDENTIFIER(bar) PARAMETERLIST() INT(34))'
    assert exp.children == inner_exp


def test_parsing_consecutive_expressions():
    tree = Parser(r'(x "foo") (y (a 42))').parse()
    first_exp = 'EXPRESSION(IDENTIFIER(x) PARAMETERLIST() STRING(foo))'
    inner = 'EXPRESSION(IDENTIFIER(a) PARAMETERLIST() INT(42))'
    second_exp = 'EXPRESSION(IDENTIFIER(y) PARAMETERLIST() {})'.format(inner)
    assert tree == '{} {}'.format(first_exp, second_exp)


def test_non_terminated_expression_raises_error():
    with pytest.raises(ParserError):
        Parser(r'(test 4').parse()
