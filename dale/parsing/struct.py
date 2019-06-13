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

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
        return node

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


# SCOPE STRUCT  ============================================

class ScopeStructParser(StructParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        self.stream.read()
        node = self.build_node()
        self.parse_key(node)
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node

    def parse_key(self, _):
        return


class PathStructParser(ScopeStructParser):
    def parse_key(self, node):
        path = self.parse_path()
        node.key = path[0]

    def parse_path(self):
        path = self.subparse(nodes.PathNode)
        if path:
            return path
        self.error(KeyNotFoundError)


# DEFAULT EXPRESSION STRUCTS ==================================

@subparser
class DefaultFormatParser(ScopeStructParser):
    Node = nodes.DefaultFormatKeywordNode
    FirstToken = tokens.StartDefaultFormatToken
    LastToken = tokens.EndObjectToken


@subparser
class DefaultDocParser(ScopeStructParser):
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
class AnonymObjectParser(ScopeStructParser):
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
class AnonymQueryParser(ScopeStructParser):
    Node = nodes.AnonymQueryNode
    FirstToken = tokens.StartAnonymQueryToken
    LastToken = tokens.EndQueryToken
