from . import nodes
from .exceptions import UnexpectedTokenError, ExpectedValueError


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


class BaseParser:
    def __init__(self, stream):
        self.stream = stream

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node


class Parser(BaseParser):
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
        return ValueParser(self.stream).parse()

    @indexed
    def parse_literal(self):
        return LiteralParser(self.stream).parse()

    @indexed
    def parse_property(self):
        return PropertyParser(self.stream).parse()

    @indexed
    def parse_scope(self):
        return ScopeParser(self.stream).parse()

    @indexed
    def parse_query(self):
        return QueryParser(self.stream).parse()

    @indexed
    def parse_list(self):
        return ListParser(self.stream).parse()


class ValueParser(Parser):
    def parse(self):
        node = self._parse_value()
        if node:
            self._parse_chain(node)
        return node

    def _parse_value(self):
        methods = [
            self.parse_literal,
            self.parse_property,
            self.parse_scope,
            self.parse_query,
            self.parse_list,
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


class ScopeParser(Parser):
    def __init__(self, *args):
        super().__init__(*args)
        self.node_class = nodes.ScopeNode
        self.delimiters = "()"

    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_current(start_token):
            return
        node = self._create_node(self.node_class)
        self.stream.read(start_token)
        self._parse_key(node)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_key(self, node):
        if self.stream.is_current(":"):
            self.stream.read(":")
        elif self.stream.is_current("*"):
            self.stream.read("*")
            node.key = nodes.AbstractScopeKeyNode()
        else:
            node.key = self.parse_value()

    def _parse_values(self, scope):
        end_token = self.delimiters[1]
        inside_scope = not self.stream.is_current(end_token)
        not_eof = not self.stream.is_eof()
        while inside_scope and not_eof:
            value = self.parse_value()
            if not value:
                break
            scope.add(value)


class QueryParser(ScopeParser):
    def __init__(self, *args):
        super().__init__(*args)
        self.node_class = nodes.QueryNode
        self.delimiters = "{}"


class ListParser(Parser):
    def __init__(self, *args):
        super().__init__(*args)
        self.delimiters = "[]"

    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_current(start_token):
            return
        node = self._create_node(nodes.ListNode)
        self.stream.read(start_token)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, node):
        end_token = self.delimiters[1]
        inside_list = not self.stream.is_current(end_token)
        not_eof = not self.stream.is_eof()
        while inside_list and not_eof:
            value = self.parse_value()
            if not value:
                break
            node.add(value)


class PropertyParser(BaseParser):
    PREFIX_MAP = {
        "#": nodes.UIDNode,
        "!": nodes.FlagNode,
        "@": nodes.AttributeNode,
        "%": nodes.FormatNode,
        "$": nodes.VariableNode,
        "?": nodes.DocNode,
    }

    def parse(self):
        current = self.stream.current()
        node_class = nodes.PropertyNode
        if current.id in self.PREFIX_MAP:
            node_class = self.PREFIX_MAP[current.id]
            self.stream.read(current.id)
        elif not self.stream.is_current("name"):
            return
        return self._parse_property(node_class)

    def _parse_property(self, node_class):
        node = self._create_node(node_class)
        node.name = self.stream.read("name").value
        return node


class LiteralParser(BaseParser):
    TOKEN_MAP = {
        "boolean": nodes.BooleanNode,
        "string": nodes.StringNode,
        "float": nodes.FloatNode,
        "int": nodes.IntNode,
    }

    def parse(self):
        token = self.stream.current()
        if token.id not in self.TOKEN_MAP:
            return
        node = self._create_node(self.TOKEN_MAP[token.id])
        node.value = self.stream.read(token.id).value
        return node
