from ..exceptions import ExpectedValueError

from .base import BaseParser


class ValueParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        node = self._parse_value()
        if node:
            self._parse_chain(node)
        return node

    def _parse_value(self):
        methods = [
            self.parser.parse_literal,
            self.parser.parse_property,
            self.parser.parse_scope,
            self.parser.parse_query,
            self.parser.parse_list,
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
