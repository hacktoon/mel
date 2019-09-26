from .. import nodes
from .. import tokens

from .constants import PATH, KEYWORD, CHILD_PATH, META_PATH
from .base import (
    BaseParser,
    indexed,
    subparser
)

from ..exceptions import KeywordNotFoundError


class SubPathParser(BaseParser):
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        self.stream.read()
        _keyword = self.read(KEYWORD)
        if not _keyword:
            self.error(KeywordNotFoundError)
        node = self.build_node()
        node.keyword = _keyword
        return node


@subparser
class ChildPathParser(SubPathParser):
    id = CHILD_PATH
    Node = nodes.ChildPathNode
    Token = tokens.SubNodeToken


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
        _keyword = self.read(KEYWORD)
        if not _keyword:
            return
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while True:
            tail = self.read_any(CHILD_PATH, META_PATH)
            if not tail:
                break
            node.add(tail)
