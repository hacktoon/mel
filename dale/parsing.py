from .types.nodes import *
from .types.errors import ParsingError


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = Node()
        while not self.stream.is_eof():
            if self.stream.is_current('('):
                node.add(self._parse_expression())
            else:
                node.add(self._parse_value())
        return node

    def _parse_expression(self):
        return ExpressionParser(self.stream).parse()

    def _parse_value(self):
        parser_method = {
            '@': self._parse_query,
            '[': self._parse_list,
            'boolean': self._parse_boolean,
            'name': self._parse_reference,
            'string': self._parse_string,
            'float': self._parse_float,
            'int': self._parse_int
        }
        token = self.stream.current()
        try:
            node = parser_method[token.id]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.id)
            raise ParsingError(message)
        return node

    def _parse_list(self):
        node = ListNode()
        self.stream.read('[')
        while not self.stream.is_current(']'):
            if self.stream.is_eof():
                token = self.stream.current()
                raise ParsingError('unexpected EOF while parsing list')
            node.add(self._parse_value())
        self.stream.read(']')
        return node

    def _parse_reference(self):
        node = ReferenceNode()
        node.add(self.stream.read('name'))
        while self.stream.is_current('.'):
            self.stream.read('.')
            node.add(self.stream.read('name'))
        return node

    def _parse_string(self):
        node = StringNode()
        node.add(self.stream.read('string'))
        return node

    def _parse_query(self):
        node = QueryNode()
        self.stream.read('@')
        if self.stream.is_current('name'):
            node.add('source', self.stream.read('name').value)
        else:
            node.add('source', '')
        node.add('content', self.stream.read('string'))
        return node

    def _parse_float(self):
        node = FloatNode()
        node.add(self.stream.read('float'))
        return node

    def _parse_int(self):
        node = IntNode()
        node.add(self.stream.read('int'))
        return node

    def _parse_boolean(self):
        node = BooleanNode()
        node.add(self.stream.read('boolean'))
        return node


class ExpressionParser(Parser):
    def parse(self):
        node = ExpressionNode()
        self.stream.read('(')
        node.add('keyword', self.stream.read('name'))
        node.add('parameters', self._parse_parameters())
        self._parse_values(node)
        self._parse_expression_end(node)
        return node

    def _parse_values(self, node):
        while not self.stream.is_current(')'):
            if self.stream.is_eof():
                break
            if self.stream.is_current('('):
                node.add(self._parse_expression())
            else:
                node.add(self._parse_value())

    def _parse_expression_end(self, node):
        self.stream.read(')')
        if self.stream.is_current('name') and self.stream.is_next(')'):
            self.stream.read('name', value=node.keyword.value)
            self.stream.read(')')

    def _parse_parameters(self):
        node = ParametersNode()
        while self.stream.is_current(':'):
            colon = self.stream.read(':')
            name = self.stream.read('name')
            node.add(name.value, self._parse_value())
        return node