import pytest

from dale import parsing
from dale import nodes

from dale.lexing import TokenStream
from dale.exceptions import KeywordNotFoundError


def create_parser(text, Parser=parsing.Parser):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text):
    return create_parser(text).parse()


def parse_one(text):
    return create_parser(text).parse()[0]


#  BASE PARSER

# def test_parser_empty_input():
#     parser = create_parser("")
#     assert parser.parse()


# OBJECT ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        ("'etc'"),
        ('"abc"'),
        ('[1, -2.3, True]'),
    ]
)
def test_subparser_object(test_input):
    parser = create_parser(test_input, parsing.ObjectParser)
    assert parser.parse()


#  LIST ======================================================

def test_subparser_empty_list():
    parser = create_parser("[]", parsing.ListParser)
    assert parser.parse().id == nodes.ListNode.id


def test_subparser_literal_list():
    parser = create_parser("[1, 2]", parsing.ListParser)
    assert parser.parse().id == nodes.ListNode.id


def test_list_size():
    parser = create_parser("[1, 2, 'abc']", parsing.ListParser)
    assert len(parser.parse()) == 3


def test_subparser_nested_list():
    parser = create_parser("[[], [1, 2]]", parsing.ListParser)
    node = parser.parse()
    assert node[0].id == nodes.ListNode.id
    assert node[1].id == nodes.ListNode.id


# METADATA ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        "!abc",
        "a = 3",
        "a/b >= 3",
        "a/b <= 5.5",
        "a.b > 102",
        "foo.bar < 'a'",
        "a.b/c != 'foo'"
    ]
)
def test_subparser_metadata(test_input):
    parser = create_parser(test_input, parsing.MetadataParser)
    assert parser.parse()


#  PATH PARSER =================================================

def test_path_single_keyword():
    parser = create_parser("foo", parsing.PathParser)
    assert parser.parse()


@pytest.mark.parametrize(
    "test_input, total",
    [
        ("foo", 1),
        ("Bar", 1),
        ("foo/#bar", 2),
        ("Foo/bar/?baz", 3),
        ("foo.Bar.%baz", 3),
        ("Foo/Etc.$bar/baz", 4)
    ]
)
def test_path_length(test_input, total):
    parser = create_parser(test_input, parsing.PathParser)
    node = parser.parse()
    assert len(node) == total


@pytest.mark.parametrize(
    "test_input, refNode",
    [
        ("foo", nodes.NameNode),
        ("Bar", nodes.ReservedNameNode),
        ("#code", nodes.UIDNode),
        ("$code", nodes.VariableNode),
        ("%code", nodes.FormatNode),
        ("?code", nodes.DocNode)
    ]
)
def test_path_single_node_ids(test_input, refNode):
    parser = create_parser(test_input, parsing.PathParser)
    node = parser.parse()
    assert node[0].id == refNode.id


@pytest.mark.parametrize(
    "test_input",
    [
        "foo/",
        "Foo.",
        "%foo.a/",
        "$etc/#bar.tsc.",
    ]
)
def test_path_keyword_not_found(test_input):
    parser = create_parser(test_input, parsing.PathParser)
    with pytest.raises(KeywordNotFoundError):
        parser.parse()


#  KEYWORD ======================================================

def test_subparser_keyword():
    parser = create_parser("foo", parsing.KeywordParser)
    assert parser.subparse(nodes.NameNode)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("foo", "foo"),
        ("Foo", "Foo"),
        ("#foo", "foo"),
        ("$foo", "foo"),
        ("%foo", "foo"),
        ("?foo", "foo"),
    ]
)
def test_keyword_acceptance(test_input, expected):
    parser = create_parser(test_input, parsing.KeywordParser)
    node = parser.parse()
    assert node.value == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "2",
        "-3",
        "'abc'",
        "(a 2)",
        "{b 5.7}",
        "[1 2]"
    ]
)
def test_keyword_non_acceptance(test_input):
    parser = create_parser(test_input, parsing.KeywordParser)
    assert parser.parse() is None


#  KEYWORD SUB PARSERS ====================================

@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("foo", parsing.NameParser),
        ("_bar", parsing.NameParser),
        ("Foo", parsing.ReservedNameParser),
        ("#foo", parsing.UIDParser),
        ("$foo", parsing.VariableParser),
        ("%foo", parsing.FormatParser),
        ("?foo", parsing.DocParser)
    ]
)
def test_keyword_subparsers(test_input, parser):
    parser = create_parser(test_input, parser)
    assert parser.parse() is not None


#  LITERAL =================================================

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2", 2),
        ("4.7e3", 4.7e3),
        ("'foo'", 'foo'),
        ("true", True),
        ("True", True),
        ("false", False),
        ("False", False)
    ]
)
def test_literal_acceptance(test_input, expected):
    parser = create_parser(test_input, parsing.LiteralParser)
    node = parser.parse()
    assert node.value == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "aa",
        "{a}",
        "[1, 2]",
        "(a 1)"
    ]
)
def test_literal_non_acceptance(test_input):
    parser = create_parser(test_input, parsing.LiteralParser)
    assert parser.parse() is None


#  LITERAL SUB PARSERS ====================================

@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("3", parsing.IntParser),
        ("-3.44", parsing.FloatParser),
        ('" aaa "', parsing.StringParser),
        ("'foo'", parsing.StringParser),
        ("true", parsing.BooleanParser),
        ("False", parsing.BooleanParser),

    ]
)
def test_literal_subparsers(test_input, parser):
    parser = create_parser(test_input, parser)
    assert parser.parse() is not None


# #  NODE INDEX TESTS


# def test_node_children_index():
#     node = parse("44 12")
#     assert node[0].index == (0, 2)
#     assert node[1].index == (3, 5)


# def test_list_index():
#     node = parse("[1, 2]")
#     assert node.index == (0, 6)


# def test_scope_index():
#     scope = parse("(a 2)")
#     assert scope.index == (0, 5)


# #  REPR TESTS


# def test_whitespace_only():
#     node = parse("   ,,,\n ; , ;, \t ")
#     assert node.id == "root"
#     assert len(node) == 0


# def test_empty_input_string():
#     node = parse("")
#     assert node.id == "root"
#     assert len(node) == 0


# @pytest.mark.parametrize(
#     "test_input",
#     [
#         ("56.75 (a b)"),
#         ("!flag -0.75"),
#         ("#id -.099999"),
#         ("-0.75e10/55 etc"),
#         ("1.45e-10"),
#         ("true  false"),
#         ('"string"'),
#         ("'string'"),
#         ("name 2"),
#         ('?foo "test"'),
#     ],
# )
# def test_string_representation(test_input):
#     tree = parse(test_input)
#     assert str(tree) == test_input


# @pytest.mark.parametrize(
#     "test_input, expected",
#     [
#         ("-215", "INT('-215')"),
#         ("56.75", "FLOAT('56.75')"),
#         ("#id", "UID('#id')"),
#         ("$path", "VARIABLE('$path')"),
#         ("(bar 42)", "SCOPE('(bar 42)')"),
#         ('[bar "etc"]', "LIST('[bar \"etc\"]')"),
#     ],
# )
# def test_object_representation(test_input, expected):
#     node = parse_one(test_input)
#     assert repr(node) == expected


# #  SCOPE TESTS


# def test_empty_scope():
#     node = parse_one("()")
#     assert not node.key
#     assert len(node) == 0


# def test_scope_with_key_and_no_value():
#     node = parse_one("(a)")
#     assert str(node.key) == "a"
#     assert len(node) == 0


# def test_scope_key_assumes_first_value():
#     node = parse_one("(foo 42)")
#     assert str(node.key) == "foo"


# def test_scope_with_many_values():
#     node = parse_one("(a (b 2) 4 'etc')")
#     assert str(node[0]) == "(b 2)"
#     assert str(node[1]) == "4"
#     assert str(node[2]) == "'etc'"


# def test_scope_key_with_doc():
#     node = parse_one("(bar (?help 'foo'))")
#     assert node.props["doc"]["help"][0].value == "foo"


# def test_scope_key_with_multi_properties():
#     node = parse_one("(foo (%bar 2) (#id 48764))")
#     assert str(node.props["format"]["bar"]) == "(%bar 2)"
#     assert str(node.props["uid"]["id"]) == "(#id 48764)"


# def test_scope_child_values():
#     node = parse_one("(foo (#bar 2, 4))")
#     uid = node.props["uid"]["bar"]
#     assert str(uid[0]) == "2"
#     assert str(uid[1]) == "4"


# def test_unclosed_scope_raises_error():
#     with pytest.raises(UnexpectedEOFError):
#         parse("(")


# def test_scope_flag_property():
#     node = parse_one("(foo !active)")
#     assert str(node.props["flag"]["active"]) == "!active"


# def test_scope_uid_property():
#     node = parse_one("(foo (#id 22))")
#     assert str(node.props["uid"]["id"]) == "(#id 22)"


# def test_scope_properties():
#     text = """
#     (object
#         (#answer_code 42)
#         ($ref {!active})
#         (?help "A object")
#         (%short child)
#     )
#     """
#     node = parse_one(text)
#     attrs = node.props
#     assert str(attrs["uid"]["answer_code"]) == "(#answer_code 42)"
#     assert str(attrs["doc"]["help"]) == '(?help "A object")'
#     assert str(attrs["variable"]["ref"]) == "($ref {!active})"
#     assert str(attrs["format"]["short"]) == "(%short child)"


# def test_null_scope_key():
#     node = parse_one("(: 'test')")
#     assert not node.key


# def test_nested_scope_with_null_key():
#     node = parse_one("(foo (: 56.7) )")
#     assert node.id == "scope"
#     assert node.props["attribute"] == {}


# def test_scope_with_wildcard_key():
#     node = parse_one("(* abc)")
#     assert node.id == "scope"
#     assert node.key.id == "wildcard"


# #  QUERY TESTS


# def test_query_key_assumes_first_value():
#     node = parse_one("{abc 42}")
#     assert str(node.key) == "abc"
#     assert node[0].value == 42


# #  PROPERTIES TESTS


# def test_name_not_found_after_prefix():
#     with pytest.raises(NameNotFoundError):
#         parse("(# )")


# #  RANGE TESTS


# def test_range_id():
#     node = parse_one("2..4")
#     assert node.id == "range"


# def test_range_limit():
#     node = parse_one("0..-10")
#     assert node.start == 0
#     assert node.end == -10


# def test_range_without_specific_end():
#     node = parse_one("42..")
#     assert node.start == 42
#     assert node.end is None


# def test_range_without_specific_start():
#     node = parse_one("..33")
#     assert node.start is None
#     assert node.end == 33


# def test_range_must_have_at_least_one_int():
#     with pytest.raises(InfiniteRangeError):
#         parse("..")


# def test_range_only_accepts_integers():
#     with pytest.raises(InfiniteRangeError):
#         parse("3.4..")


# # RELATION TESTS


# def test_root_equal_relation_attributes():
#     root = parse("name = 'john'")
#     relation = root.props["attribute"]["name"]
#     assert relation.value.value == "john"


# def test_scope_relation_attributes():
#     node = parse_one("(person name = 'john')")
#     assert node.key.name == "person"
#     relation = node.props["attribute"]["name"]
#     assert relation.value.value == "john"
