import re
from .data import tokens
from .data.errors import LexingError


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []
        while self.index < len(self.text):
            token = self._produce_token()
            if token.skip:
                continue
            tokens.append(token)
        return tokens

    def _produce_token(self):
        for Token in tokens.TOKEN_TYPES:
            match = re.compile(Token.regex).match(self.text, self.index)
            if not match:
                continue
            matched_text = match.group(0)
            token = Token(matched_text, self.line, self.column)
            self._update_counters(Token, len(matched_text))
            return token
        else:
            raise LexingError('invalid syntax', self.line, self.column)

    def _update_counters(self, token_type, match_length):
        self.index += match_length
        if token_type == tokens.NewlineToken:
            self.line += 1
            self.column = 1
        else:
            self.column += match_length


class TokenStream:
    def __init__(self, text):
        self.tokens = Lexer(text).tokenize()
        self.index = 0

    def consume(self, expected_type):
        token = self.get()
        if isinstance(token, expected_type):
            self.index += 1
            return token

        if token == tokens.EOFToken:
            token = self.get(-1)
            template = 'expected a {!r} at end of file'
            message = template.format(expected_type.name)
            column = token.column + len(token) - 1
            raise LexingError(message, token.line, column)

        template = 'expected a {!r}, found a {!r}'
        message = template.format(expected_type.name, token.name)
        raise LexingError(message, token.line, token.column)

    def is_eof(self):
        return self.index >= len(self.tokens)

    def get(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken('', -1, -1)
