from .. import nodes
from .. import tokens

from .base import (
    TokenParser,
    MultiParser,
    BaseParser,
    subparser,
    indexed
)

from ..exceptions import KeyNotFoundError


# STRUCT ==================================================

class StructParser(BaseParser):
    def parse_expressions(self, node):
        while True:
            expression = self.subparse(nodes.ExpressionNode)
            if not expression:
                break
            node.add(expression)


class KeyStructParser(StructParser):
    Key = None

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
        key = self.subparse(self.Key)
        if not key:
            self.error(KeyNotFoundError)
        node.key = key

    def parse_path(self, node):
        path = self.subparse(nodes.PathNode)
        if not path:
            self.error(KeyNotFoundError)
        node.path = path


# ROOT ======================================================

@subparser
class RootParser(StructParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
        return node


# OBJECT ======================================================

@subparser
class ObjectParser(KeyStructParser):
    Node = nodes.ObjectNode
    Key = nodes.ObjectKeyNode
    FirstToken = tokens.StartObjectToken
    LastToken = tokens.EndObjectToken

    def _build_subtree(self, node):
        key, *keywords = node.path
        node.key = key
        for keyword in keywords:
            subnode = self.build_node()
            subnode.key = keyword
            node.add(subnode)
            node = subnode
        return node

    def parse_expressions(self, node):
        # node = self._build_subtree(node)
        super().parse_expressions(node)


# QUERY ======================================================

@subparser
class QueryParser(KeyStructParser):
    Node = nodes.QueryNode
    Key = nodes.QueryKeyNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken


# STRUCT KEY ====================================================

@subparser
class ObjectKeyParser(MultiParser):
    Node = nodes.ObjectKeyNode
    options = (
        nodes.AnonymKeyNode,
        nodes.DefaultDocKeyNode,
        nodes.DefaultFormatKeyNode,
        nodes.PathNode
    )


@subparser
class QueryKeyParser(MultiParser):
    Node = nodes.QueryKeyNode
    options = (
        nodes.AnonymKeyNode,
        nodes.PathNode
    )


@subparser
class AnonymKeyParser(TokenParser):
    Node = nodes.AnonymKeyNode
    Token = tokens.AnonymKeyToken


@subparser
class DefaultDocKeyParser(TokenParser):
    Node = nodes.DefaultDocKeyNode
    Token = tokens.DefaultDocKeyToken


@subparser
class DefaultFormatKeyParser(TokenParser):
    Node = nodes.DefaultFormatKeyNode
    Token = tokens.DefaultFormatKeyToken
