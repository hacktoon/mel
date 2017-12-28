import tempfile
import pytest
from dale.types import tokens
from dale.lexing import Lexer, TokenStream
from dale.types.errors import LexingError, UnexpectedValueError


def create_lexer(text):
    return Lexer(text, tokens.rules).tokenize()


def create_stream(text):
    return TokenStream(text, tokens.rules)


def test_token_comparison():
    tokens = create_lexer('54')
    assert tokens[0].id == 'int'


def test_newline_and_comments_are_ignored():
    tokens = create_lexer('#comment \n 45')
    assert tokens[0].value == '45'


def test_tokenize_boolean_values():
    tokens = create_lexer(r'true false')
    assert tokens[0].value == 'true'
    assert tokens[1].value == 'false'


def test_tokenize_string_with_single_quotes():
    tokens = create_lexer(r"'single' string")
    assert tokens[0].value == "'single'"


def test_tokenize_string_with_double_quotes():
    tokens = create_lexer(r'"single" string')
    assert tokens[0].value == '"single"'


def test_tokenize_string_with_newline():
    tokens = create_lexer(r'"line one\nline two"')
    assert tokens[0].value == r'"line one\nline two"'


def test_tokenize_string_with_escaped_quotes():
    tokens = create_lexer(r'"single \"escaped\"" string')
    assert tokens[0].value == r'"single \"escaped\""'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = create_lexer(r"'single \'escaped\'' string")
    assert tokens[0].value == r"'single \'escaped\''"


def test_tokenize_ints_and_floats():
    tokens = create_lexer('34 -5.62 -532')
    assert tokens[0].value == '34'
    assert tokens[1].value == '-5.62'
    assert tokens[2].value == '-532'


def test_tokenize_parenthesis():
    tokens = create_lexer(r'()')
    assert tokens[0].value == '('
    assert tokens[1].value == ')'


def test_tokenize_names():
    tokens = create_lexer(r'name value')
    assert tokens[0].value == 'name'
    assert tokens[1].value == 'value'


def test_name_tokens_cant_start_with_numbers():
    with pytest.raises(LexingError):
        create_lexer(r'42name')


def test_tokenize_modifier_expression():
    tokens = create_lexer(r':foo "bar" :var "null"')
    assert tokens[0].value == ':'
    assert tokens[1].value == 'foo'
    assert tokens[2].value == '"bar"'
    assert tokens[3].value == ':'
    assert tokens[4].value == 'var'


def test_tokenize_query_strings():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    tokens = create_lexer(text)
    assert tokens[0].value == '@'
    assert tokens[1].value == '"/data/source/\nattribute[id=\'x\']"'
    assert tokens[2].value == '@'
    assert tokens[3].value == '"/site/title"'


def test_stream_get_current_token():
    stream = create_stream('345 name ()')
    assert stream.current().value == '345'


def test_stream_verify_current_token():
    stream = create_stream('345 name (')
    assert stream.read('int')
    assert stream.is_current('name')
    assert not stream.is_current('string')
    assert stream.read('name')
    assert stream.is_current('(')


def test_stream_verify_next_token():
    stream = create_stream('"bár" @ (')
    assert stream.is_current('string')
    assert stream.is_next('@')
    assert stream.read('string')
    assert stream.is_next('(')


def test_stream_read_token_with_no_id():
    stream = create_stream('42 foo')
    int_token = stream.read('int')
    assert int_token.value == '42'
    name_token = stream.read('name')
    assert name_token.value == 'foo'


def test_that_read_unexpected_token_raises_error():
    stream = create_stream('"string"')
    with pytest.raises(UnexpectedValueError):
        stream.read('int')


def test_stream_ends_with_eof_token():
    stream = create_stream('(age 5)')
    stream.read('(')
    stream.read('name')
    assert not stream.is_eof()
    stream.read('int')
    stream.read(')')
    assert stream.is_eof()
    assert stream.is_current('eof')
