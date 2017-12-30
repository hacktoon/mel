import re
from .types import tokens
from .types.errors import LexingError, UnexpectedValueError


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
        for token_type in tokens.types():
            match = token_type.regex.match(self.text, self.index)
            if not match:
                continue
            value = match.group(0)
            token = token_type(value, self.index)
            self.index += len(value)
            return token
        else:
            raise LexingError('invalid syntax')


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
                self.index += 1
                return current_token
        raise UnexpectedValueError(expected_token_id, current_token.id)

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
