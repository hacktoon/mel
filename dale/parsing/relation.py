from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)

from ..exceptions import ExpectedValueError


@subparser
class RelationParser(BaseParser):
    Node = nodes.RelationNode

    @indexed
    def parse(self):
        self.stream.save()
        node = self.build_node()
        node.key = self.subparse(nodes.PathNode)
        if not node.key:
            return
        node.sign = self.subparse(nodes.SignNode)
        if not node.sign:
            self.stream.restore()
            return
        node.value = self.parse_value()
        return node

    def parse_value(self):
        value = self.subparse(nodes.ValueNode)
        if not value:
            self.error(ExpectedValueError)
        return value


@subparser
class SignParser(MultiParser):
    Node = nodes.SignNode
    options = (
        nodes.EqualNode,
        nodes.DifferentNode,
        nodes.GreaterThanNode,
        nodes.GreaterThanEqualNode,
        nodes.LessThanNode,
        nodes.LessThanEqualNode,
        nodes.InNode,
        nodes.NotInNode
    )


@subparser
class EqualParser(TokenParser):
    Node = nodes.EqualNode
    Token = tokens.EqualToken


@subparser
class DifferentParser(TokenParser):
    Node = nodes.DifferentNode
    Token = tokens.DifferentToken


@subparser
class GreaterThanParser(TokenParser):
    Node = nodes.GreaterThanNode
    Token = tokens.GreaterThanToken


@subparser
class GreaterThanEqualParser(TokenParser):
    Node = nodes.GreaterThanEqualNode
    Token = tokens.GreaterThanEqualToken


@subparser
class LessThanParser(TokenParser):
    Node = nodes.LessThanNode
    Token = tokens.LessThanToken


@subparser
class LessThanEqualParser(TokenParser):
    Node = nodes.LessThanEqualNode
    Token = tokens.LessThanEqualToken


@subparser
class InParser(TokenParser):
    Node = nodes.InNode
    Token = tokens.InToken


@subparser
class NotInParser(TokenParser):
    Node = nodes.NotInNode
    Token = tokens.NotInToken
