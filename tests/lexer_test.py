import pytest
from dale.error import SyntaxError
from dale.lexer import Lexer
from dale.token import TokenType


def test_that_comment_tokens_are_ignored():
    tokens = Lexer('#comment  \nhere').tokenize()
    assert tokens[0] == 'IDENTIFIER(here)'


def test_token_line_count():
    tokens = Lexer('foo 2\n  bar').tokenize()
    assert tokens[0].line == 0
    assert tokens[1].line == 0
    assert tokens[2].line == 1
    assert tokens[2].column == 2


def test_tokenize_boolean_values():
    tokens = Lexer(r'true false').tokenize()
    assert tokens[0] == 'BOOLEAN(True)'
    assert tokens[1] == 'BOOLEAN(False)'


def test_tokenize_string_with_single_quotes():
    tokens = Lexer(r"'single' string").tokenize()
    assert tokens[0] == 'STRING(single)'


def test_tokenize_string_with_double_quotes():
    tokens = Lexer(r'"single" string').tokenize()
    assert tokens[0] == 'STRING(single)'


def test_tokenize_string_with_newline():
    tokens = Lexer(r'"line one\nline two"').tokenize()
    assert tokens[0] == 'STRING(line one\nline two)'


def test_tokenize_string_with_escaped_quotes():
    tokens = Lexer(r'"single \"escaped\"" string').tokenize()
    assert tokens[0] == 'STRING(single \"escaped\")'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = Lexer(r"'single \'escaped\'' string").tokenize()
    assert tokens[0] == 'STRING(single \'escaped\')'


def test_tokenize_ints_and_floats():
    tokens = Lexer(r'34 -5.62 -532').tokenize()
    assert tokens[0] == 'INT(34)'
    assert tokens[1] == 'FLOAT(-5.62)'
    assert tokens[2] == 'INT(-532)'


def test_tokenize_parenthesis_and_brackets():
    tokens = Lexer(r'[](){}').tokenize()
    assert tokens[0] == 'OPEN_LIST'
    assert tokens[1] == 'CLOSE_LIST'
    assert tokens[2] == 'OPEN_EXP'
    assert tokens[3] == 'CLOSE_EXP'
    assert tokens[4] == 'OPEN_PARAM'
    assert tokens[5] == 'CLOSE_PARAM'


def test_tokenize_identifiers():
    tokens = Lexer(r'name value ').tokenize()
    assert tokens[0] == 'IDENTIFIER(name)'
    assert tokens[1] == 'IDENTIFIER(value)'


def test_tokenize_identifiers_cant_start_with_numbers():
    with pytest.raises(SyntaxError):
        Lexer(r'(42foo').tokenize()


def test_tokenize_identifiers_with_hifens_and_numbers():
    tokens = Lexer(r'name33 id-foo').tokenize()
    assert tokens[0] == 'IDENTIFIER(name33)'
    assert tokens[1] == 'IDENTIFIER(id-foo)'


def test_dot_token_matches_between_identifiers():
    tokens = Lexer(r'foo.bar a2.bez').tokenize()
    assert tokens[0] == 'IDENTIFIER(foo)'
    assert tokens[1] == 'DOT'
    assert tokens[2] == 'IDENTIFIER(bar)'
    assert tokens[3] == 'IDENTIFIER(a2)'
    assert tokens[4] == 'DOT'
    assert tokens[5] == 'IDENTIFIER(bez)'


def test_dot_token_wont_match_after_a_identifier():
    with pytest.raises(SyntaxError):
        Lexer(r'f2.').tokenize()


def test_dot_token_wont_match_before_a_identifier():
    with pytest.raises(SyntaxError):
        Lexer(r'.f5').tokenize()


def test_identifiers_cant_start_with_hifens():
    with pytest.raises(SyntaxError):
        tokens = Lexer(r'-foo').tokenize()


def test_identifiers_cant_end_with_hifens():
    with pytest.raises(SyntaxError):
        tokens = Lexer(r'foo-').tokenize()


def test_type_of_identifier_tokens_with_dot_syntax():
    tokens = Lexer(r'name.title').tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[1].type == TokenType.DOT
    assert tokens[2].type == TokenType.IDENTIFIER


def test_identifiers_with_dots_cant_have_spaces_between_them():
    with pytest.raises(SyntaxError) as error:
        Lexer(r'name . title').tokenize()


def test_wrong_code_raises_syntax_exception_with_message():
    with pytest.raises(SyntaxError) as error:
        Lexer(r'foo(%').tokenize()
    assert str(error.value) == 'invalid syntax'


def test_tokenize_modifier_expression():
    tokens = Lexer(r'{foo: "bar", var: "null"}').tokenize()
    assert tokens[0] == 'OPEN_PARAM'
    assert tokens[1] == 'IDENTIFIER(foo)'
    assert tokens[2] == 'COLON'
    assert tokens[3] == 'STRING(bar)'
    assert tokens[4] == 'COMMA'
    assert tokens[5] == 'IDENTIFIER(var)'
    assert tokens[6] == 'COLON'
    assert tokens[7] == 'STRING(null)'
    assert tokens[8] == 'CLOSE_PARAM'


def test_tokenize_query():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    tokens = Lexer(text).tokenize()
    assert tokens[0] == 'QUERY(/data/source/\nattribute[id=\'x\'])'
    assert tokens[1] == 'QUERY(/site/title)'
