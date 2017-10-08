import re
import codecs
import string
from enum import Enum
from .error import SyntaxError


rc = re.compile


# thanks to @rspeer in https://stackoverflow.com/a/24519338/544184
def build_string(string_literal):
    ESCAPE_SEQUENCE_RE = re.compile(r'''
        \\( U........    # 8-digit hex escapes
        | u....          # 4-digit hex escapes
        | x..            # 2-digit hex escapes
        | [0-7]{1,3}     # Octal escapes
        | N\{[^}]+\}     # Unicode characters by name
        | [\\'"abfnrtv]  # Single-character escapes
        )''', re.VERBOSE)

    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')
    return ESCAPE_SEQUENCE_RE.sub(decode_match, string_literal[1:-1])


def build_boolean(boolean_literal):
    return {'true': True, 'false': False}[boolean_literal]


def build_query(query_literal):
    return re.sub('^\{\{|\}\}$', '', query_literal)


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
        value = str(self.value)
        if value in string.punctuation or value.isspace():
            return self.type.name.upper()
        return '{}({})'.format(self.type.name.upper(), self.value)

    def __repr__(self):
        return str(self)


class TokenType(Enum):
    OPEN_EXP = '('
    CLOSE_EXP = ')'
    OPEN_PARAM = '{'
    CLOSE_PARAM = '}'
    OPEN_LIST = '['
    CLOSE_LIST = ']'
    COMMENT = 'comment'
    WHITESPACE = 'whitespace'
    NEWLINE = 'newline'
    COMMA = ','
    COLON = ':'
    DOT = '.'
    STRING = 'string'
    BOOLEAN = 'boolean'
    IDENTIFIER = 'identifier'
    FLOAT = 'float'
    INT = 'int'
    QUERY = 'query'
    EOF = 'eof'


TOKEN_RULES = [
    (rc(r'\('), TokenType.OPEN_EXP, lambda s: s),
    (rc(r'\)'), TokenType.CLOSE_EXP, lambda s: s),
    (rc(r'\{\{.+?\}\}', re.DOTALL), TokenType.QUERY, build_query),
    (rc(r'\{'), TokenType.OPEN_PARAM, lambda s: s),
    (rc(r'\}'), TokenType.CLOSE_PARAM, lambda s: s),
    (rc(r'\['), TokenType.OPEN_LIST, lambda s: s),
    (rc(r'\]'), TokenType.CLOSE_LIST, lambda s: s),
    (rc(','), TokenType.COMMA, lambda s: s),
    (rc(':'), TokenType.COLON, lambda s: s),
    (rc(r'\r?\n'), TokenType.NEWLINE, lambda s: s),
    (rc(r'[ \t\f\v\x0b\x0c]+'), TokenType.WHITESPACE, lambda s: s),
    (rc(r'#[^\n\r]*'), TokenType.COMMENT, lambda s: s[1:]),
    (rc(r'"(?:\\"|[^"])*"'), TokenType.STRING, build_string),
    (rc(r"'(?:\\'|[^'])*'"), TokenType.STRING, build_string),
    (rc('true|false'), TokenType.BOOLEAN, build_boolean),
    (rc(r'[_a-zA-Z]\w*(?:-\w+)?'), TokenType.IDENTIFIER, lambda s: s),
    (rc(r'-?\d+\.\d+\b'), TokenType.FLOAT, lambda s: float(s)),
    (rc(r'-?\d+\b'), TokenType.INT, lambda s: int(s)),
    (rc(r'\b\.\b'), TokenType.DOT, lambda s: s)
]


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def consume(self, expected_type):
        token = self.get()
        if token.type != expected_type:
            template = 'expected a {!r}, found a {!r}'
            message = template.format(expected_type.value, token.type.value)
            raise SyntaxError(message, token.line, token.column)
        self.index += 1
        return token

    def is_eof(self):
        return self.index >= len(self.tokens)

    def get(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return Token('', TokenType.EOF, -1, -1)
