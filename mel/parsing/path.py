from .. import nodes
from .. import tokens

from .keyword import KeywordParser

from .base import (
    BaseParser,
    indexed
)

from ..exceptions import KeywordNotFoundError


# PATH ======================================================

class SubPathParser(BaseParser):
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        self.stream.read()
        _keyword = self.read(KeywordParser)
        if not _keyword:
            self.error(KeywordNotFoundError)
        node = self.build_node()
        node.keyword = _keyword
        return node


class ChildPathParser(SubPathParser):
    Node = nodes.ChildPathNode
    Token = tokens.SubNodeToken


class MetaPathParser(SubPathParser):
    Node = nodes.MetaPathNode
    Token = tokens.MetaNodeToken


class PathParser(BaseParser):
    Node = nodes.PathNode
    subparsers = [
        ChildPathParser,
        MetaPathParser,
    ]

    @indexed
    def parse(self):
        _keyword = self.read(KeywordParser)
        if not _keyword:
            return
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while True:
            tail = self.read_any(self.subparsers)
            if not tail:
                break
            node.add(tail)
