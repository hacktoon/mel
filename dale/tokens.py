import re
import codecs


def types():
    token_types = []
    for cls in Token.__subclasses__():
        token_types.append(cls)
    return sorted(token_types, key=lambda cls: cls.priority, reverse=True)


class Token:
    id = ''
    regex = None
    skip = False
    priority = 0

    def __init__(self, value='', index=-1):
        self.value = value
        self.index = index

    def eval(self, context={}):
        return self.value


class StringToken(Token):
    id = 'string'
    regex = re.compile('|'.join([r"'(?:\\'|[^'])*'", r'"(?:\\"|[^"])*"']))

    def eval(self):
        # source: https://stackoverflow.com/a/24519338/544184
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

        return ESCAPE_SEQUENCE_RE.sub(decode_match, self.value[1:-1])


class FloatToken(Token):
    id = 'float'
    regex = re.compile(r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b')
    priority = 2

    def eval(self):
        return float(self.value)


class IntToken(Token):
    id = 'int'
    regex = re.compile(r'[-+]?\d+\b')
    priority = 1

    def eval(self):
        return int(self.value)


class BooleanToken(Token):
    id = 'boolean'
    regex = re.compile(r'(true|false)\b')
    priority = 2

    def eval(self):
        return {'true': True, 'false': False}[self.value]


class WhitespaceToken(Token):
    id = 'whitespace'
    regex = re.compile(r'[ ,\n\r\t\x0b\x0c]+')
    skip = True


class CommentToken(Token):
    id = 'comment'
    regex = re.compile(r'#[^\n\r]*')
    skip = True


class NameToken(Token):
    id = 'name'
    regex = re.compile(r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?')
    priority = 1


class DotToken(Token):
    id = '.'
    regex = re.compile(r'\.')


class EnvToken(Token):
    id = '$'
    regex = re.compile(r'\$')


class FileToken(Token):
    id = '<'
    regex = re.compile('<')


class AtToken(Token):
    id = '@'
    regex = re.compile('@')


class ColonToken(Token):
    id = ':'
    regex = re.compile(':')


class LeftParenthesisToken(Token):
    id = '('
    regex = re.compile(r'\(')


class RightParenthesisToken(Token):
    id = ')'
    regex = re.compile(r'\)')


class LeftBracketToken(Token):
    id = '['
    regex = re.compile(r'\[')


class RightBracketToken(Token):
    id = ']'
    regex = re.compile(r'\]')


class EOFToken(Token):
    id = 'end of file'
    regex = re.compile(r'\0')
