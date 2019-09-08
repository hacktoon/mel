from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    TokenParser,
    indexed
)

from ..exceptions import InfiniteRangeError


class IntParser(TokenParser):
    Node = nodes.IntNode
    Token = tokens.IntToken


class FloatParser(TokenParser):
    Node = nodes.FloatNode
    Token = tokens.FloatToken


class BooleanParser(TokenParser):
    Node = nodes.BooleanNode
    Token = tokens.BooleanToken


class StringParser(TokenParser):
    Node = nodes.StringNode
    Token = tokens.StringToken


class TemplateStringParser(TokenParser):
    Node = nodes.TemplateStringNode
    Token = tokens.TemplateStringToken


class LiteralParser(BaseParser):
    def parse(self):
        return self.read_any([
            IntParser,
            FloatParser,
            StringParser,
            TemplateStringParser,
            BooleanParser
        ])


class RangeParser(BaseParser):
    Node = nodes.RangeNode

    @indexed
    def parse(self):
        node = self.build_node()
        if self._parse_left_open(node):
            return node
        if self._parse_left_bound(node):
            return node
        return

    def _parse_left_open(self, node):
        if not self.stream.is_next(tokens.RangeToken):
            return
        _range = self.stream.read()
        if not self.stream.is_next(tokens.IntToken):
            self.error(InfiniteRangeError, _range)
        node.end = self.stream.read().value
        return True

    def _parse_left_bound(self, node):
        first_is_int = self.stream.is_next(tokens.IntToken)
        range_is_next = self.stream.peek(1) == tokens.RangeToken
        if not (first_is_int and range_is_next):
            return
        node.start = self.stream.read().value
        self.stream.read()
        if self.stream.is_next(tokens.IntToken):
            node.end = self.stream.read().value
        return True
