from collections import defaultdict
import functools

from . import tokens
from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    SubNodeError,
    RelationError,
    NameNotFoundError,
    InfiniteRangeError
)


def indexed(method):
    @functools.wraps(method)
    def surrogate(parser):
        first = parser.stream.peek()
        node = method(parser)
        if not node:
            return
        last = parser.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        node.text = parser.stream.text
        return node
    return surrogate


class BaseParser:
    _subparsers = {}

    def __init__(self, stream):
        self.stream = stream

    def get_subparser(self, id):
        return self._subparsers.get(id)


class Parser(BaseParser):
    def __init__(self, stream):
        super(). __init__(stream)
        self._init_subparsers()

    def _init_subparsers(self):
        self._build_subparsers(BaseParser)

    def _build_subparsers(self, superclass):
        for _class in superclass.__subclasses__():
            if hasattr(_class, 'Node'):
                BaseParser._subparsers[_class.Node.id] = _class(self.stream)
            self._build_subparsers(_class)

    def parse(self):
        parser = self.get_subparser(nodes.RootNode.id)
        node = parser.parse()
        if not self.stream.is_eof():
            token = self.stream.peek()
            raise UnexpectedTokenError(token)
        return node


class MultiParser(BaseParser):
    @indexed
    def parse(self):
        for option in self.options:
            subparser = self.get_subparser(option.id)
            node = subparser.parse()
            if node:
                return node
        return


class RootParser(BaseParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        pass


class IdentifierParser(MultiParser):
    Node = nodes.IdentifierNode
    options = (
        nodes.NameNode,
        nodes.ReservedNameNode,
        nodes.UIDNode,
        nodes.VariableNode,
        nodes.FormatNode,
        nodes.DocNode
    )


class NameParser(BaseParser):
    Node = nodes.NameNode
    Token = tokens.NameToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        node = self.Node()
        node.name = self.stream.read().value
        return node


class ReservedNameParser(NameParser):
    Node = nodes.ReservedNameNode
    Token = tokens.ReservedNameToken


class PrefixedNameParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        prefix = self.stream.read()
        node = self.Node()
        if self.stream.is_next(tokens.NameToken):
            node.name = self.stream.read().value
            return node
        raise NameNotFoundError(prefix)


class UIDParser(PrefixedNameParser):
    Node = nodes.UIDNode
    Token = tokens.UIDPrefixToken


class VariableParser(PrefixedNameParser):
    Node = nodes.VariableNode
    Token = tokens.VariablePrefixToken


class FormatParser(PrefixedNameParser):
    Node = nodes.FormatNode
    Token = tokens.FormatPrefixToken


class DocParser(PrefixedNameParser):
    Node = nodes.DocNode
    Token = tokens.DocPrefixToken
