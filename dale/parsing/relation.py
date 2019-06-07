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
        key = self.subparse(nodes.PathNode)
        if not key:
            return
        sign = self.subparse(nodes.SignNode)
        if not sign:
            self.stream.restore()
            return
        value = self.subparse(nodes.ValueNode)
        if not value:
            raise ExpectedValueError(self.stream.peek())
        node = self.build_node()
        node.key = key
        node.sign = sign
        node.value = value
        return node


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
