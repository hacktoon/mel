from .. import nodes

from .base import BaseParser


class ScopeParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        if not self.stream.is_current('('):
            return
        node = self._create_node(nodes.ScopeNode)
        self.stream.read('(')
        node.key = self.parser.parse_value()
        self.parse_nodes(node)
        self.stream.read(')')
        return node

    def parse_nodes(self, node):
        while not self.stream.is_current(')') and not self.stream.is_eof():
            reference = self.parser.parse_value()
            if reference:
                node.add(reference)
