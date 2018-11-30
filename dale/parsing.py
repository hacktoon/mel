from . import nodes
from .exceptions import UnexpectedTokenError, ExpectedValueError

from .nodes import ScopeNode, QueryNode, ListNode


PROPERTY_PREFIX_MAP = {
    "#": nodes.UIDNode,
    "!": nodes.FlagNode,
    "@": nodes.AttributeNode,
    "%": nodes.FormatNode,
    "$": nodes.VariableNode,
    "?": nodes.DocNode,
}

NODE_MAP = {
    "boolean": nodes.BooleanNode,
    "string": nodes.StringNode,
    "float": nodes.FloatNode,
    "int": nodes.IntNode,
}


def indexed(method):
    def surrogate(self):
        first = self.stream.current()
        node = method(self)
        if not node:
            return
        last = self.stream.current(-1)
        node.index = first.index[0], last.index[1]
        return node

    return surrogate


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node

    @indexed
    def parse(self):
        node = self._create_node(nodes.RootNode)
        while not self.stream.is_eof():
            value = self.parse_value()
            if value:
                node.add(value)
            elif not self.stream.is_eof():
                raise UnexpectedTokenError(self.stream.current())
        return node

    @indexed
    def parse_value(self):
        return ValueParser(self).parse()

    @indexed
    def parse_literal(self):
        return LiteralParser(self).parse()

    @indexed
    def parse_property(self):
        return PropertyParser(self).parse()

    @indexed
    def parse_scope(self):
        return ScopeParser(self).parse()

    @indexed
    def parse_query(self):
        return QueryParser(self).parse()

    @indexed
    def parse_list(self):
        return ListParser(self).parse()


class ScopeParser(Parser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser
        self.node_class = ScopeNode
        self.delimiter_tokens = "()"

    def parse(self):
        start_token, end_token = self.delimiter_tokens
        if not self.stream.is_current(start_token):
            return
        node = self._create_node(self.node_class)
        self.stream.read(start_token)
        self._parse_key(node)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_key(self, node):
        node.key = self.parser.parse_value()

    def _parse_values(self, scope):
        end_token = self.delimiter_tokens[1]
        inside_scope = not self.stream.is_current(end_token)
        not_eof = not self.stream.is_eof()
        while inside_scope and not_eof:
            value = self.parser.parse_value()
            if not value:
                break
            scope.add(value)


class QueryParser(ScopeParser):
    def __init__(self, parser):
        super().__init__(parser)
        self.node_class = QueryNode
        self.delimiter_tokens = "{}"


class ListParser(Parser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser
        self.delimiter_tokens = "[]"

    def parse(self):
        start_token, end_token = self.delimiter_tokens
        if not self.stream.is_current(start_token):
            return
        node = self._create_node(ListNode)
        self.stream.read(start_token)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, node):
        end_token = self.delimiter_tokens[1]
        inside_list = not self.stream.is_current(end_token)
        not_eof = not self.stream.is_eof()
        while inside_list and not_eof:
            value = self.parser.parse_value()
            if not value:
                break
            node.add(value)


class ValueParser(Parser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        node = self._parse_value()
        if node:
            self._parse_chain(node)
        return node

    def _parse_value(self):
        methods = [
            self.parser.parse_literal,
            self.parser.parse_property,
            self.parser.parse_scope,
            self.parser.parse_query,
            self.parser.parse_list,
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    def _parse_chain(self, node):
        while self.stream.is_current("/"):
            self.stream.read("/")
            value = self._parse_value()
            if not value:
                raise ExpectedValueError()
            node.chain(value)


class PropertyParser(Parser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        current = self.stream.current()
        node_class = PROPERTY_PREFIX_MAP.get(current.id, nodes.PropertyNode)
        if self._is_prefix(current):
            self.stream.read(current.id)
        elif not self.stream.is_current("name"):
            return
        return self._build_node(node_class)

    def _is_prefix(self, prefix):
        return prefix.id in PROPERTY_PREFIX_MAP

    def _build_node(self, node_class):
        node = self._create_node(node_class)
        node.name = self.stream.read("name").value
        return node


class LiteralParser(Parser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        token = self.stream.current()
        if token.id not in NODE_MAP:
            return
        node = self._create_node(NODE_MAP[token.id])
        node.value = self.stream.read(token.id).value
        return node


