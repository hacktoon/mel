from mel.lexing.token import Token


def test_token_parsers():
    parsers = Token.parsers('-')
    assert len(parsers) == 2
