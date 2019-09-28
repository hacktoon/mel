from .. import nodes
from .. import tokens

from .constants import PATH, KEYWORD, CHILD_PATH, META_PATH
from .base import (
    BaseParser,
    indexed,
    subparser
)

from ..exceptions import ParsingError


class SubPathParser(BaseParser):
    def parse(self):
        self.read_token(self.Token)
        _keyword = self.read_rule(KEYWORD)
        node = self.build_node()
        node.keyword = _keyword
        return node


@subparser
class ChildPathParser(SubPathParser):
    id = CHILD_PATH
    Node = nodes.ChildPathNode
    Token = tokens.ChildPathToken


@subparser
class MetaPathParser(SubPathParser):
    id = META_PATH
    Node = nodes.MetaPathNode
    Token = tokens.MetaNodeToken


@subparser
class PathParser(BaseParser):
    id = PATH
    Node = nodes.PathNode

    @indexed
    def parse(self):
        _keyword = self.read_rule(KEYWORD)
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while True:
            try:
                tail = self.read_one(CHILD_PATH, META_PATH)
                node.add(tail)
            except ParsingError:
                break
