from .base import BaseParser
from ..nodes import ScopeNode


class ScopeParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        if not self.stream.is_current("("):
            return
        node = self._create_node(ScopeNode)
        self.stream.read("(")
        self._parse_key(node)
        self._parse_values(node)
        self.stream.read(")")
        return node

    def _parse_key(self, node):
        node.key = self.parser.parse_value()

    def _parse_values(self, scope):
        parsing_scope = not self.stream.is_current(")")
        streaming = not self.stream.is_eof()
        while parsing_scope and streaming:
            value = self.parser.parse_value()
            if not value:
                break
            scope.add(value)
