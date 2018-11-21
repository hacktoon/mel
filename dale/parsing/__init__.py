from .. import nodes
from ..exceptions import UnexpectedTokenError

from .base import BaseParser
from .values import ValueParser
from .properties import PropertyParser
from .scopes import ScopeParser, QueryParser
from .lists import ListParser


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
        return ValueParser(self).parse()

    @indexed
    def parse_literal(self):
        node_map = {
            "boolean": nodes.BooleanNode,
            "string": nodes.StringNode,
            "float": nodes.FloatNode,
            "int": nodes.IntNode,
        }
        token = self.stream.current()
        if token.id not in node_map:
            return
        node = self._create_node(node_map[token.id])
        node.value = self.stream.read(token.id).value
        return node

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
