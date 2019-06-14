from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    subparser,
    indexed
)

from ..exceptions import ExpectedValueError


@subparser
class RelationParser(MultiParser):
    Node = nodes.RelationNode
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


class PathRelationParser(BaseParser):
    @indexed
    def parse(self):
        node = self.build_node()
        self.stream.save()
        path = self.subparse(nodes.PathNode)
        if not path:
            return
        if not self.stream.is_next(self.Token):
            self.stream.restore()
            return
        self.stream.read()
        node.path = path
        node.value = self.parse_value()
        return node

    def parse_value(self):
        value = self.subparse(nodes.ValueNode)
        if not value:
            self.error(ExpectedValueError)
        return value


@subparser
class EqualParser(PathRelationParser):
    Node = nodes.EqualNode
    Token = tokens.EqualToken


@subparser
class DifferentParser(PathRelationParser):
    Node = nodes.DifferentNode
    Token = tokens.DifferentToken


@subparser
class GreaterThanParser(PathRelationParser):
    Node = nodes.GreaterThanNode
    Token = tokens.GreaterThanToken


@subparser
class GreaterThanEqualParser(PathRelationParser):
    Node = nodes.GreaterThanEqualNode
    Token = tokens.GreaterThanEqualToken


@subparser
class LessThanParser(PathRelationParser):
    Node = nodes.LessThanNode
    Token = tokens.LessThanToken


@subparser
class LessThanEqualParser(PathRelationParser):
    Node = nodes.LessThanEqualNode
    Token = tokens.LessThanEqualToken


@subparser
class InParser(PathRelationParser):
    Node = nodes.InNode
    Token = tokens.InToken


@subparser
class NotInParser(PathRelationParser):
    Node = nodes.NotInNode
    Token = tokens.NotInToken
