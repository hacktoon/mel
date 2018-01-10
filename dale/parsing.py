from . import nodes
from .exceptions import UnexpectedTokenError


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
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
        node = nodes.ListNode()
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

        node.name = self.stream.read('name')
        node.attributes = self._parse_attributes()
        self._parse_subnodes(node)

        self.stream.read(')')
        if self.stream.is_current('name') and self.stream.is_next(')'):
            self.stream.read('name', expected_value=node.name.eval())
            self.stream.read(')')
        return node

    def _parse_attributes(self):
        attributes = {}
        while self.stream.is_current(':'):
            self.stream.read(':')
            attribute = self.stream.read('name').eval()
            value = self._parse_value()
            attributes[attribute] = value
        return attributes

    def _parse_subnodes(self, node):
        while not self.stream.is_current(')'):
            if self.stream.is_eof():
                break
            if self.stream.is_current('('):
                node.add(self._parse_expression())
            else:
                node.add(self._parse_value())
