import pytest

from mel import tokens
from mel.lexing import Lexer, TokenStream
from mel.exceptions import ParsingError


def tokenize(text):
    return Lexer(text).tokenize()


def create_stream(text):
    return TokenStream(text)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("56.75", 56.75),
        ("-0.75", -0.75),
        ("-.099999", -0.099999),
        ("-0.75e10", -0.75e10),
        ("1.45e-10", 1.45e-10),
        ("true", True),
        ("false", False),
        ("True", True),
        ("False", False),
        ("-56", -56),
        ("45", 45),
        ("(", "("),
        (")", ")"),
        ('"string"', "string"),
        ("'string'", "string"),
        ("foo", "foo"),
        ("foo\n / bar", "foo"),
    ],
)
def test_token_value_attribute(test_input, expected):
    tokens = tokenize(test_input)
    assert tokens[0].value == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("42", "TOKEN('42')"),
        ("true", "TOKEN('true')"),
        ("#", "TOKEN('#')"),
        ('"string"', "TOKEN('\"string\"')"),
        ("foo", "TOKEN('foo')"),
    ],
)
def test_token_repr(test_input, expected):
    tokens = tokenize(test_input)
    assert repr(tokens[0]) == expected


def test_token_indices():
    tokens = tokenize("1 abc @")
    assert tokens[0].index == (0, 1)
    assert tokens[1].index == (2, 5)
    assert tokens[2].index == (6, 7)


def test_boolean_regex_word_boundary():
    tokens = tokenize("TrueFalse")
    assert tokens[0].value == "TrueFalse"


def test_that_skipped_tokens_are_ignored():
    tokens = tokenize("--comment \n 45 --after")
    assert tokens[0].value == 45
    assert len(tokens) == 1


def test_commas_are_treated_as_whitespace():
    tokens = tokenize("222, 45 true")
    assert tokens[0].value == 222
    assert tokens[1].value == 45
    assert tokens[2].value is True


def test_tokens_line_count():
    tokens = tokenize('abc 33\n\nline "two"')
    assert tokens[0].line == 0
    assert tokens[1].line == 0
    assert tokens[2].line == 2
    assert tokens[3].line == 2


def test_tokens_column_count():
    tokens = tokenize('name "test"\nline two')
    assert tokens[0].column == 0
    assert tokens[1].column == 5
    assert tokens[2].column == 0
    assert tokens[3].column == 5


def test_string_with_newline_raises_line_count():
    tokens = tokenize('"line one\nline two" uid,etc')
    assert tokens[1].line == 1
    assert tokens[1].column == 10
    assert tokens[2].column == 14


def test_string_with_many_newlines_raises_line_count():
    tokens = tokenize('"line1\n line2\nline3" name')
    assert tokens[1].line == 2
    assert tokens[1].column == 7


def test_tokenize_string_with_escaped_quotes():
    tokens = tokenize("\"single 'escaped'\"")
    assert tokens[0].value == "single 'escaped'"


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = tokenize("'single \"escaped\"'")
    assert tokens[0].value == 'single "escaped"'


def test_name_tokens_cant_start_with_numbers():
    with pytest.raises(ParsingError):
        tokenize(r"42name")


def test_non_terminated_string_throws_error():
    with pytest.raises(ParsingError):
        tokenize('" test ')


def test_single_quoted_string_doesnt_allow_same_quote_symbol():
    with pytest.raises(ParsingError):
        tokenize('"a quote " "')


def test_double_quoted_string_doesnt_allow_same_quote_symbol():
    with pytest.raises(ParsingError):
        tokenize('"a quote " "')


def test_that_read_unexpected_token_raises_error():
    stream = create_stream('"string"')
    with pytest.raises(ParsingError):
        stream.read(tokens.IntToken)


def test_stream_ends_with_eof_token():
    stream = create_stream("(age 5)")
    stream.read(tokens.StartObjectToken)
    stream.read(tokens.NameToken)
    assert not stream.is_eof()
    stream.read(tokens.IntToken)
    stream.read(tokens.EndObjectToken)
    assert stream.is_eof()
    assert stream.is_next(tokens.NullToken)


def test_stream_default_savepoint():
    stream = create_stream("1 2")
    token = stream.read()
    assert token.value == 1
    stream.restore(0)
    token = stream.read()
    assert token.value == 1


def test_stream_savepoint():
    stream = create_stream("1 2 3")
    stream.read()
    index = stream.save()
    stream.read()
    stream.read()
    stream.restore(index)
    token = stream.read()
    assert token.value == 2
