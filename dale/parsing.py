from .types.nodes import *
from .types.errors import ParsingError


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = self._build_node(Node)
        while not self.stream.is_eof():
            if self.stream.is_current('('):
                node.add(self._parse_expression())
            else:
                node.add(self._parse_value())
        return node

    def _build_node(self, cls):
        return cls(self.stream)

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
        node = self._build_node(ListNode)
        node.add(self.stream.read('['))
        while not self.stream.is_current(']'):
            if self.stream.is_eof():
                raise ParsingError('unexpected EOF while parsing list')
            node.add(self._parse_value())
        node.add(self.stream.read(']'))
        return node

    def _parse_reference(self):
        node = self._build_node(ReferenceNode)
        node.add(self.stream.read('name'))
        while self.stream.is_current('.'):
            self.stream.read('.')
            node.add(self.stream.read('name'))
        return node

    def _parse_string(self):
        node = self._build_node(StringNode)
        node.add(self.stream.read('string'))
        return node

    def _parse_query(self):
        node = self._build_node(QueryNode)
        node.add(self.stream.read('@'))
        if self.stream.is_current('name'):
            node.add('source', self.stream.read('name'))
        node.add('content', self.stream.read('string'))
        return node

    def _parse_float(self):
        node = self._build_node(FloatNode)
        node.add(self.stream.read('float'))
        return node

    def _parse_int(self):
        node = self._build_node(IntNode)
        node.add(self.stream.read('int'))
        return node

    def _parse_boolean(self):
        node = self._build_node(BooleanNode)
        node.add(self.stream.read('boolean'))
        return node


class ExpressionParser(Parser):
    def parse(self):
        node = self._build_node(ExpressionNode)
        node.add(self.stream.read('('))
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
        node.add(self.stream.read(')'))
        if self.stream.is_current('name') and self.stream.is_next(')'):
            node.add(self.stream.read('name', value=node.keyword.value))
            node.add(self.stream.read(')'))

    def _parse_parameters(self):
        node = self._build_node(ParametersNode)
        while self.stream.is_current(':'):
            node.add(self.stream.read(':'))
            name = self.stream.read('name')
            node.add(name)
            node.add(name, self._parse_value())
        return node