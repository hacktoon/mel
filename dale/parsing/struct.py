from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)

from ..exceptions import (KeyNotFoundError, ExpectedValueError)


class StructParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        self.stream.read()
        node = self.build_node()
        node.key = self.parse_key()
        node.expressions = self.parse_expressions()
        self.stream.read(self.LastToken)
        return node

    def parse_key(self):
        return nodes.NullNode()

    def parse_expressions(self):
        expressions = []
        while True:
            expression = self.subparse(nodes.ExpressionNode)
            if not expression:
                break
            expressions.append(expression)
        return expressions


class PathStructParser(BaseParser):
    def parse_path(self):
        path = self.subparse(nodes.PathNode)
        if path:
            return path
        raise KeyNotFoundError(self.stream.peek())


# DEFAULT STRUCTS ======================================================

class DefaultFormatParser(StructParser):
    Node = nodes.DefaultFormatNode
    FirstToken = tokens.StartDefaultFormatToken
    LastToken = tokens.EndObjectToken


class DefaultDocParser(StructParser):
    Node = nodes.DefaultDocNode
    FirstToken = tokens.StartDefaultDocToken
    LastToken = tokens.EndObjectToken


# ROOT ======================================================

@subparser
class RootParser(StructParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        node.expressions = self.parse_expressions()
        return node


# OBJECT ======================================================

@subparser
class ObjectParser(StructParser, PathStructParser):
    Node = nodes.ObjectNode
    FirstToken = tokens.StartObjectToken
    LastToken = tokens.EndObjectToken

    def parse_key(self):
        path = self.parse_path()
        return path[0]


@subparser
class AnonymObjectParser(StructParser):
    Node = nodes.AnonymObjectNode
    FirstToken = tokens.StartAnonymObjectToken
    LastToken = tokens.EndObjectToken


# PROTOTYPE ======================================================

@subparser
class PrototypeParser(StructParser):
    Node = nodes.PrototypeNode
    FirstToken = tokens.StartPrototypeToken
    LastToken = tokens.EndPrototypeToken


# QUERY ======================================================

@subparser
class QueryParser(StructParser):
    Node = nodes.QueryNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken


# RELATION ======================================================

@subparser
class RelationParser(BaseParser):
    Node = nodes.RelationNode

    @indexed
    def parse(self):
        self.stream.save()
        key = self.subparse(nodes.PathNode)
        if not key:
            return
        sign = self.subparse(nodes.SymbolNode)
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
