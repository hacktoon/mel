from .. import tokens
from .. import nodes

from . import ( # noqa
    struct,
    reference,
    literal,
    relation,
    keyword
)
from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)
from ..exceptions import (
    UnexpectedTokenError,
    KeywordNotFoundError,
    InfiniteRangeError
)


class Parser(BaseParser):
    def parse(self):
        node = self.subparse(nodes.Node)
        if self.stream.is_eof():
            return node
        token = self.stream.peek()
        raise UnexpectedTokenError(token)


# EXPRESSION ======================================================

@subparser
class ExpressionParser(MultiParser):
    Node = nodes.ExpressionNode
    options = (
        nodes.TagNode,
        nodes.PrototypeNode,
        nodes.RelationNode,
        nodes.ValueNode
    )


@subparser
class ObjectExpressionParser(MultiParser):
    Node = nodes.ObjectExpressionNode
    options = (
        nodes.ExpressionNode,
        nodes.DefaultFormatNode,
        nodes.DefaultDocNode
    )


# VALUE ======================================================

@subparser
class ValueParser(MultiParser):
    Node = nodes.ValueNode
    options = (
        nodes.ReferenceNode,
        nodes.LiteralNode,
        nodes.ListNode,
        nodes.ObjectNode,
        nodes.AnonymObjectNode
    )


# LIST ======================================================

@subparser
class ListParser(BaseParser):
    Node = nodes.ListNode
    FirstToken = tokens.StartListToken
    LastToken = tokens.EndListToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node

    def parse_expressions(self, node):
        while True:
            _object = self.subparse(nodes.ValueNode)
            if not _object:
                break
            node.add(_object)


# PATH ======================================================

@subparser
class PathParser(BaseParser):
    Node = nodes.PathNode

    @indexed
    def parse(self):
        _keyword = self.subparse(nodes.KeywordNode)
        if not _keyword:
            return
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            _keyword = self.subparse(nodes.KeywordNode)
            if _keyword:
                node.add(_keyword)
            else:
                raise KeywordNotFoundError(self.stream.peek())


# RANGE ===========================

@subparser
class RangeParser(BaseParser):
    Node = nodes.RangeNode

    @indexed
    def parse(self):
        node = self.build_node()
        if self._parse_left_open(node):
            return node
        if self._parse_left_bound(node):
            return node
        return

    def _parse_left_open(self, node):
        if not self.stream.is_next(tokens.RangeToken):
            return
        _range = self.stream.read()
        if not self.stream.is_next(tokens.IntToken):
            raise InfiniteRangeError(_range)
        node.end = self.stream.read().value
        return True

    def _parse_left_bound(self, node):
        first_is_int = self.stream.is_next(tokens.IntToken)
        range_is_next = self.stream.peek(1) == tokens.RangeToken
        if not (first_is_int and range_is_next):
            return
        node.start = self.stream.read().value
        self.stream.read()
        if self.stream.is_next(tokens.IntToken):
            node.end = self.stream.read().value
        return True


@subparser
class WildcardParser(TokenParser):
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken
