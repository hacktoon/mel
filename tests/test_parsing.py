import pytest

from mel import parsing
from mel import nodes

from mel.lexing import TokenStream
from mel.exceptions import ParsingError


def create_parser(text, Parser=parsing.Parser):
    stream = TokenStream(text)
    return Parser(stream)


def parse(text, Parser=parsing.Parser):
    return create_parser(text, Parser).parse()


def parse_one(text):
    return create_parser(text).parse()[0]


# PARSER ===========================================

@pytest.mark.skip()
def test_empty_input_string():
    node = parse("")
    assert node.id == nodes.RootNode.id
    assert len(node) == 0


@pytest.mark.skip()
def test_whitespace_only():
    node = parse("   ,,,\n ; , ;, \t ")
    assert node.id == nodes.RootNode.id
    assert len(node) == 0


# TO STRING ===========================================

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
@pytest.mark.skip()
def test_string_representation(test_input):
    tree = parse(test_input)
    assert str(tree) == test_input


# REPR ===========================================

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("-215", "INT('-215')"),
        ("56.75", "FLOAT('56.75')"),
        ("id", "REFERENCE('id')"),
        ("@path", "REFERENCE('@path')"),
        ("(bar 42)", "OBJECT('(bar 42)')"),
        ('["bar" "etc"]', "LIST('[\"bar\" \"etc\"]')")
    ],
)
@pytest.mark.skip()
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
@pytest.mark.skip()
def test_incomplete_input_EOF(test_input):
    parser = create_parser(test_input)
    with pytest.raises(ParsingError):
        parser.parse()


@pytest.mark.parametrize(
    "test_input",
    [
        "etc)",
        "#fd]",
        "44}",
    ]
)
@pytest.mark.skip()
def test_incomplete_input_token(test_input):
    parser = create_parser(test_input)
    with pytest.raises(ParsingError):
        parser.parse()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("42 (bar) 'foo'", ['int', 'object', 'string']),
        ("3.14 {bar} true", ['float', 'reference', 'boolean']),

    ],
)
@pytest.mark.skip()
def test_node_iteration(test_input, expected):
    node = parse(test_input)
    for index, child in enumerate(node):
        assert child.id == expected[index]


# NODE INDEX ===========================================

@pytest.mark.skip()
def test_node_subnodes_index():
    node = parse("44 12")
    assert node[0].index == (0, 2)
    assert node[1].index == (3, 5)


@pytest.mark.skip()
def test_list_index():
    node = parse("[1, 2]")
    assert node.index == (0, 6)


@pytest.mark.skip()
def test_object_index():
    _object = parse("(a 2)")
    assert _object.index == (0, 5)


# TAG =================================================

@pytest.mark.parametrize(
    "test_input",
    [
        "#foo",
        "#bar_4",
        "#fA_o",
    ]
)
@pytest.mark.skip()
def test_tags(test_input):
    node = parse(test_input, parsing.keyword.TagParser)
    assert node.id == nodes.TagKeywordNode.id


# VALUE ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        ('"abc"'),
        ("'etc'"),
        ('[1, -2.3, True]'),
        ('42'),
        ('a/b/c'),
        ('(a 3)'),
    ]
)
@pytest.mark.skip()
def test_subparser_value(test_input):
    parser = create_parser(test_input, parsing.value.ValueParser)
    assert parser.parse()


#  LIST ======================================================

@pytest.mark.skip()
def test_subparser_empty_list():
    parser = create_parser("[]", parsing.literal.ListParser)
    assert parser.parse().id == nodes.ListNode.id


@pytest.mark.skip()
def test_subparser_literal_list():
    parser = create_parser("[1, 2]", parsing.literal.ListParser)
    assert parser.parse().id == nodes.ListNode.id


@pytest.mark.skip()
def test_list_size():
    parser = create_parser("[-1, (x 2), 'abc']", parsing.literal.ListParser)
    assert len(parser.parse()) == 3


@pytest.mark.skip()
def test_subparser_nested_list():
    parser = create_parser("[[], [1, 2]]", parsing.literal.ListParser)
    node = parser.parse()
    assert node[0].id == nodes.ListNode.id
    assert node[1].id == nodes.ListNode.id


#  REFERENCE ======================================================

@pytest.mark.parametrize(
    "test_input",
    [
        "etc",
        "bar/?name",
        'foo/#bar',
        '!foo/@bar',
        '%foo/$bar',
        "etc/bar/#active",
        'abc/[1 2]'
    ]
)
@pytest.mark.skip()
def test_reference_keywords(test_input):
    parser = create_parser(test_input, parsing.reference.ReferenceParser)
    assert parser.parse()


# PATH =================================================

@pytest.mark.parametrize(
    "test_input, total",
    [
        ("foo", 1),
        ("Bar", 1),
        ("Bar/$redis", 2),
        ("Bar.name", 2),
        ("Bar.name/%upper", 3),
        ("Foo/bar/?baz", 3),
        ("foo/Bar/%baz", 3),
        ("!foo/Etc/@bar/baz", 4)
    ]
)
@pytest.mark.skip()
def test_path_length(test_input, total):
    parser = create_parser(test_input, parsing.path.PathParser)
    node = parser.parse()
    assert len(node) == total


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("foo", nodes.NameKeywordNode),
        ("Bar", nodes.ConceptKeywordNode),
        ("@code", nodes.AliasKeywordNode),
        ("%code", nodes.FormatKeywordNode),
        ("?code", nodes.DocKeywordNode)
    ]
)
@pytest.mark.skip()
def test_path_single_node_ids(test_input, expected):
    parser = create_parser(test_input, parsing.path.PathParser)
    node = parser.parse()
    assert node[0].id == expected.id


# KEYWORD ======================================================

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("!baz", "baz"),
        ("foo", "foo"),
        ("Foo", "Foo"),
        ("@foo", "foo"),
        ("%foo", "foo"),
        ("?foo", "foo")
    ]
)
@pytest.mark.skip()
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
@pytest.mark.skip()
def test_keyword_non_acceptance(test_input):
    parser = create_parser(test_input, parsing.keyword.KeywordParser)
    with pytest.raises(ParsingError):
        parser.parse()


@pytest.mark.skip()
def test_name_not_found_after_prefix():
    parser = create_parser("@", parsing.keyword.KeywordParser)
    with pytest.raises(ParsingError):
        parser.parse()


@pytest.mark.skip()
def test_expected_name_instead_of_int():
    parser = create_parser("$ 4", parsing.keyword.KeywordParser)
    with pytest.raises(ParsingError):
        parser.parse()


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
    ]
)
@pytest.mark.skip()
def test_keyword_subparsers(test_input, parser):
    parser = create_parser(test_input, parser)
    assert parser.parse()


# LITERAL =================================================

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2", "2"),
        ("4.7e3", "4.7e3"),
        ("'foo'", "'foo'"),
        ("true", "true"),
        ("True", "True"),
        ("false", "false"),
        ("False", "False")
    ]
)
@pytest.mark.skip()
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
@pytest.mark.skip()
def test_literal_non_acceptance(test_input):
    parser = create_parser(test_input, parsing.literal.LiteralParser)
    with pytest.raises(ParsingError):
        parser.parse()


@pytest.mark.parametrize(
    "test_input, parser",
    [
        ("3", parsing.literal.IntParser),
        ("-3.44", parsing.literal.FloatParser),
        ('" aaa "', parsing.literal.TemplateStringParser),
        ("'foo'", parsing.literal.StringParser),
        ("true", parsing.literal.BooleanParser),
        ("False", parsing.literal.BooleanParser),
    ]
)
@pytest.mark.skip()
def test_literal_subparsers(test_input, parser):
    parser = create_parser(test_input, parser)
    assert parser.parse() is not None


# RANGE ==================================================

@pytest.mark.skip()
def test_range_id():
    node = parse("2..4", parsing.literal.RangeParser)
    assert node.id == nodes.RangeNode.id


@pytest.mark.skip()
def test_range_limit():
    node = parse("0..-10", parsing.literal.RangeParser)
    assert node.start == "0"
    assert node.end == "-10"


@pytest.mark.skip()
def test_range_without_specific_end():
    node = parse("42..", parsing.literal.RangeParser)
    assert node.start == "42"
    assert node.end is None


@pytest.mark.skip()
def test_range_without_specific_start():
    node = parse("..33", parsing.literal.RangeParser)
    assert node.start is None
    assert node.end == "33"


@pytest.mark.skip()
def test_range_must_have_at_least_one_int():
    with pytest.raises(ParsingError):
        parse("..", parsing.literal.RangeParser)


@pytest.mark.skip()
def test_range_only_accepts_integers():
    with pytest.raises(ParsingError):
        parse("..3.4", parsing.literal.RangeParser)


# RELATION =================================================

@pytest.mark.parametrize(
    "test_input, path, value",
    [
        ("x = 4", 'x', '4'),
        ("x >< -5", 'x', '-5'),
        ("a/b <> foo", 'a/b', 'foo'),
        ("x/y != 64", 'x/y', '64'),
        ("a/pid/f_a > [1, 2]", 'a/pid/f_a', '[1, 2]'),
    ]
)
@pytest.mark.skip()
def test_relation_components(test_input, path, value):
    node = parse(test_input, parsing.relation.RelationParser)
    assert str(node.path) == path
    assert str(node.value) == value


@pytest.mark.parametrize(
    "test_input",
    [
        "x = >",
        "x <= ",
        "x > <",
        "x >= =",
    ]
)
@pytest.mark.skip()
def test_relation_value_expected(test_input):
    with pytest.raises(ParsingError):
        parse(test_input, parsing.relation.RelationParser)


# STRUCT ===================================================

@pytest.mark.parametrize(
    "test_input, Parser",
    [
        ("(?: 2)", parsing.struct.ObjectParser),
        ("(%: foo bar)", parsing.struct.ObjectParser),
        ("(abc foo bar)", parsing.struct.ObjectParser),
        ("(: foo bar)", parsing.struct.ObjectParser),
        ("{abc foo bar}", parsing.struct.QueryParser),
        ("{: foo bar}", parsing.struct.QueryParser),
    ]
)
@pytest.mark.skip()
def test_struct_object_expression(test_input, Parser):
    assert parse(test_input, Parser)
    assert parse(test_input)


# OBJECT ===================================================

@pytest.mark.skip()
def test_object_with_no_value():
    node = parse("(a)", parsing.struct.ObjectParser)
    assert len(node) == 0


@pytest.mark.parametrize(
    "test_input, value",
    [
        ("(foo 42)", 'foo'),
        ("(etc 'test')", 'etc'),
        ("(a/b 4 6 7)", 'a/b'),
    ]
)
@pytest.mark.skip()
def test_object_path_string_repr(test_input, value):
    node = parse(test_input, parsing.struct.ObjectParser)
    assert str(node.key) == value


@pytest.mark.parametrize(
    "test_input",
    [
        "()",
        "(44 'test')",
        "('test')"
    ]
)
@pytest.mark.skip()
def test_invalid_object_key(test_input):
    with pytest.raises(ParsingError):
        parse(test_input, parsing.struct.ObjectParser)


@pytest.mark.parametrize(
    "test_input",
    [
        "(x = 2)",
        "(a/b > 2)",
        "(@var != 'foo')"
    ]
)
@pytest.mark.skip()
def test_object_unexpected_expression(test_input):
    with pytest.raises(ParsingError):
        parse(test_input, parsing.struct.ObjectParser)


# ANONYM OBJECT ===============================================

@pytest.mark.skip()
def test_anonym_object_value():
    node = parse("(: x = 2)", parsing.struct.ObjectParser)
    assert str(node[0]) == "x = 2"


# QUERY ===============================================

@pytest.mark.skip()
def test_query_key_single_value():
    node = parse("{abc 42}", parsing.struct.QueryParser)
    assert node[0].value == "42"


# ANONYM QUERY ===============================================

@pytest.mark.skip()
def test_anonym_query_value():
    node = parse("{: 42}", parsing.struct.QueryParser)
    assert node[0].value == "42"
