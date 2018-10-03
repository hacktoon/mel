from .. import nodes

from .base import BaseParser
from .decorators import builder


class ScopeParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    @builder(nodes.ScopeNode)
    def parse(self, node):
        if not self.stream.is_current('('):
            return
        self.stream.read('(')
        node.key = self.parser.parse_reference()
        self.parse_nodes(node)
        self.stream.read(')')
        return node

    def parse_nodes(self, node):
        while not self.stream.is_current(')') and not self.stream.is_eof():
            reference = self.parser.parse_reference()
            if reference:
                node.add(reference)
