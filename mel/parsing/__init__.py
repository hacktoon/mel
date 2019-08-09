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
    subparser,
    indexed
)
from ..exceptions import (
    UnexpectedTokenError,
    KeywordNotFoundError
)


class Parser(BaseParser):
    def parse(self):
        node = self.subparse(nodes.RootNode)
        if self.stream.is_eof():
            return node
        self.error(UnexpectedTokenError)


# EXPRESSION ======================================================

@subparser
class ExpressionParser(MultiParser):
    Node = nodes.ExpressionNode
    options = (
        nodes.TagKeywordNode,
        nodes.RelationNode,
        nodes.ValueNode
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
        self.parse_values(node)
        self.stream.read(self.LastToken)
        return node

    def parse_values(self, node):
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
                self.error(KeywordNotFoundError)
