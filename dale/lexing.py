import re
from .data import tokens
from .data.errors import LexingError


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._emit_token()
            if not token.skip:
                tokens.append(token)
        return tokens

    def _emit_token(self):
        for token_type in tokens.TOKEN_TYPES:
            match = re.compile(token_type.regex).match(self.text, self.index)
            if not match:
                continue
            token = token_type(match.group(0), self.index)
            self.index += len(match.group(0))
            return token
        else:
            raise LexingError('invalid syntax', self.index)


class TokenStream:
    def __init__(self, text):
        self.tokens = Lexer(text).tokenize()
        self.index = 0

    def consume(self, expected_token_type):
        token = self.get()
        if isinstance(token, expected_token_type):
            self.index += 1
            return token

        if isinstance(token, tokens.EOFToken):
            token = self.get(-1)
            template = 'expected a {!r} at end of file'
            message = template.format(expected_token_type.id)
            raise LexingError(message, token.index)

        template = 'expected a {!r}, found a {!r}'
        message = template.format(expected_token_type.id, token.id)
        raise LexingError(message, token.index)


    def is_eof(self):
        return self.index >= len(self.tokens)

    def get(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken()
