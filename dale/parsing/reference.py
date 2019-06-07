from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    subparser,
    indexed
)

from ..exceptions import ExpectedKeywordError


@subparser
class ReferenceParser(BaseParser):
    Node = nodes.ReferenceNode

    @indexed
    def parse(self):
        head = self.subparse(nodes.HeadReferenceNode)
        if not head:
            return
        node = self.build_node()
        node.add(head)
        self.parse_body(node)
        return node

    def parse_body(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            self.parse_child(node)

    def parse_child(self, node):
        child = self.subparse(nodes.ChildReferenceNode)
        if not child:
            self.error(ExpectedKeywordError)
        node.add(child)
        return child


@subparser
class HeadReferenceParser(MultiParser):
    Node = nodes.HeadReferenceNode
    options = (
        nodes.QueryNode,
        nodes.AnonymQueryNode,
        nodes.KeywordNode
    )


@subparser
class ChildReferenceParser(MultiParser):
    Node = nodes.ChildReferenceNode
    options = (
        nodes.WildcardNode,
        nodes.TagNode,
        nodes.RangeNode,
        nodes.IntNode,
        nodes.ListNode,
        nodes.ObjectNode,
        nodes.AnonymObjectNode,
        nodes.QueryNode,
        nodes.AnonymQueryNode,
        nodes.KeywordNode
    )
