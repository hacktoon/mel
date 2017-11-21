import pytest
from dale.lexing import TokenStream
from dale.data import tokens
from dale.data.errors import LexingError


def test_stream_get_current_token():
    stream = TokenStream('345 name ()')
    assert stream.get().value() == 345


def test_stream_consume_token():
    stream = TokenStream('42 foo')
    int_token = stream.consume(tokens.IntToken)
    assert int_token.value() == 42
    id_token = stream.consume(tokens.KeywordToken)
    assert id_token.value() == 'foo'


def test_that_consume_unexpected_token_raises_error():
    stream = TokenStream('"string"')
    with pytest.raises(LexingError):
        stream.consume(tokens.IntToken)


def test_stream_ends_with_eof_token():
    stream = TokenStream('(age 5)')
    stream.consume(tokens.OpenExpressionToken)
    stream.consume(tokens.KeywordToken)
    assert not stream.is_eof()
    stream.consume(tokens.IntToken)
    stream.consume(tokens.CloseExpressionToken)
    assert stream.is_eof()
    assert isinstance(stream.get(), tokens.EOFToken)
