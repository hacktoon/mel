from .. import nodes
from .. import tokens

from .constants import (
    REFERENCE,
    TAG,
    RANGE,
    INT,
    LIST,
    OBJECT,
    QUERY,
    KEYWORD,
    WILDCARD
)
from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)

from ..exceptions import ExpectedKeywordError

TAIL_PARSERS = (
    WILDCARD,
    TAG,
    RANGE,
    INT,
    LIST,
    OBJECT,
    QUERY,
    KEYWORD
)


@subparser
class ReferenceParser(BaseParser):
    id = REFERENCE
    Node = nodes.ReferenceNode

    @indexed
    def parse(self):
        head = self.read_any(QUERY, KEYWORD)
        if not head:
            return
        node = self.build_node()
        node.add(head)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.read_token()
            self.parse_child(node)

    def parse_child(self, node):
        child = self.read_any(*TAIL_PARSERS)
        if not child:
            self.error(ExpectedKeywordError)
        node.add(child)
        return child


# WILDCARD ===============================================

@subparser
class WildcardParser(TokenParser):
    id = WILDCARD
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken
