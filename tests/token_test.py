import pytest
from dale.error import SyntaxError
from dale.lexer import Lexer
from dale.token import TokenType, TokenStream


def build_stream(text):
    return TokenStream(Lexer(text).tokenize())


def test_stream_get_current_token():
    stream = build_stream('345 name ()')
    assert stream.get() == 'INT<345>'


def test_stream_consume_token():
    stream = build_stream('42 foo')
    int_token = stream.consume(TokenType.INT)
    assert int_token == 'INT<42>'
    id_token = stream.consume(TokenType.KEYWORD)
    assert id_token == 'KEYWORD<foo>'


def test_that_consume_unexpected_token_raises_error():
    stream = build_stream('"string"')
    with pytest.raises(SyntaxError):
        stream.consume(TokenType.INT)


def test_stream_ends_with_eof_token():
    stream = build_stream('(age 5)')
    stream.consume(TokenType.OPEN_EXP)
    stream.consume(TokenType.KEYWORD)
    assert not stream.is_eof()
    stream.consume(TokenType.INT)
    stream.consume(TokenType.CLOSE_EXP)
    assert stream.is_eof()
    assert stream.get() == 'EOF'
