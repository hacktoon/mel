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
    priority = 0
    hints = []

    def __init__(self, stream):
        self.stream = stream

    @functools.lru_cache()
    def get_subparsers(self, parser, hint):
        classes = parser.subparsers[hint]
        sorted_cls = sorted(classes, key=lambda p: p.priority, reverse=True)
        return [cls(self.stream) for cls in sorted_cls]

    @indexed
    def parse(self):
        node = nodes.RootNode()
        self.parse_expressions(node)
        if not self.stream.is_eof():
            token = self.stream.peek()
            raise UnexpectedTokenError(token.index[0])
        return node

    @indexed
    def parse_expression(self):
        obj = self.parse_object()
        if not obj:
            return
        relation = self.parse_relation()
        if relation:
            relation.key = obj
            return relation
        return obj

    @indexed
    def parse_object(self):
        node = None
        token = self.stream.peek()
        subparsers = self.get_subparsers(ObjectParser, token.id)
        for parser in subparsers:
            node = parser.parse()
            if node:
                self._parse_subnode(node)
                break
        return node

    def _parse_subnode(self, node):
        if not self.stream.is_next("/"):
            return
        token = self.stream.read("/")
        obj = self.parse_object()
        if not obj:
            raise SubNodeError(token.index[0])
        node.add(obj)
        self._parse_subnode(obj)

    @indexed
    def parse_relation(self):
        token = self.stream.peek()
        subparsers = self.get_subparsers(RelationParser, token.id)
        for parser in subparsers:
            node = parser.parse()
            if node:
                return node
        return

    def parse_expressions(self, node):
        while True:
            exp = self.parse_expression()
            if not exp:
                break
            node.add(exp)

    def parse_objects(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)


class RelationParser(Parser):
    subparsers = defaultdict(list)

    @classmethod
    def __init_subclass__(cls):
        for hint in cls.hints:
            RelationParser.subparsers[hint].append(cls)

    def parse(self):
        token = self.stream.peek()
        if not self.stream.is_next(token.id):
            return
        self.stream.read()
        obj = self.parse_object()
        if not obj:
            raise UnexpectedTokenError(token.index[0])
        node = self.node()
        node.value = obj
        return node


class EqualParser(RelationParser):
    node = nodes.EqualNode
    hints = ["="]


class ObjectParser(Parser):
    subparsers = defaultdict(list)

    @classmethod
    def __init_subclass__(cls):
        for hint in cls.hints:
            ObjectParser.subparsers[hint].append(cls)


class StructParser(ObjectParser):
    def parse(self):
        start_id, end_id = self.delimiters
        if not self.stream.is_next(start_id):
            return
        node = self.node()
        self.stream.read(start_id)
        self._parse_key(node)
        self.parse_expressions(node)
        self.stream.read(end_id)
        return node

    def _parse_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read()
        else:
            node.key = self.parse_expression() or nodes.NullNode()


class ScopeParser(StructParser):
    node = nodes.ScopeNode
    delimiters = "()"
    hints = ["("]


class QueryParser(StructParser):
    node = nodes.QueryNode
    delimiters = "{}"
    hints = ["{"]


class ListParser(ObjectParser):
    node = nodes.ListNode
    delimiters = "[]"
    hints = ["["]

    def parse(self):
        start_id, end_id = self.delimiters
        if not self.stream.is_next(start_id):
            return
        node = self.node()
        self.stream.read(start_id)
        self.parse_objects(node)
        self.stream.read(end_id)
        return node


class NameParser(ObjectParser):
    node = nodes.NameNode
    hints = ["name"]

    def parse(self):
        if not self.stream.is_next("name"):
            return
        node = self.node()
        node.name = self.stream.read("name").value
        return node


class PrefixedNameParser(ObjectParser):
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


class RangeParser(ObjectParser):
    node = nodes.RangeNode
    hints = ["int", ".."]
    priority = 1

    def parse(self):
        range = self._parse_range()
        if not range:
            return
        node = self.node()
        node.value = range
        return node

    def _parse_range(self):
        start = end = None
        token = self.stream.peek()
        next_token = self.stream.peek(1)
        if token.id == "..":
            self.stream.read()
            end = self.stream.read("int").value
        elif token.id == "int" and next_token.id == "..":
            start = self.stream.read().value
            self.stream.read("..")
            if self.stream.is_next("int"):
                end = self.stream.read().value
        else:
            return
        return (start, end)


class LiteralParser(ObjectParser):
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


class WildcardParser(ObjectParser):
    node = nodes.WildcardNode
    hints = ["*"]

    def parse(self):
        if self.stream.is_next("*"):
            self.stream.read()
            return self.node()
        return
