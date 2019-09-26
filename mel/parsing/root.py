from .. import nodes

from .constants import ROOT, EXPRESSION
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
        expressions = self.read_zero_many(EXPRESSION)
        node.add(*expressions)
        return node
