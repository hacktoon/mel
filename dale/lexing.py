from . import tokens
from .exceptions import (
    LexingError,
    UnexpectedTokenError,
    UnexpectedTokenValueError
)


class Lexer:
    def __init__(self):
        self.index = 0

    def tokenize(self, text):
        _tokens = []
        while self.index < len(text):
            token = self._build_token(text)
            if token.skip:
                continue
            _tokens.append(token)
        return _tokens

    def _build_token(self, text):
        for Token in tokens.classes():
            match = Token.regex.match(text, self.index)
            if not match:
                continue
            text = match.group(0)
            index = match.start(), match.end()
            token = Token(text, index)
            self.index += len(text)
            return token
        else:
            raise LexingError(self.index)


class TokenStream:
    def __init__(self, text, lexer=Lexer):
        self.tokens = lexer().tokenize(text)
        self.text = text
        self.index = 0

    def read(self, expected_token_id, expected_value=None):
        current_token = self.current()
        if not self.is_current(expected_token_id):
            raise UnexpectedTokenError(current_token, expected_token_id)

        if expected_value:
            if expected_value == current_token.value:
                self.index += 1
                return current_token
            else:
                raise UnexpectedTokenValueError(
                    current_token,
                    expected_token_id,
                    expected_value
                )
        else:
            self.index += 1
            return current_token

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        return self.current().id == token_id

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken()
