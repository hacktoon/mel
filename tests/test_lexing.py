import pytest
from dale.lexing import Lexer
from dale.data import tokens
from dale.data.errors import LexingError


def test_that_comment_tokens_are_ignored():
    token_list = Lexer('#comment  \n@here').tokenize()
    assert token_list[0] == 'ALIAS<here>'


def test_token_line_count():
    token_list = Lexer('foo 2\n  bar').tokenize()
    assert token_list[0].line == 0
    assert token_list[1].line == 0
    assert token_list[2].line == 1
    assert token_list[2].column == 2


def test_tokenize_boolean_values():
    token_list = Lexer(r'true false').tokenize()
    assert token_list[0] == 'BOOLEAN<True>'
    assert token_list[1] == 'BOOLEAN<False>'


def test_tokenize_string_with_single_quotes():
    token_list = Lexer(r"'single' string").tokenize()
    assert token_list[0] == 'STRING<single>'


def test_tokenize_string_with_double_quotes():
    token_list = Lexer(r'"single" string').tokenize()
    assert token_list[0] == 'STRING<single>'


def test_tokenize_string_with_newline():
    token_list = Lexer(r'"line one\nline two"').tokenize()
    assert token_list[0] == 'STRING<line one\nline two>'


def test_tokenize_string_with_escaped_quotes():
    token_list = Lexer(r'"single \"escaped\"" string').tokenize()
    assert token_list[0] == 'STRING<single \"escaped\">'


def test_tokenize_string_with_escaped_quotes_and_single_quotes():
    token_list = Lexer(r"'single \'escaped\'' string").tokenize()
    assert token_list[0] == 'STRING<single \'escaped\'>'


def test_tokenize_ints_and_floats():
    token_list = Lexer(r'34 -5.62 -532').tokenize()
    assert token_list[0] == 'INT<34>'
    assert token_list[1] == 'FLOAT<-5.62>'
    assert token_list[2] == 'INT<-532>'


def test_tokenize_parenthesis_and_brackets():
    token_list = Lexer(r'[]()').tokenize()
    assert token_list[0] == 'OPEN_LIST'
    assert token_list[1] == 'CLOSE_LIST'
    assert token_list[2] == 'OPEN_EXP'
    assert token_list[3] == 'CLOSE_EXP'


def test_tokenize_aliases():
    token_list = Lexer(r'@name @value').tokenize()
    assert token_list[0] == 'ALIAS<name>'
    assert token_list[1] == 'ALIAS<value>'


def test_tokenize_aliases_cant_start_with_numbers():
    with pytest.raises(LexingError):
        Lexer(r'@42foo').tokenize()


def test_tokenize_aliases_and_keywords_with_hifens_and_numbers():
    token_list = Lexer(r'@name33 id-foo').tokenize()
    assert token_list[0] == 'ALIAS<name33>'
    assert token_list[1] == 'KEYWORD<id-foo>'


def test_aliases_using_dot_syntax():
    token_list = Lexer(r'@foo.bar @a2.bez').tokenize()
    assert token_list[0] == 'ALIAS<foo.bar>'
    assert token_list[1] == 'ALIAS<a2.bez>'


def test_expression_alt_closing():
    token_list = Lexer(r'(foo "bar")foo)').tokenize()
    close_exp = token_list[-1]
    assert close_exp == tokens.CloseExpressionToken
    assert close_exp.value == 'foo'


def test_expression_alt_closing_must_not_have_spaces():
    token_list = Lexer(r'(two 2) two)').tokenize()
    assert token_list[3] == 'CLOSE_EXP'
    assert token_list[3].value == ')'


def test_dot_token_wont_match_after_an_alias():
    with pytest.raises(LexingError):
        Lexer(r'f2.').tokenize()


def test_dot_token_wont_match_before_an_alias():
    with pytest.raises(LexingError):
        Lexer(r'.f5').tokenize()


def test_aliass_cant_start_with_hifens():
    with pytest.raises(LexingError):
        Lexer(r'-foo').tokenize()


def test_aliass_cant_end_with_hifens():
    with pytest.raises(LexingError):
        Lexer(r'foo-').tokenize()


def test_type_of_alias_tokens_with_dot_syntax():
    token_list = Lexer(r'@name.title').tokenize()
    assert token_list[0] == tokens.AliasToken


def test_aliass_with_dots_can_have_spaces_between_them():
    token_list = Lexer(r'@name . title').tokenize()
    assert token_list[0] == tokens.AliasToken


def test_wrong_code_raises_syntax_exception_with_message():
    with pytest.raises(LexingError) as error:
        Lexer(r'(foo %').tokenize()
    assert str(error.value) == 'invalid syntax'


def test_tokenize_modifier_expression():
    token_list = Lexer(r':foo "bar" :var "null"').tokenize()
    assert token_list[0] == 'PARAMETER<foo>'
    assert token_list[1] == 'STRING<bar>'
    assert token_list[2] == 'PARAMETER<var>'
    assert token_list[3] == 'STRING<null>'


def test_tokenize_query():
    text = '@"/data/source/\nattribute[id=\'x\']" @"/site/title"'
    token_list = Lexer(text).tokenize()
    assert token_list[0] == 'QUERY</data/source/\nattribute[id=\'x\']>'
    assert token_list[1] == 'QUERY</site/title>'


def test_native_query_keyword():
    token_list = Lexer(r'(@ "query")').tokenize()
    assert token_list[1] == tokens.KeywordToken
