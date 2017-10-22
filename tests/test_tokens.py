import pytest
from dale.lexing import TokenStream
from dale.data.tokens import TokenType
from dale.data.errors import LexingError


def test_stream_get_current_token():
    stream = TokenStream('345 name ()')
    assert stream.get() == 'INT<345>'


def test_stream_consume_token():
    stream = TokenStream('42 foo')
    int_token = stream.consume(TokenType.INT)
    assert int_token == 'INT<42>'
    id_token = stream.consume(TokenType.KEYWORD)
    assert id_token == 'KEYWORD<foo>'


def test_that_consume_unexpected_token_raises_error():
    stream = TokenStream('"string"')
    with pytest.raises(LexingError):
        stream.consume(TokenType.INT)


def test_stream_ends_with_eof_token():
    stream = TokenStream('(age 5)')
    stream.consume(TokenType.OPEN_EXP)
    stream.consume(TokenType.KEYWORD)
    assert not stream.is_eof()
    stream.consume(TokenType.INT)
    stream.consume(TokenType.CLOSE_EXP)
    assert stream.is_eof()
    assert stream.get() == 'EOF'
