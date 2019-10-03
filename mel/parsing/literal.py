from .. import nodes

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
    token = 'int'


@subparser
class FloatParser(TokenParser):
    id = FLOAT
    Node = nodes.FloatNode
    token = 'float'


@subparser
class BooleanParser(TokenParser):
    id = BOOLEAN
    Node = nodes.BooleanNode
    token = 'boolean'


@subparser
class StringParser(TokenParser):
    id = STRING
    Node = nodes.StringNode
    token = 'string'


@subparser
class TemplateStringParser(TokenParser):
    id = TEMPLATE_STRING
    Node = nodes.TemplateStringNode
    token = 'template-string'


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
        self.parse_token('range')
        node = self.build_node()
        node.end = self.parse_token('int')
        return node


@subparser
class LeftBoundRangeParser(BaseParser):
    id = LEFT_BOUND_RANGE
    Node = nodes.RangeNode

    def parse(self):
        node = self.build_node()
        node.start = self.parse_token('int')
        self.parse_token('range')
        node.end = self.parse_token_optional('int')
        return node


@subparser
class ListParser(BaseParser):
    id = LIST
    Node = nodes.ListNode

    @indexed
    def parse(self):
        self.parse_token('[')
        node = self.build_node()
        node.add(*self.parse_zero_many(VALUE))
        self.parse_token(']')
        return node


# WILDCARD ===============================================

@subparser
class WildcardParser(TokenParser):
    id = WILDCARD
    Node = nodes.WildcardNode
    token = '*'
