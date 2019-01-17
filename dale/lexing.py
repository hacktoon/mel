from . import tokens
from .exceptions import (
    InvalidSyntaxError,
    UnexpectedTokenError,
    UnexpectedEOFError
)


class Lexer:
    def __init__(self, text):
        self.index = 0
        self.text = text
        self.token_classes = tokens.classes()

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._build_token()
            self.index += len(token)
            if not token.skip:
                tokens.append(token)
        return tokens

    def _build_token(self):
        for Token in self.token_classes:
            match = Token.regex.match(self.text, self.index)
            if not match:
                continue
            index = match.start(), match.end()
            token = Token(match.group(0), index)
            return token
        raise InvalidSyntaxError(self.index)


class TokenStream:
    def __init__(self, text, lexer=Lexer):
        self.tokens = lexer(text).tokenize()
        self.text = text
        self.index = 0

    def read(self, token_id=None):
        current = self.peek()
        if token_id and not self.is_next(token_id):
            if self.is_eof():
                raise UnexpectedEOFError(self.index)
            raise UnexpectedTokenError(current.index[0])
        self.index += 1
        return current

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_next(self, token_id):
        return self.peek().id == token_id

    def peek(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken()
