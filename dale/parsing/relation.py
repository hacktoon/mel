from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)

from ..exceptions import ObjectNotFoundError


@subparser
class RelationParser(BaseParser):
    Node = nodes.RelationNode

    @indexed
    def parse(self):
        self.stream.save()
        key = self.subparse(nodes.PathNode)
        if not key:
            return
        symbol = self.subparse(nodes.SymbolNode)
        if not symbol:
            self.stream.restore()
            return
        value = self.subparse(nodes.ObjectNode)
        if not value:
            raise ObjectNotFoundError(self.stream.peek())
        node = self.build_node()
        node.key = key
        node.symbol = symbol
        node.value = value
        return node


@subparser
class SymbolParser(MultiParser):
    Node = nodes.SymbolNode
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