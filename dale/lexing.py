from . import tokens
from .exceptions import LexingError, UnexpectedTokenError


class Lexer:
    def __init__(self, text):
        self.index = 0
        self.text = text
        self.token_classes = tokens.classes()

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._build_token()
            if not token.skip:
                tokens.append(token)
        return tokens

    def _build_token(self):
        for Token in self.token_classes:
            match = Token.regex.match(self.text, self.index)
            if not match:
                continue
            content = match.group(0)
            index = match.start(), match.end()
            self.index += len(content)
            return Token(content, index)
        else:
            raise LexingError


class TokenStream:
    def __init__(self, text, lexer=Lexer):
        self.tokens = lexer(text).tokenize()
        self.text = text
        self.index = 0

    def read(self, token_id=None):
        current_token = self.current()
        if token_id and not self.is_current(token_id):
            raise UnexpectedTokenError
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
