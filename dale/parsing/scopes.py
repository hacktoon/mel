from .base import BaseParser
from ..nodes import ScopeNode, QueryNode


class ScopeParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser
        self.node_class = ScopeNode
        self.delimiter_symbols = ("(", ")")

    def parse(self):
        start_symbol, end_symbol = self.delimiter_symbols
        if not self.stream.is_current(start_symbol):
            return
        node = self._create_node(self.node_class)
        self.stream.read(start_symbol)
        self._parse_key(node)
        self._parse_values(node)
        self.stream.read(end_symbol)
        return node

    def _parse_key(self, node):
        node.key = self.parser.parse_value()

    def _parse_values(self, scope):
        end_symbol = self.delimiter_symbols[1]
        inside_scope = not self.stream.is_current(end_symbol)
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
        self.delimiter_symbols = ("{", "}")
