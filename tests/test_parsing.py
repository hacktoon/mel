import pytest

from dale import parsing
from dale import nodes

from dale.lexing import TokenStream
from dale.exceptions import (
    UnexpectedTokenError,
    UnexpectedEOFError,
    KeywordNotFoundError,
    KeyNotFoundError,
    NameNotFoundError,
    InfiniteRangeError,
    UnexpectedKeywordError
)


def create_parser(text, Parser=parsing.Parser):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text, Parser=parsing.Parser):
    return create_parser(text, Parser).parse()


def parse_one(text):
    return create_parser(text).parse()[0]


# BASE PARSER ===========================================

def test_empty_input_string():
    node = parse("")
    assert node.id == nodes.RootNode.id
    assert len(node) == 0


def test_whitespace_only():
    node = parse("   ,,,\n ; , ;, \t ")
    assert node.id == "root"
    assert len(node) == 0


@pytest.mark.parametrize(
    "test_input",
    [
        ("56.75 (a 3)"),
        ("#checked -0.75"),
        ("True  False"),
        ("1.45e-10"),
        ('"string"'),
        ("'string'"),
        ("#id -0.099999"),
        ("-0.75e10 etc"),
        ("name 2"),
        ('?foo "test"')
    ],
)
def test_string_representation(test_input):
    tree = parse(test_input)
    assert str(tree) == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("-215", "INT('-215')"),
        ("56.75", "FLOAT('56.75')"),
        ("id", "REFERENCE('id')"),
        ("@path", "REFERENCE('@path')"),
        ("(bar 42)", "SCOPE('(bar 42)')"),
        ('[bar "etc"]', "LIST('[bar \"etc\"]')")
    ],
)
def test_node_representation(test_input, expected):
    node = parse_one(test_input)
    assert repr(node) == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "[etc",
        "[2, 6",
        "(a ",
        "{a x=2",
        "{a x=2 [55, 'foo' ",
    ]
)
def test_incomplete_input_EOF(test_input):
    parser = create_parser(test_input)
    with pytest.raises(UnexpectedEOFError):
        parser.parse()


# NODE INDEX ===========================================

def test_node_children_index():
    node = parse("44 12")
    assert node[0].index == (0, 2)
    assert node[1].index == (3, 5)


def test_list_index():
    node = parse("[1, 2]")
    assert node.index == (0, 6)


def test_scope_index():
    scope = parse("(a 2)")
    assert scope.index == (0, 5)


# EXPRESSION =================================================

@pytest.mark.parametrize(
    "test_input, refnode",
    [
        ("#foo", nodes.TagNode),
        ("x = 3", nodes.RelationNode),
        ("x != 3", nodes.RelationNode),
        ("44", nodes.IntNode),
        ("'foo'", nodes.StringNode),
    ]
)
def test_expression(test_input, refnode):
    node = parse(test_input, parsing.ExpressionParser)
    assert node.id == refnode.id


# TAG =================================================

@pytest.mark.parametrize(
    "test_input",
    [
        "#foo",
        "#bar_4",
        "#fA_o",
    ]
)
def test_tags(test_input):
    node = parse(test_input, parsing.TagParser)
    assert node.id == nodes.TagNode.id


# OBJECT ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        ("'etc'"),
        ('"abc"'),
        ('[1, -2.3, True]'),
        ('42'),
        ('a/b/c'),
        ('(a 3)'),
    ]
)
def test_subparser_object(test_input):
    parser = create_parser(test_input, parsing.ObjectParser)
    assert parser.parse()


# RELATION =================================================

@pytest.mark.parametrize(
    "test_input, key, symbol, value",
    [
        ("x = 4", 'x', '=', '4'),
        ("x/y != 64", 'x/y', '!=', '64'),
        ("a/pid/f_a > [1, 2]", 'a/pid/f_a', '>', '[1, 2]'),
    ]
)
def test_relation(test_input, key, symbol, value):
    node = parse(test_input, parsing.RelationParser)
    assert str(node.key) == key
    assert str(node.symbol) == symbol
    assert str(node.value) == value


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


#  REFERENCE ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        "etc",
        "bar/.name",
        'foo/#bar',
        'abc/[1 2]'
    ]
)
def test_reference_keywords(test_input):
    parser = create_parser(test_input, parsing.ReferenceParser)
    assert parser.parse()


@pytest.mark.parametrize(
    "test_input",
    [
        "etc/bar/#active",
        'foo/#bar'
    ]
)
def test_reference_tag(test_input):
    parser = create_parser(test_input, parsing.ReferenceParser)
    assert parser.parse()


@pytest.mark.parametrize(
    "test_input",
    [
        "etc/bar/#active/ge",
        'foo/#bar/ff'
    ]
)
def test_reference_non_terminal_tag_error(test_input):
    with pytest.raises(UnexpectedKeywordError):
        parse(test_input, parsing.ReferenceParser)


# PATH =================================================

@pytest.mark.parametrize(
    "test_input, total",
    [
        ("foo", 1),
        ("Bar", 1),
        ("Foo/bar/?baz", 3),
        ("foo/Bar/%baz", 3),
        ("Foo/Etc/@bar/baz", 4)
    ]
)
def test_path_length(test_input, total):
    parser = create_parser(test_input, parsing.PathParser)
    node = parser.parse()
    assert len(node) == total


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("foo", nodes.NameNode),
        ("Bar", nodes.ConceptNode),
        ("@code", nodes.AliasNode),
        ("%code", nodes.FormatNode),
        ("?code", nodes.DocNode)
    ]
)
def test_path_single_node_ids(test_input, expected):
    parser = create_parser(test_input, parsing.PathParser)
    node = parser.parse()
    assert node[0].id == expected.id


@pytest.mark.parametrize(
    "test_input",
    [
        "foo/",
        "Foo/",
        "%foo/a/",
        "@etc/bar/Tsc/",
    ]
)
def test_path_keyword_not_found(test_input):
    parser = create_parser(test_input, parsing.PathParser)
    with pytest.raises(KeywordNotFoundError):
        parser.parse()


# KEYWORD ======================================================

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("foo", "foo"),
        ("Foo", "Foo"),
        ("@foo", "foo"),
        ("%foo", "foo"),
        ("?foo", "foo"),
        (".ba_r2", "ba_r2")
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


def test_name_not_found_after_prefix():
    with pytest.raises(NameNotFoundError):
        parse("(@ )")


@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("foo", parsing.NameParser),
        ("bar_", parsing.NameParser),
        ("Foo", parsing.ConceptParser),
        ("#foo", parsing.TagParser),
        ("@foo", parsing.AliasParser),
        ("%foo", parsing.FormatParser),
        ("?foo", parsing.DocParser),
        (".fo_o", parsing.MetaParser)
    ]
)
def test_keyword_subparsers(test_input, parser):
    parser = create_parser(test_input, parser)
    assert parser.parse() is not None


# LITERAL =================================================

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


# RANGE ==================================================

def test_range_id():
    node = parse("2..4", parsing.RangeParser)
    assert node.id == nodes.RangeNode.id


def test_range_limit():
    node = parse("0..-10", parsing.RangeParser)
    assert node.start == 0
    assert node.end == -10


def test_range_without_specific_end():
    node = parse("42..", parsing.RangeParser)
    assert node.start == 42
    assert node.end is None


def test_range_without_specific_start():
    node = parse("..33", parsing.RangeParser)
    assert node.start is None
    assert node.end == 33


def test_range_must_have_at_least_one_int():
    with pytest.raises(InfiniteRangeError):
        parse("..", parsing.RangeParser)


def test_range_only_accepts_integers():
    with pytest.raises(InfiniteRangeError):
        parse("..3.4", parsing.RangeParser)


# SCOPE ===================================================

def test_scope_with_key_and_no_value():
    node = parse("(a)", parsing.ScopeParser)
    assert str(node.key) == "a"
    assert len(node) == 0


def test_scope_key_assumes_first_value():
    node = parse("(foo 42)", parsing.ScopeParser)
    assert str(node.key) == "foo"


def test_scope_with_many_values():
    node = parse("(a (b 2) 4 'etc')", parsing.ScopeParser)
    assert str(node[0]) == "(b 2)"
    assert str(node[1]) == "4"
    assert str(node[2]) == "'etc'"


def test_null_scope_key():
    node = parse("(: 4 'test')", parsing.ScopeParser)
    assert not node.key


@pytest.mark.parametrize(
    "test_input, value",
    [
        ("(foo 42)", 'foo'),
        ("(etc 'test')", 'etc'),
        ("(a/b 4 6 7)", 'a/b'),
    ]
)
def test_scope_key_string_repr(test_input, value):
    node = parse(test_input, parsing.ScopeParser)
    assert str(node.key) == value


@pytest.mark.parametrize(
    "test_input",
    [
        "()",
        "(44 'test')",
        "('test')"
    ]
)
def test_invalid_scope_key(test_input):
    with pytest.raises(KeyNotFoundError):
        parse(test_input, parsing.ScopeParser)


@pytest.mark.parametrize(
    "test_input",
    [
        "(x = 2)",
        "(a/b > 2)",
        "(@var != 'foo')"
    ]
)
def test_scope_unexpected_expression(test_input):
    with pytest.raises(UnexpectedTokenError):
        parse(test_input, parsing.ScopeParser)


# QUERY ===============================================

def test_query_key_single_value():
    node = parse("{abc 42}", parsing.QueryParser)
    assert str(node.key) == "abc"
    assert node[0].value == 42
