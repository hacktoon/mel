from . import tokens
from .exceptions import (
    InvalidSyntaxError,
    UnexpectedTokenError,
    UnexpectedEOFError
)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 0

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self.lex()
            self._update_counters(token)
            if not token.skip:
                _tokens.append(token)
        return _tokens

    def lex(self):
        for Token in tokens.subclasses():
            match = Token.regex.match(self.text, self.index)
            if not match:
                continue
            token = Token(self.text, match.span())
            token.line = self.line
            token.column = self.column
            return token
        token = self._build_null_token()
        raise InvalidSyntaxError(token)

    def _build_null_token(self):
        token = tokens.NullToken(self.text, (self.index,) * 2)
        token.line = self.line
        token.column = self.column
        return token

    def _update_counters(self, token):
        self.index += len(token)
        self.column += len(token)
        if not token.newline:
            return
        lines = token.value.splitlines()
        *_, end = lines
        self.column = len(end) + 1 if end else 0
        self.line += max(1, len(lines) - 1)


class TokenStream:
    def __init__(self, text, lexer=Lexer):
        self.tokens = lexer(text).tokenize()
        self.text = text
        self.index = 0

    def read(self, token=None):
        current = self.peek()
        if token and not self.is_next(token):
            if self.is_eof():
                raise UnexpectedEOFError(current)
            raise UnexpectedTokenError(current)
        self.index += 1
        return current

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_next(self, token):
        return self.peek() == token

    def peek(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            index = (self.index,) * 2
            return tokens.NullToken(index=index)
