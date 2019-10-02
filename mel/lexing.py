from . import tokens
from .exceptions import ParsingError


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 0
        self.column = 0

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self.lex()
            if not token.skip:
                _tokens.append(token)
        return _tokens

    def lex(self):
        for Token in tokens.subclasses():
            match = Token.regex.match(self.text, self.index)
            if match:
                return self.build_token(Token, match.span())
        raise ParsingError(self.build_token())

    def build_token(self, Token=tokens.Token, index=None):
        index = index or (self.index, self.index)
        token = Token(self.text, index)
        return token


class TokenStream:
    def __init__(self, text, Lexer=Lexer):
        self.lexer = Lexer(text)
        self.tokens = self.lexer.tokenize()
        self.text = text
        self.index = 0

    def save(self):
        return self.index

    def restore(self, index):
        self.index = index

    def read(self, token=None):
        current = self.peek()
        if token and not self.is_next(token):
            if self.is_eof():
                self.error(ParsingError, self.peek(-1))
            self.error(ParsingError)
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
            return self.lexer.build_token()

    def error(self, Error, token=None):
        raise Error(token or self.peek())
