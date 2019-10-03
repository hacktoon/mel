from .. import nodes

from .constants import (
    PATH,
    RELATION,
    EQUAL,
    DIFFERENT,
    GREATER_THAN,
    GREATER_THAN_EQUAL,
    LESS_THAN,
    LESS_THAN_EQUAL,
    IN,
    NOT_IN,
    VALUE
)

from .base import BaseParser, indexed, subparser


@subparser
class RelationParser(BaseParser):
    id = RELATION

    def parse(self):
        return self.parse_alternative(
            EQUAL,
            DIFFERENT,
            GREATER_THAN,
            GREATER_THAN_EQUAL,
            LESS_THAN,
            LESS_THAN_EQUAL,
            IN,
            NOT_IN,
        )


class SignedValueParser(BaseParser):
    @indexed
    def parse(self):
        node = self.build_node()
        node.path = self.parse_rule(PATH)
        node.sign = self.parse_token(self.sign_token)
        node.value = self.parse_rule(VALUE)
        return node


@subparser
class EqualParser(SignedValueParser):
    id = EQUAL
    Node = nodes.EqualNode
    sign_token = '='


@subparser
class DifferentParser(SignedValueParser):
    id = DIFFERENT
    Node = nodes.DifferentNode
    sign_token = '!='


@subparser
class GreaterThanParser(SignedValueParser):
    id = GREATER_THAN
    Node = nodes.GreaterThanNode
    sign_token = '>'


@subparser
class GreaterThanEqualParser(SignedValueParser):
    id = GREATER_THAN_EQUAL
    Node = nodes.GreaterThanEqualNode
    sign_token = '>='


@subparser
class LessThanParser(SignedValueParser):
    id = LESS_THAN
    Node = nodes.LessThanNode
    sign_token = '<'


@subparser
class LessThanEqualParser(SignedValueParser):
    id = LESS_THAN_EQUAL
    Node = nodes.LessThanEqualNode
    sign_token = '<='


@subparser
class InParser(SignedValueParser):
    id = IN
    Node = nodes.InNode
    sign_token = '><'


@subparser
class NotInParser(SignedValueParser):
    id = NOT_IN
    Node = nodes.NotInNode
    sign_token = '<>'
