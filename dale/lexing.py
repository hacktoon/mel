import re

from . import tokens
from .exceptions import (
    InvalidSyntaxError,
    UnexpectedTokenError,
    UnexpectedEOFError
)


class Lexer:
    def __init__(self, text):
        self.index = 0
        self.line = 1
        self.column = 0
        self.text = text
        self.token_classes = tokens.classes()

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self.lex()
            self.index += len(token)
            self.column += len(token)
            if token.newline:
                _, end = re.split(tokens.NewlineToken.regex, token.value)
                self.column = len(end) + 1 if end else 0
                self.line += 1
            if not token.skip:
                _tokens.append(token)
        return _tokens

    def lex(self):
        for Token in self.token_classes:
            match = Token.regex.match(self.text, self.index)
            if not match:
                continue
            index = match.start(), match.end()
            token = Token(match.group(0), index)
            token.line = self.line
            token.column = self.column
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
