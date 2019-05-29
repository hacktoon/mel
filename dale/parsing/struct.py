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
        node.key = self.parse_path(node)

    def parse_path(self, node):
        path = self.subparse(nodes.PathNode)
        if not path:
            raise KeyNotFoundError(self.stream.peek())
        node.name = path[0].value
        return path

    def parse_expressions(self, node):
        while True:
            expr = self.subparse(nodes.ExpressionNode)
            if not expr:
                break
            node.add(expr)


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
