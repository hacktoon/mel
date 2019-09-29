from .. import nodes
from .. import tokens

from .constants import (
    REFERENCE,
    CHILD_REFERENCE,
    TAG,
    RANGE,
    INT,
    LIST,
    OBJECT,
    QUERY,
    KEYWORD,
    WILDCARD,
)
from .base import (
    BaseParser,
    indexed,
    subparser
)


@subparser
class SubReferenceParser(BaseParser):
    id = CHILD_REFERENCE
    Node = nodes.SubReferenceNode

    @indexed
    def parse(self):
        self.parse_token(tokens.ChildPathToken)
        return self.read_alternative([
            WILDCARD,
            TAG,
            RANGE,
            INT,
            LIST,
            OBJECT,
            QUERY,
            KEYWORD
        ])


@subparser
class ReferenceParser(BaseParser):
    id = REFERENCE
    Node = nodes.ReferenceNode

    @indexed
    def parse(self):
        head = self.parse_alternative(QUERY, KEYWORD)
        node = self.build_node()
        node.add(head)
        node.add(*self.parse_zero_many(CHILD_REFERENCE))
        return node
