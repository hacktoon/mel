from .base import BaseParser
from .. import nodes


NODE_MAP = {
    "boolean": nodes.BooleanNode,
    "string": nodes.StringNode,
    "float": nodes.FloatNode,
    "int": nodes.IntNode,
}


class LiteralParser(BaseParser):
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
