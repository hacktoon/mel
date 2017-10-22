from .data.tokens import TokenType, TOKEN_RULES
from .data.errors import LexingError


class Token:
    def __init__(self, value, type_, line, column):
        self.value = value
        self.line = line
        self.type = type_
        self.column = column

    def __eq__(self, token_repr):
        return str(self) == token_repr

    def __ne__(self, char):
        return str(self) != token_repr

    def __str__(self):
        if str(self.value) in '()[]':
            return self.type.name.upper()
        return '{}<{}>'.format(self.type.name.upper(), self.value)

    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line_index = 0
        self.column_index = 0

    def tokenize(self):
        tokens = []
        ignored_tokens = (
            TokenType.COMMENT,
            TokenType.WHITESPACE,
            TokenType.NEWLINE
        )
        while self.index < len(self.text):
            token = self._create_token()
            if token.type not in ignored_tokens:
                tokens.append(token)
        return tokens

    def _create_token(self):
        for token_regex, type_, get_token_value in TOKEN_RULES:
            match = token_regex.match(self.text, self.index)
            if not match:
                continue
            matched_string = match.group(0)
            match_length = len(matched_string)
            self.index += match_length
            value = get_token_value(matched_string)
            token = Token(value, type_, self.line_index, self.column_index)
            self._update_counters(type_, match_length)
            return token
        else:
            raise LexingError(
                'invalid syntax',
                self.line_index,
                self.column_index
            )

    def _update_counters(self, token_type, match_length):
        if token_type == TokenType.NEWLINE:
            self.line_index += 1
            self.column_index = 0
        else:
            self.column_index += match_length


class TokenStream:
    def __init__(self, text):
        self.tokens = Lexer(text).tokenize()
        self.index = 0

    def consume(self, expected_type):
        token = self.get()
        if token.type != expected_type:
            template = 'expected a {!r}, found a {!r}'
            message = template.format(expected_type.value, token.type.value)
            raise LexingError(message, token.line, token.column)
        self.index += 1
        return token

    def is_eof(self):
        return self.index >= len(self.tokens)

    def get(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return Token('', TokenType.EOF, -1, -1)