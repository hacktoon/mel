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
        token = self.read_token(self.Token)
        if not token:
            return
        _keyword = self.read_rule(KEYWORD)
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
        _keyword = self.read_rule(KEYWORD)
        if not _keyword:
            return
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while True:
            tail = self.read_one(CHILD_PATH, META_PATH)
            if not tail:
                break
            node.add(tail)
