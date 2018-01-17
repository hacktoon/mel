from . import nodes
from .exceptions import UnexpectedTokenError


def text_range(first, last=None):
    if last:
        return first.index[0], last.index[1]
    return first.index[0], first.index[1]


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = self._create_node(nodes.Node)
        while not self.stream.is_eof():
            if self.stream.is_current('('):
                expression = self._parse_expression()
                node.add(expression, alias=expression.id.value)
            else:
                node.add(self._parse_value())
        node.text_range = 0, len(self.stream.text)
        return node

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node

    def _parse_expression(self):
        return ExpressionParser(self.stream).parse()

    def _parse_value(self):
        parser_method = {
            '@': self._parse_query,
            '<': self._parse_file,
            '$': self._parse_env,
            '[': self._parse_list,
            'name': self._parse_reference,
            'boolean': self._parse_boolean,
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

    def _parse_query(self):
        node = self._create_node(nodes.QueryNode)
        first = self.stream.read('@')
        if self.stream.is_current('name'):
            node.source = self.stream.read('name')
        node.query = self.stream.read('string')
        node.text_range = text_range(first, node.query)
        return node

    def _parse_file(self):
        node = self._create_node(nodes.FileNode)
        first = self.stream.read('<')
        node.path = self.stream.read('string')
        node.text_range = text_range(first, node.path)
        return node

    def _parse_env(self):
        node = self._create_node(nodes.EnvNode)
        first = self.stream.read('$')
        node.variable = self.stream.read('name')
        node.text_range = text_range(first, node.variable)
        return node

    def _parse_list(self):
        node = self._create_node(nodes.ListNode)
        first = self.stream.read('[')
        while not self.stream.is_current(']'):
            node.add(self._parse_value())
        last = self.stream.read(']')
        node.text_range = text_range(first, last)
        return node

    def _parse_reference(self):
        return ReferenceParser(self.stream).parse()

    def _parse_boolean(self):
        node = self._create_node(nodes.BooleanNode)
        node.token = self.stream.read('boolean')
        node.text_range = text_range(node.token)
        return node

    def _parse_string(self):
        node = self._create_node(nodes.StringNode)
        node.token = self.stream.read('string')
        node.text_range = text_range(node.token)
        return node

    def _parse_float(self):
        node = self._create_node(nodes.FloatNode)
        node.token = self.stream.read('float')
        node.text_range = text_range(node.token)
        return node

    def _parse_int(self):
        node = self._create_node(nodes.IntNode)
        node.token = self.stream.read('int')
        node.text_range = text_range(node.token)
        return node


class ReferenceParser(Parser):
    def parse(self):
        node = self._create_node(nodes.ReferenceNode)
        first, last = self.stream.read('name'), None
        node.add(first)
        while self.stream.is_current('.'):
            self.stream.read('.')
            last = self.stream.read('name')
            node.add(last)
        node.text_range = text_range(first, last)
        return node


class ExpressionParser(Parser):
    def parse(self):
        node = self._create_node(nodes.ExpressionNode)
        first = self.stream.read('(')
        node.id = self.stream.read('name')
        node.attrs = self._parse_attributes()
        self._parse_subnodes(node)
        last = self.stream.read(')')
        if self.stream.is_current('name') and self.stream.is_next(')'):
            self.stream.read('name', expected_value=node.id.value)
            last = self.stream.read(')')
        node.text_range = text_range(first, last)
        return node

    def _parse_attributes(self):
        attrs = {}
        while self.stream.is_current(':'):
            self.stream.read(':')
            attribute = self.stream.read('name')
            value = self._parse_value()
            attrs[attribute.value] = value
        return attrs

    def _parse_subnodes(self, node):
        while not self.stream.is_current(')'):
            if self.stream.is_eof():
                break
            if self.stream.is_current('('):
                expression = self._parse_expression()
                node.add(expression, alias=expression.id.value)
            else:
                node.add(self._parse_value())
