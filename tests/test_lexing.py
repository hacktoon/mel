import tempfile
import pytest
from dale.lexing import Lexer, TokenStream
from dale.types import tokens
from dale.types.errors import LexingError


def test_token_comparison():
    token_list = Lexer('54').tokenize()
    assert isinstance(token_list[0], tokens.IntToken)


def test_that_comment_and_whitespace_tokens_are_ignored():
    token_list = Lexer('#comment  \nhere').tokenize()
    assert token_list[0].value == 'here'


def test_tokenize_boolean_values():
    token_list = Lexer(r'true false').tokenize()
    assert token_list[0].value == True
    assert token_list[1].value == False


def test_tokenize_string_with_single_quotes():
    token_list = Lexer(r"'single' string").tokenize()
    assert token_list[0].value == 'single'


def test_tokenize_string_with_double_quotes():
    token_list = Lexer(r'"single" string').tokenize()
    assert token_list[0].value == 'single'


def test_tokenize_string_with_newline():
    token_list = Lexer(r'"line one\nline two"').tokenize()
    assert token_list[0].value == 'line one\nline two'


def test_tokenize_string_with_escaped_quotes():
    token_list = Lexer(r'"single \"escaped\"" string').tokenize()
    assert token_list[0].value == 'single \"escaped\"'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    token_list = Lexer(r"'single \'escaped\'' string").tokenize()
    assert token_list[0].value == 'single \'escaped\''


def test_tokenize_ints_and_floats():
    token_list = Lexer('34 -5.62 -532').tokenize()
    assert token_list[0].value == 34
    assert token_list[1].value == -5.62
    assert token_list[2].value == -532


def test_tokenize_parenthesis():
    token_list = Lexer(r'()').tokenize()
    assert token_list[0].value == '('
    assert token_list[1].value == ')'


def test_tokenize_names():
    token_list = Lexer(r'name value').tokenize()
    assert token_list[0].value == 'name'
    assert token_list[1].value == 'value'


def test_name_tokens_cant_start_with_numbers():
    with pytest.raises(LexingError):
        Lexer(r'42foo').tokenize()


def test_named_expression_ending_keyword_must_be_equal():
    token_list = Lexer('(name  \t "foo")name)').tokenize()
    end_exp = token_list[-1]
    assert isinstance(end_exp, tokens.RightParenToken)
    assert end_exp.value == ')'


def test_named_expression_ending_must_not_have_spaces():
    token_list = Lexer('(two 2) two)').tokenize()
    assert str(token_list[3]) == ')'
    assert token_list[3].value == ')'


def test_wrong_code_raises_syntax_exception_with_message():
    with pytest.raises(LexingError) as error:
        Lexer(r'(foo %').tokenize()
    assert str(error.value) == 'invalid syntax'


def test_tokenize_modifier_expression():
    token_list = Lexer(r':foo "bar" :var "null"').tokenize()
    assert token_list[0].value == 'foo'
    assert token_list[1].value == 'bar'
    assert token_list[2].value == 'var'
    assert token_list[3].value == 'null'


def test_tokenize_query_strings():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    token_list = Lexer(text).tokenize()
    assert token_list[1].value == '/data/source/\nattribute[id=\'x\']'
    assert token_list[3].value == '/site/title'


def test_stream_get_current_token():
    stream = TokenStream('345 name ()')
    assert stream.current().value == 345


def test_stream_verify_current_token():
    stream = TokenStream('345 name ()')
    assert stream.read('Int')
    # import ipdb; ipdb.set_trace()
    assert stream.is_current('Name')
    assert not stream.is_current('String')
    assert stream.read('Name')
    assert stream.is_current('LeftParen')


def test_stream_read_token():
    stream = TokenStream('42 foo')
    int_token = stream.read('Int')
    assert int_token.value == 42
    name_token = stream.read('Name')
    assert name_token.value == 'foo'


def test_that_read_unexpected_token_raises_error():
    stream = TokenStream('"string"')
    with pytest.raises(LexingError):
        stream.read('Int')


def test_stream_ends_with_eof_token():
    stream = TokenStream('(age 5)')
    stream.read('LeftParen')
    stream.read('Name')
    assert not stream.is_eof()
    stream.read('Int')
    stream.read('RightParen')
    assert stream.is_eof()
    assert stream.is_current('EOF')