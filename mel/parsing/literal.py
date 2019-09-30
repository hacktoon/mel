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
    LEFT_BOUND_RANGE,
    RIGHT_BOUND_RANGE,
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

    @indexed
    def parse(self):
        return self.parse_alternative(RIGHT_BOUND_RANGE, LEFT_BOUND_RANGE)


@subparser
class RightBoundRangeParser(BaseParser):
    id = RIGHT_BOUND_RANGE
    Node = nodes.RangeNode

    def parse(self):
        self.parse_token(tokens.RangeToken)
        node = self.build_node()
        node.end = self.parse_token(tokens.IntToken)
        return node


@subparser
class LeftBoundRangeParser(BaseParser):
    id = LEFT_BOUND_RANGE
    Node = nodes.RangeNode

    def parse(self):
        node = self.build_node()
        node.start = self.parse_token(tokens.IntToken)
        self.parse_token(tokens.RangeToken)
        node.end = self.parse_token_optional(tokens.IntToken)
        return node


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
