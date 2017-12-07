import pytest
from dale.types import tokens
from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.types.errors import ParsingError


def create_tree(text):
    stream = TokenStream(text, tokens.rules)
    return Parser(stream).parse()


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
    #("@ '/foo/bar'", '/foo/bar'),
    #('@ "/foo/\nbar"', '/foo/\nbar'),
    ('foo.bar', ['foo', 'bar']),
    ('foo .\n bar', ['foo', 'bar'])
])
def test_parsing_single_values(test_input, expected):
    tree = create_tree(test_input)
    assert tree.value == expected


@pytest.mark.parametrize('test_input, expected', [
    ('56.75', '56.75'),
    ('-0.75', '-0.75'),
    ('[11, -0.75]', '[11, -0.75]'),
    ('true', 'true'),
    ('"string"', '"string"'),
    ('@ "/tree/data"', '@ "/tree/data"'),
    ('(foo 321 x.y)', '(foo 321 x.y)'),
    ('(foo :id 4 "data")', '(foo :id 4 "data")'),
])
def test_tree_repr(test_input, expected):
    tree = create_tree(test_input)
    assert repr(tree) == expected


def test_list_parsing():
    tree = create_tree('[1, 2.3, 3, foo.bar "str" ]')
    assert tree.value == [1, 2.3, 3, ['foo', 'bar'], "str"]


def test_EOF_while_parsing_list():
    with pytest.raises(ParsingError):
        create_tree('[1, 2.3, 3, ')


def test_EOF_while_parsing_reference():
    with pytest.raises(ParsingError):
        create_tree('foo.bar.')


def test_parsing_simple_expression():
    tree = create_tree('(name :id 1 "foo")')
    assert tree.value == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': ['foo']
    }


@pytest.mark.skip
def test_parsing_expression_with_named_ending():
    tree = create_tree('(name :id 1 "foo")name)')
    assert tree.value == {
        'keyword': 'name',
        'parameters': {'id': 1},
        'values': ['foo']
    }


def test_parsing_expression_with_wrong_ending_keyword():
    with pytest.raises(ParsingError):
        create_tree('(start  \t "foo")end)')


def test_parameters_parsing_using_comma_as_separator():
    tree = create_tree('(x :a 1, :b 2, :c 3, "foo-bar")')
    assert tree.value == {
        'keyword': 'x',
        'parameters': {'a': 1, 'b': 2, 'c': 3},
        'values': ['foo-bar']
    }


def test_parsing_expression_with_multiple_children():
    tree = create_tree(r'(kw :id 1, :title "foo" "bar" 34)')
    assert tree.value == {
        'keyword': 'kw',
        'parameters': {'id': 1, 'title': 'foo'},
        'values': ['bar', 34]
    }


def test_parsing_consecutive_expressions_with_sub_expressions():
    tree = create_tree(r'(x "foo") (y (a 42))')
    assert tree[0].value == {'keyword': 'x', 'values': ['foo']}
    assert tree[1].value == {
        'keyword': 'y', 'values': [
            {'keyword': 'a', 'values': [42]}
        ]
    }


def test_parsing_expression_with_a_list_as_child():
    tree = create_tree('(opts [3 foo.bar "str"])')
    assert tree.value == {
        'keyword': 'opts',
        'values': [[3, ['foo', 'bar'], "str"]]
    }


def test_non_terminated_expression_raises_error():
    with pytest.raises(ParsingError):
        create_tree('(test 4')


@pytest.mark.skip
def test_file_node_value_is_file_content(temporary_file):
    content = 'foobar 123'
    with temporary_file(content) as file:
        tree = create_tree('@ file "{}"'.format(file.name))
        assert tree.value == content
