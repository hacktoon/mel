import tempfile
import pytest
from dale.lexing import Lexer, TokenStream
from dale.types import tokens
from dale.types.errors import LexingError, ParsingError


def test_token_comparison():
    tokens = Lexer('54').tokenize()
    assert tokens[0].id == 'int'


def test_token_line_and_column():
    tokens = Lexer('2\r\n"foo"\n@').tokenize()
    assert tokens[0].value == '2'
    assert tokens[0].line == 1
    assert tokens[1].line == 2
    assert tokens[2].value == '"foo"'
    assert tokens[2].line == 2
    assert tokens[4].value == '@'
    assert tokens[4].line == 3


def test_tokenize_boolean_values():
    tokens = Lexer(r'true false').tokenize()
    assert tokens[0].value == 'true'
    assert tokens[2].value == 'false'


def test_tokenize_string_with_single_quotes():
    tokens = Lexer(r"'single' string").tokenize()
    assert tokens[0].value == "'single'"


def test_tokenize_string_with_double_quotes():
    tokens = Lexer(r'"single" string').tokenize()
    assert tokens[0].value == '"single"'


def test_tokenize_string_with_newline():
    tokens = Lexer(r'"line one\nline two"').tokenize()
    assert tokens[0].value == r'"line one\nline two"'


def test_tokenize_string_with_escaped_quotes():
    tokens = Lexer(r'"single \"escaped\"" string').tokenize()
    assert tokens[0].value == r'"single \"escaped\""'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = Lexer(r"'single \'escaped\'' string").tokenize()
    assert tokens[0].value == r"'single \'escaped\''"


def test_tokenize_ints_and_floats():
    tokens = Lexer('34 -5.62 -532').tokenize()
    assert tokens[0].value == '34'
    assert tokens[2].value == '-5.62'
    assert tokens[4].value == '-532'


def test_tokenize_parenthesis():
    tokens = Lexer(r'()').tokenize()
    assert tokens[0].value == '('
    assert tokens[1].value == ')'


def test_tokenize_names():
    tokens = Lexer(r'name value').tokenize()
    assert tokens[0].value == 'name'
    assert tokens[2].value == 'value'


def test_name_tokens_cant_start_with_numbers():
    with pytest.raises(LexingError):
        Lexer(r'42foo').tokenize()


def test_tokenize_modifier_expression():
    tokens = Lexer(r':foo "bar" :var "null"').tokenize()
    assert tokens[0].value == ':'
    assert tokens[1].value == 'foo'
    assert tokens[3].value == '"bar"'
    assert tokens[5].value == ':'
    assert tokens[6].value == 'var'


def test_tokenize_query_strings():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    tokens = Lexer(text).tokenize()
    assert tokens[0].value == '@'
    assert tokens[1].value == '"/data/source/\nattribute[id=\'x\']"'
    assert tokens[3].value == '@'
    assert tokens[4].value == '"/site/title"'


def test_stream_get_current_token():
    stream = TokenStream('345 name ()')
    assert stream.current().value == '345'


def test_stream_verify_current_token():
    stream = TokenStream('345 name (')
    assert stream.read('int')
    stream.read('whitespace')
    assert stream.is_current('name')
    assert not stream.is_current('string')
    assert stream.read('name')
    stream.read('whitespace')
    assert stream.is_current('(')


def test_stream_read_token_with_no_id():
    stream = TokenStream('42 foo')
    int_token = stream.read('int')
    assert int_token.value == '42'
    stream.read()
    name_token = stream.read('name')
    assert name_token.value == 'foo'


def test_that_read_unexpected_token_raises_error():
    stream = TokenStream('"string"')
    with pytest.raises(ParsingError):
        stream.read('int')


def test_stream_ends_with_eof_token():
    stream = TokenStream('(age 5)')
    stream.read('(')
    stream.read('name')
    assert not stream.is_eof()
    stream.read()
    stream.read('int')
    stream.read(')')
    assert stream.is_eof()
    assert stream.is_current('eof')