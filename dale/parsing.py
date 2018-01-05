from . import nodes
from .exceptions import UnexpectedTokenError


class Parser:
    def __init__(self, stream):
        self.stream = stream
        self.context = {}

    def parse(self, context={}):
        node = nodes.Node()
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
            '<': self._parse_file,
            '$': self._parse_env,
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
            expected_values = list(parser_method.keys())
            raise UnexpectedTokenError(token, expected_values)
        return node

    def _parse_list(self):
        node = nodes.Node()
        self.stream.read('[')
        while not self.stream.is_current(']'):
            node.add(self._parse_value())
        self.stream.read(']')
        return node

    def _parse_reference(self):
        node = nodes.ReferenceNode()
        node.add(self.stream.read('name'))
        while self.stream.is_current('.'):
            self.stream.read('.')
            node.add(self.stream.read('name'))
        return node

    def _parse_query(self):
        node = nodes.QueryNode()
        self.stream.read('@')
        if self.stream.is_current('name'):
            node.source = self.stream.read('name')
        node.query = self.stream.read('string')
        return node

    def _parse_file(self):
        node = nodes.FileNode()
        self.stream.read('<')
        node.path = self.stream.read('string')
        return node

    def _parse_env(self):
        node = nodes.EnvNode()
        self.stream.read('$')
        node.variable = self.stream.read('name')
        return node

    def _parse_string(self):
        node = nodes.StringNode()
        node.value = self.stream.read('string')
        return node

    def _parse_float(self):
        node = nodes.FloatNode()
        node.value = self.stream.read('float')
        return node

    def _parse_int(self):
        node = nodes.IntNode()
        node.value = self.stream.read('int')
        return node

    def _parse_boolean(self):
        node = nodes.BooleanNode()
        node.value = self.stream.read('boolean')
        return node


class ExpressionParser(Parser):
    def parse(self):
        node = nodes.ExpressionNode()
        self.stream.read('(')

        node.keyword = self.stream.read('name')
        node.parameters = self._parse_parameters()
        node.values = self._parse_values()

        self.stream.read(')')
        if self.stream.is_current('name') and self.stream.is_next(')'):
            self.stream.read('name', expected_value=node.keyword.value)
            self.stream.read(')')
        return node

    def _parse_values(self):
        values = []
        while not self.stream.is_current(')'):
            if self.stream.is_eof():
                break
            if self.stream.is_current('('):
                values.append(self._parse_expression())
            else:
                values.append(self._parse_value())
        return values

    def _parse_parameters(self):
        parameters = {}
        while self.stream.is_current(':'):
            self.stream.read(':')
            attribute = self.stream.read('name')
            value = self._parse_value()
            parameters[attribute.value] = value
        return parameters
