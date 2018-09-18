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
        node = self._create_node(nodes.RootNode)
        while not self.stream.is_eof():
            node.add(self._parse_reference())
        node.text_range = 0, len(self.stream.text)
        return node

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node

    def _parse_reference(self):
        node = self._create_node(nodes.ReferenceNode)
        first = last = self._parse_value()
        while self.stream.is_current('/'):
            self.stream.read('/')
            last = self._parse_value()
            node.add(last)
        node.text_range = text_range(first, last)
        return node

    def _parse_value(self):
        parser_methods = [
            self._parse_literal,
            self._parse_property,
            self._parse_scope,
            self._parse_query,
            self._parse_list,
            self._parse_class
        ]
        for parser_method in parser_methods:
            try:
                return parser_method()
            except UnexpectedTokenError:  # TODO generalize error
                pass
        else:
            raise UnexpectedTokenError

    def _parse_literal(self):
        literal_nodes = {
            'boolean': nodes.BooleanNode,
            'string': nodes.StringNode,
            'float': nodes.FloatNode,
            'int': nodes.IntNode
        }
        literal_token = self.stream.current()
        if literal_token.id in literal_nodes:
            Node = literal_nodes[literal_token.id]
        else:
            expected_values = list(literal_nodes.keys())
            raise UnexpectedTokenError(literal_token, expected_values)
        node = self._create_node(Node)
        node.token = literal_token
        node.text_range = text_range(literal_token)
        return node

    def _parse_property(self):
        prefix_node_map = {
            '#': nodes.UIDNode,
            '!': nodes.FlagNode,
            '@': nodes.AttributeNode,
            '%': nodes.FormatNode,
            '~': nodes.AliasNode,
            '?': nodes.DocNode
        }
        prefix = self.stream.current()
        Node = prefix_node_map.get(prefix.id, nodes.PropertyNode)
        node = self._create_node(Node)
        node.name = self.stream.read('name')
        node.text_range = text_range(prefix, node.name)
        return node

    def _parse_scope(self):
        node = self._create_node(nodes.ScopeNode)
        first = self.stream.read('(')
        if not self.stream.is_current(')'):
            node.key = self._parse_reference()
        while not self.stream.is_current(')'):
            node.add(self._parse_reference())
        last = self.stream.read(')')
        node.text_range = text_range(first, last)
        return node

    def _parse_query(self):
        node = self._create_node(nodes.QueryNode)
        first = self.stream.read('{')
        if not self.stream.is_current('}'):
            node.key = self._parse_reference()
        while not self.stream.is_current('}'):
            node.add(self._parse_reference())
        last = self.stream.read('}')
        node.text_range = text_range(first, last)
        return node

    def _parse_list(self):
        node = self._create_node(nodes.ListNode)
        first = self.stream.read('[')
        while not self.stream.is_current(']'):
            node.add(self._parse_reference())
        last = self.stream.read(']')
        node.text_range = text_range(first, last)
        return node

    def _parse_class(self):
        pass
