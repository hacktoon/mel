from . import tokens
from .exceptions import (
    InvalidSyntaxError,
    UnexpectedTokenError,
    UnexpectedTokenValueError
)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self._build_token()
            if token.skip:
                continue
            _tokens.append(token)
        return _tokens

    def _build_token(self):
        for Token in tokens.classes():
            match = Token.regex.match(self.text, self.index)
            if not match:
                continue
            value = match.group(0)
            token = Token(value, self.index)
            self.index += len(value)
            return token
        else:
            raise InvalidSyntaxError(self.index)


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def read(self, expected_token_id, expected_value=None):
        current_token = self.current()
        if self.is_current(expected_token_id):
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
        raise UnexpectedTokenError(current_token, expected_token_id)

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        return self.current().id == token_id

    def is_next(self, token_id):
        return self.current(offset=1).id == token_id

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken('', -1)
