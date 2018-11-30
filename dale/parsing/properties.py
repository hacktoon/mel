from .base import BaseParser
from .. import nodes


PREFIX_MAP = {
    "#": nodes.UIDNode,
    "!": nodes.FlagNode,
    "@": nodes.AttributeNode,
    "%": nodes.FormatNode,
    "$": nodes.VariableNode,
    "?": nodes.DocNode,
}


class PropertyParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        current = self.stream.current()
        node_class = PREFIX_MAP.get(current.id, nodes.PropertyNode)
        if self._is_prefix(current):
            self.stream.read(current.id)
        elif not self.stream.is_current("name"):
            return
        return self._build_node(node_class)

    def _is_prefix(self, prefix):
        return prefix.id in PREFIX_MAP

    def _build_node(self, node_class):
        node = self._create_node(node_class)
        node.name = self.stream.read("name").value
        return node
