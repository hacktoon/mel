from .. import nodes
from ..exceptions import UnexpectedTokenError

from .decorators import indexed
from .scopes import ScopeParser
from .values import ValueParser
from .base import BaseParser


class Parser(BaseParser):
    @indexed
    def parse(self):
        node = self._create_node(nodes.Node)
        while not self.stream.is_eof():
            reference = self.parse_value()
            if reference:
                node.add(reference)
            elif not self.stream.is_eof():
                raise UnexpectedTokenError(self.stream.current())
        return node

    def parse_value(self):
        return ValueParser(self).parse()

    @indexed
    def parse_literal(self):
        node_map = {
            'boolean': nodes.BooleanNode,
            'string': nodes.StringNode,
            'float': nodes.FloatNode,
            'int': nodes.IntNode
        }
        token = self.stream.current()
        if token.id not in node_map:
            return
        node = self._create_node(node_map[token.id])
        node.token = self.stream.read(token.id)
        return node

    @indexed
    def parse_property(self):
        if not self.stream.is_current('name'):
            return
        node = self._create_node(nodes.PropertyNode)
        node.name = self.stream.read('name')
        return node

    @indexed
    def parse_prefixed_property(self):
        node_map = {
            '#': nodes.UIDNode,
            '!': nodes.FlagNode,
            '@': nodes.AttributeNode,
            '%': nodes.FormatNode,
            '~': nodes.AliasNode,
            '?': nodes.DocNode
        }
        prefix = self.stream.current()
        if prefix.id not in node_map:
            return
        node = self._create_node(node_map[prefix.id])
        self.stream.read(prefix.id)
        node.name = self.stream.read('name')
        return node

    def parse_scope(self):
        return ScopeParser(self).parse()

    @indexed
    def parse_query(self):
        if not self.stream.is_current('{'):
            return
        node = self._create_node(nodes.QueryNode)
        self.stream.read('{')
        node.key = self.parse_value()
        while not self.stream.is_current('}') and not self.stream.is_eof():
            reference = self.parse_value()
            if reference:
                node.add(reference)
        self.stream.read('}')
        return node

    @indexed
    def parse_list(self):
        if not self.stream.is_current('['):
            return
        node = self._create_node(nodes.ListNode)
        self.stream.read('[')
        while not self.stream.is_current(']') and not self.stream.is_eof():
            reference = self.parse_value()
            if reference:
                node.add(reference)
        self.stream.read(']')
        return node
