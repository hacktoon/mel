from .. import nodes
from ..exceptions import ExpectedValueError, UnexpectedTokenError

from .decorators import builder, mapbuilder
from .scopes import a


class BaseParser:
    def __init__(self, stream):
        self.stream = stream

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node


class Parser(BaseParser):
    @builder(nodes.Node)
    def parse(self, node):
        while not self.stream.is_eof():
            reference = self.parse_reference()
            if reference:
                node.add(reference)
            elif not self.stream.is_eof():
                raise UnexpectedTokenError(self.stream.current())
        if len(node.nodes) == 1:
            return node.nodes[0]
        return node

    @builder(nodes.ReferenceNode)
    def parse_reference(self, node):
        first = last = self.parse_value()
        if not first:
            return
        node.add(first)
        while self.stream.is_current('/'):
            self.stream.read('/')
            last = self.parse_value()
            if not last:
                raise ExpectedValueError()
            node.add(last)
        if len(node.nodes) == 1:
            return node.nodes[0]
        return node

    def parse_value(self):
        methods = [
            self.parse_literal,
            self.parse_prefixed_property,
            self.parse_property,
            self.parse_scope,
            self.parse_query,
            self.parse_list
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    @mapbuilder({
        'boolean': nodes.BooleanNode,
        'string': nodes.StringNode,
        'float': nodes.FloatNode,
        'int': nodes.IntNode
    })
    def parse_literal(self, node):
        token = self.stream.current()
        node.token = self.stream.read(token.id)
        return node

    @builder(nodes.PropertyNode)
    def parse_property(self, node):
        if not self.stream.is_current('name'):
            return
        node.name = self.stream.read('name')
        return node

    @mapbuilder({
        '#': nodes.UIDNode,
        '!': nodes.FlagNode,
        '@': nodes.AttributeNode,
        '%': nodes.FormatNode,
        '~': nodes.AliasNode,
        '?': nodes.DocNode
    })
    def parse_prefixed_property(self, node):
        prefix = self.stream.current()
        self.stream.read(prefix.id)
        node.name = self.stream.read('name')
        return node

    @builder(nodes.ScopeNode)
    def parse_scope(self, node):
        if not self.stream.is_current('('):
            return
        self.stream.read('(')
        node.key = self.parse_reference()
        while not self.stream.is_current(')') and not self.stream.is_eof():
            reference = self.parse_reference()
            if reference:
                node.add(reference)
        self.stream.read(')')
        return node

    @builder(nodes.QueryNode)
    def parse_query(self, node):
        if not self.stream.is_current('{'):
            return
        self.stream.read('{')
        node.key = self.parse_reference()
        while not self.stream.is_current('}') and not self.stream.is_eof():
            reference = self.parse_reference()
            if reference:
                node.add(reference)
        self.stream.read('}')
        return node

    @builder(nodes.ListNode)
    def parse_list(self, node):
        if not self.stream.is_current('['):
            return
        self.stream.read('[')
        while not self.stream.is_current(']') and not self.stream.is_eof():
            reference = self.parse_reference()
            if reference:
                node.add(reference)
        self.stream.read(']')
        return node
