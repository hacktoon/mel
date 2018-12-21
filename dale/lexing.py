from . import tokens
from .exceptions import InvalidSyntaxError, UnexpectedTokenError


class Lexer:
    def __init__(self, text):
        self.index = 0
        self.text = text
        self.token_classes = tokens.classes()

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._build_token()
            if not token:
                raise InvalidSyntaxError(self.index)
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
        return


class TokenStream:
    def __init__(self, text, lexer=Lexer):
        self.tokens = lexer(text).tokenize()
        self.text = text
        self.index = 0

    def read(self, token_id=None):
        current = self.current()
        if token_id and not self.is_current(token_id):
            raise UnexpectedTokenError(current.index[0])
        self.index += 1
        return current

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        return self.current().id == token_id

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken()
