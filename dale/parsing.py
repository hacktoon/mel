from . import nodes
from .exceptions import UnexpectedTokenError


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = self._create_node(nodes.Node)
        while not self.stream.is_eof():
            if self.stream.is_current('('):
                expression = self._parse_expression()
                node.add(expression, ref=expression.name.value)
            else:
                node.add(self._parse_value())
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
        source = None
        self.stream.read('@')
        if self.stream.is_current('name'):
            source = self.stream.read('name')
        query = self.stream.read('string')
        return nodes.QueryNode(source, query)

    def _parse_file(self):
        self.stream.read('<')
        path = self.stream.read('string')
        return nodes.FileNode(path)

    def _parse_env(self):
        self.stream.read('$')
        variable = self.stream.read('name')
        return nodes.EnvNode(variable)

    def _parse_list(self):
        node = self._create_node(nodes.ListNode)
        self.stream.read('[')
        while not self.stream.is_current(']'):
            node.add(self._parse_value())
        self.stream.read(']')
        return node

    def _parse_reference(self):
        return ReferenceParser(self.stream).parse()

    def _parse_boolean(self):
        value = self.stream.read('boolean')
        return nodes.BooleanNode(value)

    def _parse_string(self):
        value = self.stream.read('string')
        return nodes.StringNode(value)

    def _parse_float(self):
        value = self.stream.read('float')
        return nodes.FloatNode(value)

    def _parse_int(self):
        value = self.stream.read('int')
        return nodes.IntNode(value)


class ReferenceParser(Parser):
    def parse(self):
        node = self._create_node(nodes.ReferenceNode)
        node.add(self.stream.read('name'))
        while self.stream.is_current('.'):
            self.stream.read('.')
            node.add(self.stream.read('name'))
        return node


class ExpressionParser(Parser):
    def parse(self):
        self.stream.read('(')
        name = self.stream.read('name')
        attributes = self._parse_attributes()

        node = nodes.ExpressionNode(name, attributes)

        self._parse_subnodes(node)

        self.stream.read(')')

        if self.stream.is_current('name') and self.stream.is_next(')'):
            self.stream.read('name', expected_value=name.value)
            self.stream.read(')')
        return node

    def _parse_attributes(self):
        attributes = {}
        while self.stream.is_current(':'):
            self.stream.read(':')
            attribute = self.stream.read('name')
            value = self._parse_value()
            attributes[attribute.value] = value
        return attributes

    def _parse_subnodes(self, node):
        while not self.stream.is_current(')'):
            if self.stream.is_eof():
                break
            if self.stream.is_current('('):
                expression = self._parse_expression()
                node.add(expression, ref=expression.name.value)
            else:
                node.add(self._parse_value())
