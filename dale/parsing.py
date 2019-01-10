import functools

from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    SubNodeError,
)


def subparser(method):
    def surrogate(self):
        first = self.stream.peek()
        node = method(self)
        if not node:
            return
        last = self.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        node.text = self.stream.text
        return node

    return surrogate


class BaseParser:
    def __init__(self, stream):
        self.stream = stream
        self.subparsers = {}

    def parse_object(self):
        node = None
        for parser_id in [
                "range",
                "float",
                "int",
                "string",
                "boolean",
                "name",
                "flag",
                "attribute",
                "uid",
                "variable",
                "format",
                "doc",
                "wildcard",
                "list",
                "scope",
                "query",
            ]:
            method = getattr(self, "parse_" + parser_id)
            node = method()
            if node:
                break
        if node:
            self._parse_subnode(node)
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

    def parse_objects(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)


class Parser(BaseParser):
    @subparser
    def parse(self):
        node = nodes.RootNode()
        self.parse_objects(node)
        if not self.stream.is_eof():
            index = self.stream.peek().index[0]
            raise UnexpectedTokenError(index)
        return node

    """
    StructParser -----------------------------
    """
    @subparser
    def parse_scope(self):
        return self._parse_struct("()", nodes.ScopeNode)

    @subparser
    def parse_query(self):
        return self._parse_struct("{}", nodes.QueryNode)

    def _parse_struct(self, delimiters, node_class):
        start_token, end_token = delimiters
        if not self.stream.is_next(start_token):
            return
        node = node_class()
        self.stream.read(start_token)
        self._parse_struct_key(node)
        self.parse_objects(node)
        self.stream.read(end_token)
        return node

    def _parse_struct_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read()
        else:
            node.key = self.parse_object()

    """
    ListParser -----------------------------
    """
    @subparser
    def parse_list(self):
        start_token, end_token = "[]"
        if not self.stream.is_next(start_token):
            return
        node = nodes.ListNode()
        self.stream.read(start_token)
        self._parse_list_items(node)
        self.stream.read(end_token)
        return node

    def _parse_list_items(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)

    """
    NameParser -----------------------------
    """
    @subparser
    def parse_name(self):
        if not self.stream.is_next("name"):
            return
        node = nodes.NameNode()
        node.name = self.stream.read("name").value
        return node

    """
    PrefixedNameParser -----------------------------
    """
    @subparser
    def parse_attribute(self):
        return self._parse_prefixed_name("@", nodes.AttributeNode)

    @subparser
    def parse_flag(self):
        return self._parse_prefixed_name("!", nodes.FlagNode)

    @subparser
    def parse_uid(self):
        return self._parse_prefixed_name("#", nodes.UIDNode)

    @subparser
    def parse_variable(self):
        return self._parse_prefixed_name("$", nodes.VariableNode)

    @subparser
    def parse_format(self):
        return self._parse_prefixed_name("%", nodes.FormatNode)

    @subparser
    def parse_doc(self):
        return self._parse_prefixed_name("?", nodes.DocNode)

    def _parse_prefixed_name(self, prefix, node_class):
        if not self.stream.is_next(prefix):
            return
        self.stream.read()
        node = node_class()
        node.name = self.stream.read("name").value
        return node

    """
    RangeParser -----------------------------
    """
    #@priority(2)
    @subparser
    def parse_range(self):
        _range = self._parse_range_values()
        if not _range:
            return
        node = nodes.RangeNode()
        node.value = _range
        return node

    def _parse_range_values(self):
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

    """
    LiteralParser -----------------------------
    """
    @subparser
    def parse_int(self):
        return self._parse_literal(nodes.IntNode)

    @subparser
    def parse_float(self):
        return self._parse_literal(nodes.FloatNode)

    @subparser
    def parse_string(self):
        return self._parse_literal(nodes.StringNode)

    @subparser
    def parse_boolean(self):
        return self._parse_literal(nodes.BooleanNode)

    def _parse_literal(self, node_class):
        if not self.stream.is_next(node_class.id):
            return
        node = node_class()
        node.value = self.stream.read().value
        return node

    """
    WildcardParser -----------------------------
    """
    @subparser
    def parse_wildcard(self):
        if self.stream.is_next("*"):
            self.stream.read()
            return nodes.WildcardNode()
        return
