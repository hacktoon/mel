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
    UnexpectedKeywordError,
    ObjectNotFoundError,
    ExpectedKeywordError
)


def create_parser(text, Parser=parsing.Parser):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text, Parser=parsing.Parser):
    return create_parser(text, Parser).parse()


def parse_one(text):
    return create_parser(text).parse()[0]


# BASE PARSER ===========================================

def test_subparser_invalid_node_id():
    stream = TokenStream("foo")
    with pytest.raises(Exception):
        parsing.base.get_subparser("x", stream)


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


@pytest.mark.parametrize(
    "test_input",
    [
        "etc)",
        "#fd]",
        "44}",
    ]
)
def test_incomplete_input_token(test_input):
    parser = create_parser(test_input)
    with pytest.raises(UnexpectedTokenError):
        parser.parse()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("42 (bar) 'foo'", ['int', 'scope', 'string']),
        ("3.14 {bar} true", ['float', 'reference', 'boolean']),

    ],
)
def test_node_iteration(test_input, expected):
    node = parse(test_input)
    for index, child in enumerate(node):
        assert child.id == expected[index]


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
    node = parse(test_input, parsing.keyword.TagParser)
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
    "test_input, key, sign, object",
    [
        ("x = 4", 'x', '=', '4'),
        ("x >< -5", 'x', '><', '-5'),
        ("a/b <> foo", 'a/b', '<>', 'foo'),
        ("x/y != 64", 'x/y', '!=', '64'),
        ("a/pid/f_a > [1, 2]", 'a/pid/f_a', '>', '[1, 2]'),
    ]
)
def test_relation_components(test_input, key, sign, object):
    node = parse(test_input, parsing.struct.RelationParser)
    assert str(node.key) == key
    assert str(node.sign) == sign
    assert str(node.value) == object


@pytest.mark.parametrize(
    "test_input",
    [
        "x = >",
        "x <= ",
        "x > <",
        "x >= =",
    ]
)
def test_relation_object_expected(test_input):
    with pytest.raises(ObjectNotFoundError):
        parse(test_input, parsing.struct.RelationParser)


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
        '!foo/@bar',
        '%foo/$bar',
        "etc/bar/#active",
        "etc/bar/(: a=2 b=true)",
        'abc/[1 2]'
    ]
)
def test_reference_keywords(test_input):
    parser = create_parser(test_input, parsing.reference.ReferenceParser)
    assert parser.parse()


@pytest.mark.parametrize(
    "test_input",
    [
        "etc/bar/#active/ge",
        'foo/#bar/ff',
        "etc/#bar/",
    ]
)
def test_reference_non_terminal_tag_error(test_input):
    with pytest.raises(UnexpectedKeywordError):
        parse(test_input, parsing.reference.ReferenceParser)


@pytest.mark.parametrize(
    "test_input",
    [
        "etc/bar/",
        "!etc/@bar/",
    ]
)
def test_reference_expected_child(test_input):
    with pytest.raises(ExpectedKeywordError):
        parse(test_input, parsing.reference.ReferenceParser)


# PATH =================================================

@pytest.mark.parametrize(
    "test_input, total",
    [
        ("foo", 1),
        ("Bar", 1),
        ("Bar/$redis", 2),
        ("Foo/bar/?baz", 3),
        ("foo/Bar/%baz", 3),
        ("!foo/Etc/@bar/baz", 4)
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
        ("!baz", "baz"),
        ("?foo", "foo"),
        (".ba_r2", "ba_r2")
    ]
)
def test_keyword_acceptance(test_input, expected):
    parser = create_parser(test_input, parsing.keyword.KeywordParser)
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
    parser = create_parser(test_input, parsing.keyword.KeywordParser)
    assert parser.parse() is None


def test_name_not_found_after_prefix():
    with pytest.raises(NameNotFoundError):
        parse("(@ )")


@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("foo", parsing.keyword.NameParser),
        ("bar_", parsing.keyword.NameParser),
        ("Foo", parsing.keyword.ConceptParser),
        ("#foo", parsing.keyword.TagParser),
        ("!foo", parsing.keyword.LogParser),
        ("@foo", parsing.keyword.AliasParser),
        ("%foo", parsing.keyword.FormatParser),
        ("?foo", parsing.keyword.DocParser),
        (".fo_o", parsing.keyword.MetaParser)
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
    parser = create_parser(test_input, parsing.literal.LiteralParser)
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
    parser = create_parser(test_input, parsing.literal.LiteralParser)
    assert parser.parse() is None


@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("3", parsing.literal.IntParser),
        ("-3.44", parsing.literal.FloatParser),
        ('" aaa "', parsing.literal.StringParser),
        ("'foo'", parsing.literal.StringParser),
        ("true", parsing.literal.BooleanParser),
        ("False", parsing.literal.BooleanParser),

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


# STRUCT ===================================================

def test_tag_scope():
    node = parse("(a #bar #foo)", parsing.struct.ScopeParser)
    assert 'bar' in node.tags
    assert 'foo' in node.tags


# SCOPE ===================================================

def test_scope_with_key_and_no_value():
    node = parse("(a)", parsing.struct.ScopeParser)
    assert str(node.key) == "a"
    assert len(node) == 0


def test_scope_key_assumes_first_value():
    node = parse("(foo 42)", parsing.struct.ScopeParser)
    assert str(node.key) == "foo"


@pytest.mark.parametrize(
    "test_input, value",
    [
        ("(foo 42)", 'foo'),
        ("(etc 'test')", 'etc'),
        ("(a/b 4 6 7)", 'a'),
    ]
)
def test_scope_key_string_repr(test_input, value):
    node = parse(test_input, parsing.struct.ScopeParser)
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
        parse(test_input, parsing.struct.ScopeParser)


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
        parse(test_input, parsing.struct.ScopeParser)


# QUERY ===============================================

@pytest.mark.skip
def test_query_key_single_value():
    node = parse("{abc 42}", parsing.struct.QueryParser)
    assert str(node.key) == "abc"
    assert node[0].value == 42


# PROTOTYPE ===============================================

@pytest.mark.skip
def test_prototype_key_single_value():
    node = parse("((abc 42))", parsing.struct.PrototypeParser)
    assert str(node.key) == "abc"
    assert node[0].value == 42
