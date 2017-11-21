import re
import codecs

from .errors import LexingError


NAME_RULE = r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?'
SINGLE_QUOTE_STRING = r"'(?:\\'|[^'])*'"
DOUBLE_QUOTE_STRING = r'"(?:\\"|[^"])*"'
STRING_RULE = '({}|{})'.format(SINGLE_QUOTE_STRING, DOUBLE_QUOTE_STRING)
KEYWORD_RULE = '(' + NAME_RULE + r'|[:?@])'


class Token:
    id = ''
    regex = ''
    skip = False

    def __init__(self, match='', index=0, source_text=''):
        self.match = match
        self.index = index

    def value(self, context=None):
        return self.match

    def __repr__(self):
        return self.match

    def __str__(self):
        return self.match


class WhitespaceToken(Token):
    id = 'whitespace'
    regex = r'[,\s]+'
    skip = True


class CommentToken(Token):
    id = 'comment'
    regex = r'#[^\n\r]*'
    skip = True

    def value(self):
        return self.match[1:]


class OpenListToken(Token):
    id = '['
    regex = r'\['


class CloseListToken(Token):
    id = ']'
    regex = r'\]'


class StartExpressionToken(Token):
    id = '('
    regex = r'\('


class EndExpressionToken(Token):
    id = ')'
    regex = r'\)(' + KEYWORD_RULE + r'\))?'

    def value(self):
        if len(self.match) > 1:
            return self.match.replace(')', '')
        return self.match


class StringToken(Token):
    id = 'string'
    regex = STRING_RULE

    def value(self):
        # thanks to @rspeer in https://stackoverflow.com/a/24519338/544184
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


class QueryToken(StringToken):
    id = 'query'
    regex = '@' + STRING_RULE

    def value(self):
        return super().value()[1:]


class BooleanToken(Token):
    id = 'boolean'
    regex = 'true|false'

    def value(self):
        return {'true': True, 'false': False}[self.match]


class ParameterToken(Token):
    id = 'parameter'
    regex = ':' + NAME_RULE

    def value(self):
        return self.match[1:]


class KeywordToken(Token):
    id = 'keyword'
    regex = KEYWORD_RULE


class FloatToken(Token):
    id = 'float'
    regex = r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b'

    def value(self):
        return float(self.match)


class IntToken(Token):
    id = 'int'
    regex = r'[-+]?\d+\b'

    def value(self):
        return int(self.match)


class ReferenceToken(Token):
    id = 'reference'
    regex = r'@' + NAME_RULE + r'(\s*\.\s*' + NAME_RULE + ')*'

    def value(self):
        strip_whitespaces = lambda value: re.sub('\s+', '', value)
        return strip_whitespaces(self.match[1:]).split('.')


class EOFToken(Token):
    id = 'end of file'


# the order of tokens is important in this list
TOKEN_TYPES = [
    OpenListToken,
    CloseListToken,
    StartExpressionToken,
    EndExpressionToken,
    BooleanToken,
    ParameterToken,
    WhitespaceToken,
    CommentToken,
    QueryToken,
    StringToken,
    ReferenceToken,
    KeywordToken,
    FloatToken,
    IntToken
]
