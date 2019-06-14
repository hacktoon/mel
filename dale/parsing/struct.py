from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    subparser,
    indexed
)

from ..exceptions import KeyNotFoundError


# STRUCT ==================================================

class StructParser(BaseParser):
    Expression = nodes.ExpressionNode

    def parse_expressions(self, node):
        while True:
            expression = self.subparse(self.Expression)
            if not expression:
                break
            node.add(expression)


# ROOT ======================================================

@subparser
class RootParser(StructParser):
    Node = nodes.RootNode
    Expression = nodes.ObjectExpressionNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
        return node


# SPECIALIZED STRUCTS  ======================================

class MetaStructParser(StructParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node


class PathStructParser(StructParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_path(node)
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node

    def parse_path(self, node):
        path = self.subparse(nodes.PathNode)
        if not path:
            self.error(KeyNotFoundError)
        node.path = path


# DEFAULT EXPRESSION STRUCTS ==================================

@subparser
class DefaultFormatParser(MetaStructParser):
    Node = nodes.DefaultFormatKeywordNode
    FirstToken = tokens.StartDefaultFormatToken
    LastToken = tokens.EndObjectToken


@subparser
class DefaultDocParser(MetaStructParser):
    Node = nodes.DefaultDocKeywordNode
    FirstToken = tokens.StartDefaultDocToken
    LastToken = tokens.EndObjectToken


# OBJECT ======================================================

@subparser
class ObjectParser(PathStructParser):
    Node = nodes.ObjectNode
    FirstToken = tokens.StartObjectToken
    LastToken = tokens.EndObjectToken
    Expression = nodes.ObjectExpressionNode


@subparser
class AnonymObjectParser(MetaStructParser):
    Node = nodes.AnonymObjectNode
    FirstToken = tokens.StartAnonymObjectToken
    LastToken = tokens.EndObjectToken
    Expression = nodes.ObjectExpressionNode


# QUERY ======================================================

@subparser
class QueryParser(PathStructParser):
    Node = nodes.QueryNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken


@subparser
class AnonymQueryParser(MetaStructParser):
    Node = nodes.AnonymQueryNode
    FirstToken = tokens.StartAnonymQueryToken
    LastToken = tokens.EndQueryToken
