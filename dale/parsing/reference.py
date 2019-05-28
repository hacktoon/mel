from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    subparser,
    indexed
)

from ..exceptions import (
    UnexpectedKeywordError,
    ExpectedKeywordError
)


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
        self.parse_children(node)

        return node

    def parse_children(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            if self.parse_tag(node):
                break
            self.parse_child(node)

    def parse_tag(self, node):
        tag = self.subparse(nodes.TagNode)
        if tag:
            node.add(tag)
        if self.stream.is_next(tokens.SubNodeToken):
            raise UnexpectedKeywordError(self.stream.peek(1))
        return tag

    def parse_child(self, node):
        child = self.subparse(nodes.ChildReferenceNode)
        if not child:
            raise ExpectedKeywordError(self.stream.peek())
        node.add(child)
        return child


@subparser
class HeadReferenceParser(MultiParser):
    Node = nodes.HeadReferenceNode
    options = (
        nodes.QueryNode,
        nodes.KeywordNode
    )


@subparser
class ChildReferenceParser(MultiParser):
    Node = nodes.ChildReferenceNode
    options = (
        nodes.WildcardNode,
        nodes.RangeNode,
        nodes.IntNode,
        nodes.ListNode,
        nodes.QueryNode,
        nodes.KeywordNode
    )