from .. import nodes
from ..exceptions import ExpectedValueError

from .base import BaseParser


class ValueParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        base_value = self.parse_base_value()
        if not base_value or not self.stream.is_current('/'):
            return base_value
        return self.parse_remaining_values(base_value)

    def parse_base_value(self):
        methods = [
            self.parser.parse_literal,
            self.parser.parse_prefixed_property,
            self.parser.parse_property,
            self.parser.parse_scope,
            self.parser.parse_query,
            self.parser.parse_list
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    def parse_remaining_values(self, base_value):
        reference = self._create_node(nodes.PathNode)
        reference.add(base_value)
        while self.stream.is_current('/'):
            self.stream.read('/')
            value = self.parse_base_value()
            if not value:
                raise ExpectedValueError()
            reference.add(value)
        return reference
