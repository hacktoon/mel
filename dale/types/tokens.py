import re
import codecs

from .errors import LexingError


NAME_RULE = r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?'
SINGLE_QUOTE_STRING = r"'(?:\\'|[^'])*'"
DOUBLE_QUOTE_STRING = r'"(?:\\"|[^"])*"'
STRING_RULE = '({}|{})'.format(SINGLE_QUOTE_STRING, DOUBLE_QUOTE_STRING)


class Token:
    id = ''
    regex = ''
    skip = False

    def __init__(self, match='', index=0):
        self.match = match
        self.index = index

    def value(self, context=None):
        return self.match

    def __repr__(self):
        return self.match

    def __str__(self):
        return self.match


class WhitespaceToken(Token):
    id = 'Whitespace'
    regex = r'[,\s]+'
    skip = True


class CommentToken(Token):
    id = 'Comment'
    regex = r'#[^\n\r]*'
    skip = True

    def value(self):
        return self.match[1:]


class DotToken(Token):
    id = 'Dot'
    regex = r'\.'


class LeftBracketToken(Token):
    id = 'LeftBracket'
    regex = r'\['


class RightBracketToken(Token):
    id = 'RightBracket'
    regex = r'\]'


class LeftParenToken(Token):
    id = 'LeftParen'
    regex = r'\('


class RightParenToken(Token):
    id = 'RightParen'
    regex = r'\)(' + NAME_RULE + r'\))?'

    def value(self):
        if len(self.match) > 1:
            return self.match.replace(')', '')
        return self.match


class StringToken(Token):
    id = 'String'
    regex = STRING_RULE

    def value(self):
        # thanks to @rspeer at https://stackoverflow.com/a/24519338/544184
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
        return ESCAPE_SEQUENCE_RE.sub(decode_match, self.match[1:-1])


class QueryToken(Token):
    id = 'Query'
    regex = '@'


class BooleanToken(Token):
    id = 'Boolean'
    regex = 'true|false'

    def value(self):
        return {'true': True, 'false': False}[self.match]


class ParameterToken(Token):
    id = 'Parameter'
    regex = ':' + NAME_RULE

    def value(self):
        return self.match[1:]


class NameToken(Token):
    id = 'Name'
    regex = NAME_RULE


class FloatToken(Token):
    id = 'Float'
    regex = r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b'

    def value(self):
        return float(self.match)


class IntToken(Token):
    id = 'Int'
    regex = r'[-+]?\d+\b'

    def value(self):
        return int(self.match)


class EOFToken(Token):
    id = 'end of file'


# the order of tokens is important in this list
TOKEN_TYPES = [
    LeftBracketToken,
    RightBracketToken,
    LeftParenToken,
    RightParenToken,
    DotToken,
    ParameterToken,
    BooleanToken,
    NameToken,
    WhitespaceToken,
    CommentToken,
    QueryToken,
    StringToken,
    FloatToken,
    IntToken
]
