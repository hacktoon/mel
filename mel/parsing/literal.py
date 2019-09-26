from .. import nodes
from .. import tokens

from .constants import (
    INT,
    FLOAT,
    BOOLEAN,
    STRING,
    TEMPLATE_STRING,
    LITERAL,
    RANGE,
    VALUE,
    LIST
)

from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)

from ..exceptions import InfiniteRangeError


@subparser
class IntParser(TokenParser):
    id = INT
    Node = nodes.IntNode
    Token = tokens.IntToken


@subparser
class FloatParser(TokenParser):
    id = FLOAT
    Node = nodes.FloatNode
    Token = tokens.FloatToken


@subparser
class BooleanParser(TokenParser):
    id = BOOLEAN
    Node = nodes.BooleanNode
    Token = tokens.BooleanToken


@subparser
class StringParser(TokenParser):
    id = STRING
    Node = nodes.StringNode
    Token = tokens.StringToken


@subparser
class TemplateStringParser(TokenParser):
    id = TEMPLATE_STRING
    Node = nodes.TemplateStringNode
    Token = tokens.TemplateStringToken


@subparser
class LiteralParser(BaseParser):
    id = LITERAL

    def parse(self):
        return self.read_any(
            INT,
            FLOAT,
            BOOLEAN,
            STRING,
            TEMPLATE_STRING
        )


@subparser
class RangeParser(BaseParser):
    id = RANGE
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


@subparser
class ListParser(BaseParser):
    id = LIST
    Node = nodes.ListNode
    PrefixToken = tokens.StartListToken
    SuffixToken = tokens.EndListToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.PrefixToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_values(node)
        self.stream.read(self.SuffixToken)
        return node

    def parse_values(self, node):
        while True:
            _object = self.read(VALUE)
            if not _object:
                break
            node.add(_object)
