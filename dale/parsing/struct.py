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


class BaseStructParser(BaseParser):
    def parse_expressions(self):
        expressions = []
        while True:
            expression = self.subparse(nodes.ExpressionNode)
            if not expression:
                break
            expressions.append(expression)
        return expressions


class BaseFormatStructParser(BaseParser):
    Node = nodes.ScopeNode

    def parse(self):
        if not self.stream.is_next(tokens.DefaultFormatKeyToken):
            return
        self.stream.read()
        node = self.build_node()
        node.expressions = self.parse_expressions()
        return node


@subparser
class PathStructParser(BaseStructParser):
    Node = nodes.PathStructNode

    @indexed
    def parse(self):
        node = self.build_node()
        node.path = self.parse_path()
        node.expressions = self.parse_expressions()
        return node

    def parse_path(self):
        if self.stream.is_next(tokens.NullPathToken):
            self.stream.read()
            return
        path = self.subparse(nodes.PathNode)
        if path:
            return path
        raise KeyNotFoundError(self.stream.peek())


class SubTreeStructParser(PathStructParser):
    @indexed
    def parse(self):
        node = self.build_node()
        node.path = self.parse_path()
        node.expressions = self.parse_expressions()
        return node


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
        path = self.parse_path()
        node.key = path[0]
        node.target = self.build_tree(node, path)

    def parse_path(self):
        path = self.subparse(nodes.PathNode)
        if path:
            return path
        raise KeyNotFoundError(self.stream.peek())

    def build_tree(self, node, path):
        for keyword in path[1:]:
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


# ROOT ======================================================

@subparser
class RootParser(BaseStructParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        # TODO: move 'children' to 'expressions'
        node.children = self.parse_expressions()
        return node


# SCOPE ======================================================

@subparser
class ScopeParser(StructParser):
    Node = nodes.ScopeNode
    FirstToken = tokens.StartScopeToken
    LastToken = tokens.EndScopeToken

    def parse_key(self, node):
        if self.is_null_key():
            self.stream.read()
            return
        path = self.parse_path()
        node.key = path[0]
        node.target = self.build_tree(node, path)

    def is_null_key(self):
        is_null = self.stream.is_next(tokens.NullPathToken)
        is_default_fmt = self.stream.is_next(tokens.DefaultFormatKeyToken)
        return is_null or is_default_fmt

    def build_tree(self, parent, path):
        for keyword in path[1:]:
            child = self.build_indexed_node(keyword, path)
            parent.add(child)
            parent = child
        return parent

    def build_indexed_node(self, keyword, path):
        node = self.build_node()
        node.key = keyword
        node.text = path.text
        node.index = (keyword.index[0], path.index[1])
        return node

    def parse_expressions(self, node):
        while True:
            expression = self.subparse(nodes.ExpressionNode)
            if not expression:
                break
            node.target.add(expression)


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
