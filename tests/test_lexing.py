import pytest

from dale.lexing import Lexer, TokenStream
from dale.exceptions import InvalidSyntaxError, UnexpectedTokenError


def tokenize(text):
    return Lexer().tokenize(text)


def create_stream(text):
    return TokenStream(text)


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
    ('{', '{'),
    ('}', '}'),
    ('"string"', 'string'),
    ("'string'", 'string'),
    ("@", '@'),
    (':', ':'),
    ('foo', 'foo'),
    ('foo\n . bar', 'foo')
])
def test_token_value_comparison(test_input, expected):
    tokens = tokenize(test_input)
    assert tokens[0].value == expected


def test_newline_and_comments_are_ignored():
    tokens = tokenize('--comment \n 45')
    assert tokens[0].value == 45


def test_commas_are_treated_as_whitespace():
    tokens = tokenize('222, 45  true')
    assert tokens[0].value == 222
    assert tokens[1].value == 45
    assert tokens[2].value is True


def test_tokenize_string_with_newline():
    tokens = tokenize('"line one\nline two"')
    assert tokens[0].value == 'line one\nline two'


def test_tokenize_string_with_escaped_quotes():
    tokens = tokenize('"single \'escaped\'"')
    assert tokens[0].value == "single 'escaped'"


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = tokenize("'single \"escaped\"'")
    assert tokens[0].value == 'single "escaped"'


def test_name_tokens_cant_start_with_numbers():
    with pytest.raises(InvalidSyntaxError):
        tokenize(r'42name')


def test_non_terminated_string_throws_error():
    with pytest.raises(InvalidSyntaxError):
        tokenize('" test ')


def test_single_quoted_string_doesnt_allow_same_quote_symbol():
    with pytest.raises(InvalidSyntaxError):
        tokenize('"a quote \" "')


def test_double_quoted_string_doesnt_allow_same_quote_symbol():
    with pytest.raises(InvalidSyntaxError):
        tokenize('"a quote \" "')


def test_tokenize_attributes_tokens():
    tokens = tokenize(r':foo "bar" :var "null"')
    assert tokens[0].value == ':'
    assert tokens[1].value == 'foo'
    assert tokens[2].value == 'bar'
    assert tokens[3].value == ':'
    assert tokens[4].value == 'var'


def test_tokenize_query_strings():
    text = '@ "/data/query/", <"title.txt"'
    tokens = tokenize(text)
    assert tokens[0].value == '@'
    assert tokens[1].value == '/data/query/'
    assert tokens[2].value == '<'
    assert tokens[3].value == 'title.txt'


def test_that_read_unexpected_token_raises_error():
    stream = create_stream('"string"')
    with pytest.raises(UnexpectedTokenError):
        stream.read('int')


def test_stream_ends_with_eof_token():
    stream = create_stream('{age 5}')
    stream.read('{')
    stream.read('name')
    assert not stream.is_eof()
    stream.read('int')
    stream.read('}')
    assert stream.is_eof()
    assert stream.is_current('end of file')
