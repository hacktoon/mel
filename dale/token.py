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
    return build_string(query_literal[1:])


def build_alias(alias_literal):
    return alias_literal[1:].replace(' ', '')


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
        if value in '()[]':
            return self.type.name.upper()
        return '{}<{}>'.format(self.type.name.upper(), self.value)

    def __repr__(self):
        return str(self)


class TokenType(Enum):
    OPEN_EXP = '('
    CLOSE_EXP = ')'
    OPEN_LIST = '['
    CLOSE_LIST = ']'
    COMMENT = 'comment'
    WHITESPACE = 'whitespace'
    PARAMETER = 'parameter'
    KEYWORD = 'keyword'
    NEWLINE = 'newline'
    STRING = 'string'
    BOOLEAN = 'boolean'
    ALIAS = 'alias'
    FLOAT = 'float'
    INT = 'int'
    QUERY = 'query'
    EOF = 'eof'


NAME_RULE = r'[_a-zA-Z]\w*(?:-[_a-zA-Z]\w*)?'
SINGLE_QUOTE_STRING = r"'(?:\\'|[^'])*'"
DOUBLE_QUOTE_STRING = r'"(?:\\"|[^"])*"'
STRING_RULE = '(' + SINGLE_QUOTE_STRING + '|' + DOUBLE_QUOTE_STRING + ')'
ALIAS_RULE = r'@' + NAME_RULE + r'(\s*\.\s*' + NAME_RULE + ')*'

TOKEN_RULES = [
    (rc(r'\('), TokenType.OPEN_EXP, lambda s: s),
    (rc(r'\)'), TokenType.CLOSE_EXP, lambda s: s),
    (rc(r'\['), TokenType.OPEN_LIST, lambda s: s),
    (rc(r'\]'), TokenType.CLOSE_LIST, lambda s: s),
    (rc('true|false'), TokenType.BOOLEAN, build_boolean),
    (rc(r':' + NAME_RULE), TokenType.PARAMETER, lambda s: s[1:]),
    (rc(NAME_RULE + '|\?'), TokenType.KEYWORD, lambda s: s),
    (rc(r'\r?\n'), TokenType.NEWLINE, lambda s: s),
    (rc(r'[ ,\t\f\v\x0b\x0c]+'), TokenType.WHITESPACE, lambda s: s),
    (rc(r'#[^\n\r]*'), TokenType.COMMENT, lambda s: s[1:]),
    (rc('@' + STRING_RULE), TokenType.QUERY, build_query),
    (rc(STRING_RULE), TokenType.STRING, build_string),
    (rc(ALIAS_RULE), TokenType.ALIAS, build_alias),
    (rc(r'-?\d+\.\d+\b'), TokenType.FLOAT, lambda s: float(s)),
    (rc(r'-?\d+\b'), TokenType.INT, lambda s: int(s))
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
