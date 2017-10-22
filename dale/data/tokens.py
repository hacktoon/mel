import re
import codecs
import string
from enum import Enum
from .errors import LexingError


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
KEYWORD_RULE = NAME_RULE + r'|\?'

TOKEN_RULES = [
    (rc(r'\('), TokenType.OPEN_EXP, lambda s: s),
    (rc(r'\)(?:'+ KEYWORD_RULE +'\))?'), TokenType.CLOSE_EXP, lambda s: s),
    (rc(r'\['), TokenType.OPEN_LIST, lambda s: s),
    (rc(r'\]'), TokenType.CLOSE_LIST, lambda s: s),
    (rc('true|false'), TokenType.BOOLEAN, build_boolean),
    (rc(r':' + NAME_RULE), TokenType.PARAMETER, lambda s: s[1:]),
    (rc(KEYWORD_RULE), TokenType.KEYWORD, lambda s: s),
    (rc(r'\r?\n'), TokenType.NEWLINE, lambda s: s),
    (rc(r'[ ,\t\f\v\x0b\x0c]+'), TokenType.WHITESPACE, lambda s: s),
    (rc(r'#[^\n\r]*'), TokenType.COMMENT, lambda s: s[1:]),
    (rc('@' + STRING_RULE), TokenType.QUERY, build_query),
    (rc(STRING_RULE), TokenType.STRING, build_string),
    (rc(ALIAS_RULE), TokenType.ALIAS, build_alias),
    (rc(r'-?\d+\.\d+\b'), TokenType.FLOAT, lambda s: float(s)),
    (rc(r'-?\d+\b'), TokenType.INT, lambda s: int(s))
]



