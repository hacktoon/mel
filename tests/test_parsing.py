import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context
from dale.exceptions import (
    SubNodeError,
    UnexpectedTokenError,
)


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
    node = create_tree("")
    assert node.id == "root"


def test_node_children_index():
    node = create_tree("44 12")
    assert node[0].index == (0, 2)
    assert node[1].index == (3, 5)


def test_list_index():
    _list = create_tree("[1, 2]")
    assert _list.index == (0, 6)


def test_scope_index():
    scope = create_tree("(a 2)")
    assert scope.index == (0, 5)


@pytest.mark.parametrize(
    "test_input",
    [
        ("56.75 (a b)"),
        ("!flag -0.75"),
        ("#id -.099999"),
        ("-0.75e10/55 etc"),
        ("+1.45e-10"),
        ("true  false"),
        ('"string"'),
        ("'string'"),
        ("name 2"),
        ('?foo "test"'),
    ],
)
def test_string_representation(test_input):
    tree = create_tree(test_input)
    assert str(tree) == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("-215", "INT('-215')"),
        ("56.75", "FLOAT('56.75')"),
        ("#id", "UID('#id')"),
        ("$path", "VARIABLE('$path')"),
        ("(bar 42)", "SCOPE('(bar 42)')"),
        ('[bar "etc"]', "LIST('[bar \"etc\"]')"),
    ],
)
def test_object_representation(test_input, expected):
    tree = create_tree(test_input)
    assert repr(tree[0]) == expected


#  LIST TESTS


def test_empty_list():
    parser = create_parser("[]")
    node = parser.parse_list()
    assert len(node) == 0


def test_one_sized_list_node_always_returns_list():
    parser = create_parser("[3]")
    node = parser.parse_list()
    assert node.id == "list"


#  SUBNODE TESTS


def test_path_creates_subnode():
    parser = create_parser("abc/$def")
    _object = parser.parse_object()
    assert _object.id == "name"
    assert _object[0].id == "variable"


def test_bigger_subnode_path():
    parser = create_parser("abc/$def/#pid/!active")
    _object = parser.parse_object()
    assert _object.id == "name"
    assert _object[0].id == "variable"
    assert _object[0][0].id == "uid"
    assert _object[0][0][0].id == "flag"


def test_unexpected_finished_chained_value_error():
    with pytest.raises(SubNodeError):
        create_tree("name/")


def test_unexpected_separator_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree("/")


#  SCOPE TESTS


def test_scope_key_assumes_first_value():
    parser = create_parser("(foo 42)")
    node = parser.parse_scope()
    assert str(node.key) == "foo"


def test_empty_scope():
    parser = create_parser("()")
    node = parser.parse_scope()
    assert not node.key
    assert len(node) == 0


def test_scope_children():
    parser = create_parser("(a (b 2) 4 'etc')")
    node = parser.parse_scope()
    assert str(node[0]) == "(b 2)"
    assert str(node[1]) == "4"
    assert str(node[2]) == "'etc'"


def test_scope_key_with_attribute():
    parser = create_parser("(a (@b 2))")
    node = parser.parse_scope()
    assert str(node.attributes["attribute"]["b"]) == "(@b 2)"


def test_scope_key_with_doc():
    parser = create_parser("(bar (?help 'foo'))")
    node = parser.parse_scope()
    assert node.attributes["doc"]["help"][0].value == "foo"


def test_scope_key_with_multi_properties():
    parser = create_parser("(foo (%bar 2) (#id 48764))")
    node = parser.parse_scope()
    assert str(node.attributes["format"]["bar"]) == "(%bar 2)"
    assert str(node.attributes["uid"]["id"]) == "(#id 48764)"


def test_scope_child_values():
    parser = create_parser("(foo (@bar 2, 4))")
    node = parser.parse_scope()
    property = node.attributes["attribute"]["bar"]
    assert str(property[0]) == "2"
    assert str(property[1]) == "4"


def test_unclosed_scope_raises_error():
    with pytest.raises(UnexpectedTokenError):
        create_tree("(")


def test_scope_flag_property():
    parser = create_parser("(foo !active)")
    node = parser.parse_scope()
    assert str(node.attributes["flag"]["active"]) == "!active"


def test_scope_uid_property():
    parser = create_parser("(foo (#id 22))")
    node = parser.parse_scope()
    assert str(node.attributes["uid"]["id"]) == "(#id 22)"


def test_scope_properties():
    text = """
    (object
        (#answer_code 42)
        ($ref {!active})
        (?help "A object")
        (@child {bar 2})
        (%short child)
    )
    """
    parser = create_parser(text)
    node = parser.parse_scope()
    attrs = node.attributes
    assert str(attrs["uid"]["answer_code"]) == "(#answer_code 42)"
    assert str(attrs["attribute"]["child"]) == "(@child {bar 2})"
    assert str(attrs["doc"]["help"]) == '(?help "A object")'
    assert str(attrs["variable"]["ref"]) == "($ref {!active})"


def test_null_scope_key():
    parser = create_parser("(: 'test')")
    node = parser.parse_scope()
    assert not node.key


def test_nested_scope_with_null_key():
    parser = create_parser("(foo (: 56.7) )")
    node = parser.parse_scope()
    assert node[0].id == "scope"
    assert node.attributes["attribute"] == {}


def test_scope_with_wildcard_key():
    parser = create_parser("(* abc)")
    node = parser.parse_scope()
    assert node.id == "scope"
    assert node.key.id == "wildcard"


#  QUERY TESTS


def test_query_key_assumes_first_value():
    parser = create_parser("{abc 42}")
    node = parser.parse_query()
    assert str(node.key) == "abc"


#  ATTRIBUTE TESTS


def test_name_not_found_after_prefix():
    with pytest.raises(UnexpectedTokenError):
        create_tree("(# )")


#  RANGE TESTS


def test_range_type():
    parser = create_parser("2..4")
    node = parser.parse_range()
    assert node.id == "range"


def test_range_limit():
    parser = create_parser("0..10")
    node = parser.parse_range()
    assert node[0] == 0
    assert node[1] == 10


def test_range_without_specific_end():
    parser = create_parser("42..")
    node = parser.parse_range()
    assert node[0] == 42
    assert node[1] is None


def test_range_without_specific_start():
    parser = create_parser("..33")
    node = parser.parse_range()
    assert node[0] is None
    assert node[1] == 33


def test_range_must_have_at_least_one_int():
    with pytest.raises(UnexpectedTokenError):
        create_tree("..")


def test_range_only_accepts_integers():
    parser = create_parser("3.4..")
    node = parser.parse_float()
    assert node.value == 3.4
    with pytest.raises(UnexpectedTokenError):
        parser.parse_range()
