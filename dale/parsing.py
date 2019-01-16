from collections import defaultdict
import functools

from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    SubNodeError,
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


class Parser:
    subparsers = defaultdict(list)
    priority = 0
    hints = []

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def __init_subclass__(cls):
        for hint in cls.hints:
            Parser.subparsers[hint].append(cls)

    @functools.lru_cache()
    def get_parsers(self, hint):
        classes = Parser.subparsers[hint]
        sorted_cls = sorted(classes, key=lambda p: p.priority, reverse=True)
        return [cls(self.stream) for cls in sorted_cls]

    @indexed
    def parse(self):
        node = nodes.RootNode()
        self.parse_objects(node)
        if not self.stream.is_eof():
            index = self.stream.peek().index[0]
            raise UnexpectedTokenError(index)
        return node

    def parse_objects(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)

    def parse_object(self):
        node = None
        hint = self.stream.peek().id
        for parser in self.get_parsers(hint):
            node = parser.parse()
            if not node:
                continue
            self._parse_subnode(node)
            break
        return node

    def _parse_subnode(self, node):
        if not self.stream.is_next("/"):
            return
        separator = self.stream.read()
        obj = self.parse_object()
        if not obj:
            raise SubNodeError(separator.index[0])
        node.add(obj)
        self._parse_subnode(obj)


class StructParser(Parser):
    @indexed
    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_next(start_token):
            return
        node = self.node()
        self.stream.read(start_token)
        self._parse_key(node)
        self.parse_objects(node)
        self.stream.read(end_token)
        return node

    def _parse_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read()
        else:
            node.key = self.parse_object() or nodes.NullNode()


class ScopeParser(StructParser):
    node = nodes.ScopeNode
    delimiters = "()"
    hints = ["("]


class QueryParser(StructParser):
    node = nodes.QueryNode
    delimiters = "{}"
    hints = ["{"]


class ListParser(Parser):
    node = nodes.ListNode
    delimiters = "[]"
    hints = ["["]

    @indexed
    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_next(start_token):
            return
        node = self.node()
        self.stream.read(start_token)
        self.parse_objects(node)
        self.stream.read(end_token)
        return node


class NameParser(Parser):
    node = nodes.NameNode
    hints = ["name"]

    @indexed
    def parse(self):
        if not self.stream.is_next("name"):
            return
        node = self.node()
        node.name = self.stream.read("name").value
        return node


class PrefixedNameParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.hints[0]):
            return
        self.stream.read()
        node = self.node()
        node.name = self.stream.read("name").value
        return node


class AttributeParser(PrefixedNameParser):
    node = nodes.AttributeNode
    hints = ["@"]


class FlagParser(PrefixedNameParser):
    node = nodes.FlagNode
    hints = ["!"]


class UIDParser(PrefixedNameParser):
    node = nodes.UIDNode
    hints = ["#"]


class VariableParser(PrefixedNameParser):
    node = nodes.VariableNode
    hints = ["$"]


class FormatParser(PrefixedNameParser):
    node = nodes.FormatNode
    hints = ["%"]


class DocParser(PrefixedNameParser):
    node = nodes.DocNode
    hints = ["?"]


class RangeParser(Parser):
    node = nodes.RangeNode
    hints = ["int", ".."]
    priority = 1

    @indexed
    def parse(self):
        _range = self._parse_range()
        if not _range:
            return
        node = self.node()
        node.value = _range
        return node

    def _parse_range(self):
        start = end = None
        current = self.stream.peek()
        next = self.stream.peek(1)
        if current.id == "..":
            self.stream.read()
            end = self.stream.read("int").value
        elif current.id == "int" and next.id == "..":
            start = self.stream.read().value
            self.stream.read("..")
            if self.stream.is_next("int"):
                end = self.stream.read().value
        else:
            return
        return (start, end)


class LiteralParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.node.id):
            return
        node = self.node()
        node.value = self.stream.read().value
        return node


class FloatParser(LiteralParser):
    node = nodes.FloatNode
    hints = ["float"]


class IntParser(LiteralParser):
    node = nodes.IntNode
    hints = ["int"]


class StringParser(LiteralParser):
    node = nodes.StringNode
    hints = ["string"]


class BooleanParser(LiteralParser):
    node = nodes.BooleanNode
    hints = ["boolean"]


class WildcardParser(Parser):
    node = nodes.WildcardNode
    hints = ["*"]

    @indexed
    def parse(self):
        if self.stream.is_next("*"):
            self.stream.read()
            return self.node()
        return
