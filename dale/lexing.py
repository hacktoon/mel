import re
from .types import tokens
from .types.errors import LexingError


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

    def read(self, token_id, value=None):
        token = self.current()
        if self.is_current(token_id):
            if value:
                if value == token.value:
                    self.index += 1
                    return token
            else:
                self.index += 1
                return token

        template = 'expected a token of type {}, but found {}'
        message = template.format(token_id, token.id)
        raise LexingError(message, token.index)

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        Token = getattr(tokens, token_id + 'Token')
        return isinstance(self.current(), Token)

    def is_next(self, token_id, offset=1):
        Token = getattr(tokens, token_id + 'Token')
        return isinstance(self.current(offset=offset), Token)

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return tokens.EOFToken()
