import re
import codecs
from dale.types.errors import ParsingError
from collections import namedtuple

Position = namedtuple('Position', 'start, end, line, column')


class Node:
    priority = 0
    skip = False

    def __init__(self, stream):
        self._children = []
        self._parameters = {}
        self.stream = stream
        self.position = Position(0, 0, 0, 0)

    def match(self, node):
        token = self.stream.read(node.id)
        self.add(token)

    def add(self, *args):
        if len(args) == 2:
            key, child = args
            self.__dict__[key] = child
            self._parameters[key] = child
            self._children.append(child)
        else:
            self._children.append(args[0])
        self.update_position()

    def update_position(self):
        self.position = Position(
            start  = self._children[0].position.start,
            end    = self._children[-1].position.end,
            line   = self._children[0].position.line,
            column = self._children[0].position.column
        )

    @property
    def value(self):
        if len(self._children) == 1:
            return self._children[0].value
        return [child.value for child in self._children]

    def __getitem__(self, key):
        try:
            return self._parameters.get(key, self._children[key])
        except (KeyError, IndexError):
            raise ValueError(key + ' is not a valid key or index')

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        start = self._children[0].position.start
        end = self._children[-1].position.end
        return self.stream.text[start:end]
        
    def __str__(self):
        return repr(self)


class Dot(Node):
    id = '.'
    regex = r'\.'


class At(Node):
    id = '@'
    regex = '@'


class Colon(Node):
    id = ':'
    regex = ':'


class LeftParenthesis(Node):
    id = '('
    regex = r'\('


class RightParenthesis(Node):
    id = ')'
    regex = r'\)'


class LeftBracket(Node):
    id = '['
    regex = r'\['


class RightBracket(Node):
    id = ']'
    regex = r'\]'


class Whitespace(Node):
    id = 'whitespace'
    regex = r'[ ,\t\x0b\x0c]+'
    skip = True


class Newline(Node):
    id = 'newline'
    regex = r'[\r\n]+'
    skip = True


class Comment(Node):
    id = 'comment'
    regex = r'#[^\n\r]*'
    skip = True


class Name(Node):
    id = 'name'
    regex = r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?'
    priority = 1


class Expression(Node):
    def __init__(self, stream):
        super().__init__(stream)
        self.keyword = None
        self.parameters = None

    @property
    def value(self):
        exp = {'keyword': self.keyword.value}
        if self.parameters.value.items():
            exp['parameters'] = self.parameters.value
        exp['values'] = [child.value for child in self._children[3:-1]]
        return exp


class Parameters(Node):
    @property
    def value(self):
        params = self._parameters.items()
        return {key.value:child.value for key, child in params}


class Query(Node):
    def __init__(self, stream):
        super().__init__(stream)
        self.source = None
        self.content = None

    @property
    def value(self):
        if self.source and self.source.value == 'file':
            try:
                with open(self.content.value, 'r') as file_obj:
                    return file_obj.read()
            except IOError as e:
               raise ParsingError("I/O error: {}".format(e))
            except:
               raise ParsingError("Unexpected error")
        else:
            return self.content.value


class Reference(Node):
    pass


class String(Node):
    id = 'string'
    regex = r'|'.join([r"'(?:\\'|[^'])*'", r'"(?:\\"|[^"])*"'])

    @property
    def value(self):
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

        value = self._children[0].value
        return ESCAPE_SEQUENCE_RE.sub(decode_match, value[1:-1])


class Int(Node):
    id = 'int'
    priority = 1
    regex = r'[-+]?\d+\b'

    @property
    def value(self):
        return int(self._children[0].value)


class Float(Node):
    id = 'float'
    priority = 2
    regex = r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b'

    @property
    def value(self):
        return float(self._children[0].value)


class Boolean(Node):
    id = 'boolean'
    regex = r'(true|false)\b'
    priority = 2

    @property
    def value(self):
        mapping = {'true': True, 'false': False}
        return mapping[self._children[0].value]


class List(Node):
    @property
    def value(self):
        return [child.value for child in self._children[1:-1]]