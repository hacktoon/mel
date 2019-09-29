from .. import nodes

from .constants import ROOT, TAG, RELATION, VALUE
from .base import (
    BaseParser,
    indexed,
    subparser
)


@subparser
class RootParser(BaseParser):
    id = ROOT
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        expressions = self.parse_zero_many_alternative(TAG, RELATION, VALUE)
        node.add(*expressions)
        return node
