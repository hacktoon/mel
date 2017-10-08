from .token import Token, TokenType, TOKEN_RULES
from .error import SyntaxError


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
            raise SyntaxError(
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
