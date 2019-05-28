
from .. import tokens
from .. import nodes

from . import relation
from . import struct
from . import reference
from . import keyword
from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    get_subparser,
    indexed
)

from ..exceptions import (
    UnexpectedTokenError,
    NameNotFoundError,
    KeywordNotFoundError,
    KeyNotFoundError,
    InfiniteRangeError,
    ExpectedKeywordError,
    UnexpectedKeywordError
)


class Parser(BaseParser):
    def parse(self):
        node = RootParser(self.stream).parse()
        if self.stream.is_eof():
            return node
        token = self.stream.peek()
        raise UnexpectedTokenError(token)



# ROOT ======================================================

class RootParser(BaseParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        while True:
            expr = self.subparse(nodes.ExpressionNode)
            if not expr:
                break
            node.add(expr)
        return node


# EXPRESSION ======================================================

@subparser
class ExpressionParser(MultiParser):
    Node = nodes.ExpressionNode
    options = (
        nodes.TagNode,
        nodes.RelationNode,
        nodes.ObjectNode
    )


# OBJECT ======================================================

@subparser
class ObjectParser(MultiParser):
    Node = nodes.ObjectNode
    options = (
        nodes.ReferenceNode,
        nodes.LiteralNode,
        nodes.ListNode,
        nodes.ScopeNode
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
            _object = self.subparse(nodes.ObjectNode)
            if not _object:
                break
            node.add(_object)


# PATH ======================================================

@subparser
class PathParser(BaseParser):
    Node = nodes.PathNode

    @indexed
    def parse(self):
        keyword = self.subparse(nodes.KeywordNode)
        if not keyword:
            return
        node = self.build_node()
        node.add(keyword)
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            keyword = self.subparse(nodes.KeywordNode)
            if keyword:
                node.add(keyword)
            else:
                raise KeywordNotFoundError(self.stream.peek())
        return node


# LITERAL ===========================

@subparser
class LiteralParser(MultiParser):
    Node = nodes.LiteralNode
    options = (
        nodes.IntNode,
        nodes.FloatNode,
        nodes.StringNode,
        nodes.BooleanNode
    )


@subparser
class IntParser(TokenParser):
    Node = nodes.IntNode
    Token = tokens.IntToken


@subparser
class FloatParser(TokenParser):
    Node = nodes.FloatNode
    Token = tokens.FloatToken


@subparser
class StringParser(TokenParser):
    Node = nodes.StringNode
    Token = tokens.StringToken


@subparser
class BooleanParser(TokenParser):
    Node = nodes.BooleanNode
    Token = tokens.BooleanToken


@subparser
class WildcardParser(TokenParser):
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken


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
