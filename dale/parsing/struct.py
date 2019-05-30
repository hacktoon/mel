from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    subparser,
    indexed
)

from ..exceptions import KeyNotFoundError


class StructParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_key(node)
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node

    def parse_key(self, node):
        is_null = self.stream.is_next(tokens.NullKeyToken)
        is_default_fmt = self.stream.is_next(tokens.DefaultFormatKeyToken)
        if is_null or is_default_fmt:
            self.stream.read()
            return
        key, *path = self.parse_path()
        node.key = key
        node.target = self.build_tree(node, path)

    def parse_path(self):
        path = self.subparse(nodes.PathNode)
        if path:
            return path
        raise KeyNotFoundError(self.stream.peek())

    def build_tree(self, node, path):
        for keyword in path:
            scope = self.build_node()
            scope.key = keyword
            node.add(scope)
            node = scope
        return node

    def parse_expressions(self, node):
        while True:
            expression = self.subparse(nodes.ExpressionNode)
            if not expression:
                break
            node.add(expression)


@subparser
class ScopeParser(StructParser):
    Node = nodes.ScopeNode
    FirstToken = tokens.StartScopeToken
    LastToken = tokens.EndScopeToken


@subparser
class PrototypeParser(StructParser):
    Node = nodes.PrototypeNode
    FirstToken = tokens.StartPrototypeToken
    LastToken = tokens.EndPrototypeToken


@subparser
class QueryParser(StructParser):
    Node = nodes.QueryNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken
