from .base import BaseParser
from ..nodes import ScopeNode, QueryNode


class ScopeParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser
        self.node_class = ScopeNode
        self.delimiter_tokens = ("(", ")")

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
        self.delimiter_tokens = ("{", "}")
