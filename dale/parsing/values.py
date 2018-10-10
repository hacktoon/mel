from .. import nodes
from ..exceptions import ExpectedValueError

from .base import BaseParser


class ValueParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser

    def parse(self):
        base_value = self._parse_value()
        if not base_value or not self.stream.is_current('/'):
            return base_value
        return self._parse_path(base_value)

    def _parse_value(self):
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

    def _parse_path(self, base_value):
        path = self._create_node(nodes.PathNode)
        path.add(base_value)
        while self.stream.is_current('/'):
            self.stream.read('/')
            value = self._parse_value()
            if not value:
                raise ExpectedValueError()
            path.add(value)
        return path
