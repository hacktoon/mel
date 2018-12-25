from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    ValueChainError,
    NameNotFoundError
)


def indexed(method):
    def surrogate(self):
        first = self.stream.peek()
        node = method(self)
        if not node:
            return
        last = self.stream.peek(-1)
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
                index = self.stream.peek().index[0]
                raise UnexpectedTokenError(index)
        return node

    @indexed
    def parse_value(self):
        return ValueParser(self.stream).parse()

    @indexed
    def parse_number(self):
        return NumberParser(self.stream).parse()

    @indexed
    def parse_string(self):
        token = self.stream.peek()
        if token.id != "string":
            return
        self.stream.read()
        node = self._create_node(nodes.StringNode)
        node.value = token.value
        return node

    @indexed
    def parse_boolean(self):
        token = self.stream.peek()
        if token.id != "boolean":
            return
        self.stream.read()
        node = self._create_node(nodes.BooleanNode)
        node.value = token.value
        return node

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

    @indexed
    def parse_wildcard(self):
        if self.stream.is_next("*"):
            self.stream.read("*")
            return self._create_node(nodes.WildcardNode)


class ValueParser(Parser):
    def parse(self):
        node = self._parse_value()
        if node:
            self._parse_chain(node)
        return node

    def _parse_value(self):
        methods = [
            self.parse_number,
            self.parse_boolean,
            self.parse_string,
            self.parse_property,
            self.parse_scope,
            self.parse_query,
            self.parse_list,
            self.parse_wildcard,
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    def _parse_chain(self, node):
        while self.stream.is_next("/"):
            sep = self.stream.read("/")
            value = self._parse_value()
            if not value:
                raise ValueChainError(sep.index[0])
            node.chain(value)


class ScopeParser(Parser):
    def __init__(self, *args):
        super().__init__(*args)
        self.node_class = nodes.ScopeNode
        self.delimiters = "()"

    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_next(start_token):
            return
        node = self._create_node(self.node_class)
        self.stream.read(start_token)
        self._parse_key(node)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read(":")
        else:
            node.key = self.parse_value()

    def _parse_values(self, scope):
        end_token = self.delimiters[1]
        inside_scope = not self.stream.is_next(end_token)
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
        if not self.stream.is_next(start_token):
            return
        node = self._create_node(nodes.ListNode)
        self.stream.read(start_token)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, node):
        end_token = self.delimiters[1]
        inside_list = not self.stream.is_next(end_token)
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
        current = self.stream.peek()
        node_class = nodes.PropertyNode
        if current.id in self.PREFIX_MAP:
            node_class = self.PREFIX_MAP[current.id]
            self.stream.read(current.id)
        elif not self.stream.is_next("name"):
            return
        return self._parse_property(node_class)

    def _parse_property(self, node_class):
        if not self.stream.is_next("name"):
            raise NameNotFoundError(self.stream.peek().index[0])
        node = self._create_node(node_class)
        node.name = self.stream.read("name").value
        return node


class NumberParser(BaseParser):
    def parse(self):
        if self.stream.is_next("float"):
            node_class = nodes.FloatNode
        elif self.stream.is_next("int"):
            node_class = nodes.IntNode
            if self.stream.peek(1).id == "..":
                return RangeParser(self.stream).parse()
        elif self.stream.is_next(".."):
            return RangeParser(self.stream).parse()
        else:
            return
        node = self._create_node(node_class)
        node.value = self.stream.read().value
        return node


class RangeParser(BaseParser):
    def parse(self):
        node = self._create_node(nodes.RangeNode)
        if self.stream.is_next("int"):
            node.start = self.stream.read().value
        self.stream.read('..')
        if not node.start or self.stream.is_next("int"):
            node.end = self.stream.read("int").value
        return node
