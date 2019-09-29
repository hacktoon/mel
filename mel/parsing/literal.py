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
    LIST,
    WILDCARD
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
        return self.parse_alternative(
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
        _range = self.parse_token(tokens.RangeToken)
        if not _range:
            return
        int_token = self.parse_token(tokens.IntToken)
        if not int_token:
            self.error(InfiniteRangeError, _range)
        node.end = int_token.value
        return True

    def _parse_left_bound(self, node):
        first_is_int = self.stream.is_next(tokens.IntToken)
        range_is_next = self.stream.peek(1) == tokens.RangeToken
        if not (first_is_int and range_is_next):
            return
        node.start = self.parse_token().value
        self.parse_token()
        token = self.parse_token(tokens.IntToken)
        if token:
            node.end = token.value
        return True


@subparser
class ListParser(BaseParser):
    id = LIST
    Node = nodes.ListNode
    PrefixToken = tokens.StartListToken
    SuffixToken = tokens.EndListToken

    @indexed
    def parse(self):
        self.parse_token(self.PrefixToken)
        node = self.build_node()
        node.add(*self.parse_zero_many(VALUE))
        self.parse_token(self.SuffixToken)
        return node


# WILDCARD ===============================================

@subparser
class WildcardParser(TokenParser):
    id = WILDCARD
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken
