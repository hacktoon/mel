import pytest
from dale.lexing import Lexer
from dale.data.tokens import TokenType
from dale.data.errors import LexingError


def test_that_comment_tokens_are_ignored():
    tokens = Lexer('#comment  \n@here').tokenize()
    assert tokens[0] == 'ALIAS<here>'


def test_token_line_count():
    tokens = Lexer('foo 2\n  bar').tokenize()
    assert tokens[0].line == 0
    assert tokens[1].line == 0
    assert tokens[2].line == 1
    assert tokens[2].column == 2


def test_tokenize_boolean_values():
    tokens = Lexer(r'true false').tokenize()
    assert tokens[0] == 'BOOLEAN<True>'
    assert tokens[1] == 'BOOLEAN<False>'


def test_tokenize_string_with_single_quotes():
    tokens = Lexer(r"'single' string").tokenize()
    assert tokens[0] == 'STRING<single>'


def test_tokenize_string_with_double_quotes():
    tokens = Lexer(r'"single" string').tokenize()
    assert tokens[0] == 'STRING<single>'


def test_tokenize_string_with_newline():
    tokens = Lexer(r'"line one\nline two"').tokenize()
    assert tokens[0] == 'STRING<line one\nline two>'


def test_tokenize_string_with_escaped_quotes():
    tokens = Lexer(r'"single \"escaped\"" string').tokenize()
    assert tokens[0] == 'STRING<single \"escaped\">'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    tokens = Lexer(r"'single \'escaped\'' string").tokenize()
    assert tokens[0] == 'STRING<single \'escaped\'>'


def test_tokenize_ints_and_floats():
    tokens = Lexer(r'34 -5.62 -532').tokenize()
    assert tokens[0] == 'INT<34>'
    assert tokens[1] == 'FLOAT<-5.62>'
    assert tokens[2] == 'INT<-532>'


def test_tokenize_parenthesis_and_brackets():
    tokens = Lexer(r'[]()').tokenize()
    assert tokens[0] == 'OPEN_LIST'
    assert tokens[1] == 'CLOSE_LIST'
    assert tokens[2] == 'OPEN_EXP'
    assert tokens[3] == 'CLOSE_EXP'


def test_tokenize_aliases():
    tokens = Lexer(r'@name @value').tokenize()
    assert tokens[0] == 'ALIAS<name>'
    assert tokens[1] == 'ALIAS<value>'


def test_tokenize_aliases_cant_start_with_numbers():
    with pytest.raises(LexingError):
        Lexer(r'@42foo').tokenize()


def test_tokenize_aliases_and_keywords_with_hifens_and_numbers():
    tokens = Lexer(r'@name33 id-foo').tokenize()
    assert tokens[0] == 'ALIAS<name33>'
    assert tokens[1] == 'KEYWORD<id-foo>'


def test_aliases_using_dot_syntax():
    tokens = Lexer(r'@foo.bar @a2.bez').tokenize()
    assert tokens[0] == 'ALIAS<foo.bar>'
    assert tokens[1] == 'ALIAS<a2.bez>'


def test_dot_token_wont_match_after_an_alias():
    with pytest.raises(LexingError):
        Lexer(r'f2.').tokenize()


def test_dot_token_wont_match_before_an_alias():
    with pytest.raises(LexingError):
        Lexer(r'.f5').tokenize()


def test_aliass_cant_start_with_hifens():
    with pytest.raises(LexingError):
        tokens = Lexer(r'-foo').tokenize()


def test_aliass_cant_end_with_hifens():
    with pytest.raises(LexingError):
        tokens = Lexer(r'foo-').tokenize()


def test_type_of_alias_tokens_with_dot_syntax():
    tokens = Lexer(r'@name.title').tokenize()
    assert tokens[0].type == TokenType.ALIAS


def test_aliass_with_dots_can_have_spaces_between_them():
    tokens = Lexer(r'@name . title').tokenize()
    assert tokens[0].type == TokenType.ALIAS


def test_wrong_code_raises_syntax_exception_with_message():
    with pytest.raises(LexingError) as error:
        Lexer(r'(foo %').tokenize()
    assert str(error.value) == 'invalid syntax'


def test_tokenize_modifier_expression():
    tokens = Lexer(r':foo "bar" :var "null"').tokenize()
    assert tokens[0] == 'PARAMETER<foo>'
    assert tokens[1] == 'STRING<bar>'
    assert tokens[2] == 'PARAMETER<var>'
    assert tokens[3] == 'STRING<null>'


def test_tokenize_query():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    tokens = Lexer(text).tokenize()
    assert tokens[0] == 'QUERY</data/source/\nattribute[id=\'x\']>'
    assert tokens[1] == 'QUERY</site/title>'
