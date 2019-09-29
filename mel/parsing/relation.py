from .. import nodes
from .. import tokens

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
        node.path = self.read_rule(PATH)
        node.sign = self.parse_token(self.SignToken)
        node.value = self.read_rule(VALUE)
        return node


@subparser
class EqualParser(SignedValueParser):
    id = EQUAL
    Node = nodes.EqualNode
    SignToken = tokens.EqualToken


@subparser
class DifferentParser(SignedValueParser):
    id = DIFFERENT
    Node = nodes.DifferentNode
    SignToken = tokens.DifferentToken


@subparser
class GreaterThanParser(SignedValueParser):
    id = GREATER_THAN
    Node = nodes.GreaterThanNode
    SignToken = tokens.GreaterThanToken


@subparser
class GreaterThanEqualParser(SignedValueParser):
    id = GREATER_THAN_EQUAL
    Node = nodes.GreaterThanEqualNode
    SignToken = tokens.GreaterThanEqualToken


@subparser
class LessThanParser(SignedValueParser):
    id = LESS_THAN
    Node = nodes.LessThanNode
    SignToken = tokens.LessThanToken


@subparser
class LessThanEqualParser(SignedValueParser):
    id = LESS_THAN_EQUAL
    Node = nodes.LessThanEqualNode
    SignToken = tokens.LessThanEqualToken


@subparser
class InParser(SignedValueParser):
    id = IN
    Node = nodes.InNode
    SignToken = tokens.InToken


@subparser
class NotInParser(SignedValueParser):
    id = NOT_IN
    Node = nodes.NotInNode
    SignToken = tokens.NotInToken
