import re
import codecs

from .errors import LexingError


NAME_RULE = r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?'
SINGLE_QUOTE_STRING = r"'(?:\\'|[^'])*'"
DOUBLE_QUOTE_STRING = r'"(?:\\"|[^"])*"'
STRING_RULE = '({}|{})'.format(SINGLE_QUOTE_STRING, DOUBLE_QUOTE_STRING)
KEYWORD_RULE = '(' + NAME_RULE + r'|[\?@])'


class Token:
    regex = ''
    skip = False

    def __init__(self, value, line, column):
        self.value = self._process(value)
        self.line = line
        self.column = column

    def _process(self, raw_value):
        return raw_value

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        return isinstance(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return '{}<{}>'.format(self.name.upper(), self.value)

    def __repr__(self):
        return str(self)


class SymbolToken(Token):
    def __str__(self):
        return self.name.upper()


class OpenExpressionToken(SymbolToken):
    name = '('
    regex = r'\('


class CloseExpressionToken(SymbolToken):
    name = ')'
    regex = r'\)(' + KEYWORD_RULE + r'\))?'

    def _process(self, exp):
        if len(exp) > 1:
            return exp.replace(')', '')
        return exp


class OpenListToken(SymbolToken):
    name = '['
    regex = r'\['


class CloseListToken(SymbolToken):
    name = ']'
    regex = r'\]'


class StringToken(Token):
    name = 'String'
    regex = STRING_RULE

    def _process(self, string_literal):
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
        return ESCAPE_SEQUENCE_RE.sub(decode_match, string_literal[1:-1])


class QueryToken(StringToken):
    name = 'Query'
    regex = '@' + STRING_RULE

    def _process(self, query_literal):
        return super()._process(query_literal[1:])


class CommentToken(Token):
    name = 'Comment'
    skip = True
    regex = r'#[^\n\r]*'

    def _process(self, comment_literal):
        return comment_literal[1:]


class WhitespaceToken(Token):
    name = 'Whitespace'
    skip = True
    regex = r'[ ,\t\f\v\x0b\x0c]+'


class NewlineToken(Token):
    name = 'Newline'
    skip = True
    regex = r'\r?\n'


class BooleanToken(Token):
    name = 'Boolean'
    regex = 'true|false'

    def _process(self, boolean_literal):
        return {'true': True, 'false': False}[boolean_literal]


class ParameterToken(Token):
    name = 'Parameter'
    regex = ':' + NAME_RULE

    def _process(self, parameter_literal):
        return super()._process(parameter_literal[1:])


class KeywordToken(Token):
    name = 'Keyword'
    regex = KEYWORD_RULE


class FloatToken(Token):
    name = 'Float'
    regex = r'-?\d+\.\d+\b'

    def _process(self, float_literal):
        return float(float_literal)


class IntToken(Token):
    name = 'Int'
    regex = r'-?\d+\b'

    def _process(self, int_literal):
        return int(int_literal)


class AliasToken(Token):
    name = 'Alias'
    regex = r'@' + NAME_RULE + r'(\s*\.\s*' + NAME_RULE + ')*'

    def _process(self, alias_literal):
        return alias_literal[1:].replace(' ', '')


class EOFToken(Token):
    name = 'EOF'

    def __str__(self):
        return self.name


# the order of tokens is important in this list
TOKEN_TYPES = [
    OpenExpressionToken,
    CloseExpressionToken,
    OpenListToken,
    CloseListToken,
    BooleanToken,
    ParameterToken,
    NewlineToken,
    WhitespaceToken,
    CommentToken,
    QueryToken,
    StringToken,
    AliasToken,
    KeywordToken,
    FloatToken,
    IntToken
]
