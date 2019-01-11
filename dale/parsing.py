from collections import defaultdict

from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    SubNodeError,
)


def _MetaParser_builder(hints=None, priority=0, root=False):
    def decorator(method):
        def surrogate(parser):
            first = parser.stream.peek()
            node = method(parser)
            if not node:
                return
            last = parser.stream.peek(-1)
            node.index = first.index[0], last.index[1]
            node.text = parser.stream.text
            return node
        surrogate._subparser = True
        surrogate.__name__ = method.__name__
        surrogate._priority = priority
        surrogate._root = root
        surrogate._hints = hints if isinstance(hints, list) else [hints]
        return surrogate
    return decorator


class _MetaParser:
    def __init__(self, parser):
        self.parser = parser
        self._hints = defaultdict(list)

        self.__init__hints()

    def __init__hints(self):
        def sort_parsers(parsers):
            return sorted(parsers, key=lambda p: p._priority, reverse=True)

        for method in self.parser.__class__.__dict__.values():
            if not hasattr(method, "_subparser") or method._root:
                continue
            for token_id in method._hints:
                self._hints[token_id].append(method)

    def subparsers(self):
        token_id = self.parser.stream.peek().id
        return self._hints[token_id]


class Parser:
    def __init__(self, stream):
        self.stream = stream
        self.meta = _MetaParser(self)

    @_MetaParser_builder(root=True)
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

    """
    StructParser -----------------------------
    """
    @_MetaParser_builder(hints="(")
    def parse_scope(self):
        return self._parse_struct("()", nodes.ScopeNode)

    @_MetaParser_builder(hints="{")
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
    @_MetaParser_builder(hints="[")
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
    @_MetaParser_builder(hints="name")
    def parse_name(self):
        if not self.stream.is_next("name"):
            return
        node = nodes.NameNode()
        node.name = self.stream.read("name").value
        return node

    """
    PrefixedNameParser -----------------------------
    """
    @_MetaParser_builder(hints="@")
    def parse_attribute(self):
        return self._parse_prefixed_name("@", nodes.AttributeNode)

    @_MetaParser_builder(hints="!")
    def parse_flag(self):
        return self._parse_prefixed_name("!", nodes.FlagNode)

    @_MetaParser_builder(hints="#")
    def parse_uid(self):
        return self._parse_prefixed_name("#", nodes.UIDNode)

    @_MetaParser_builder(hints="$")
    def parse_variable(self):
        return self._parse_prefixed_name("$", nodes.VariableNode)

    @_MetaParser_builder(hints="%")
    def parse_format(self):
        return self._parse_prefixed_name("%", nodes.FormatNode)

    @_MetaParser_builder(hints="?")
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
    @_MetaParser_builder(priority=2, hints=["int", ".."])
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
    @_MetaParser_builder(priority=1, hints="float")
    def parse_float(self):
        return self._parse_literal(nodes.FloatNode)

    @_MetaParser_builder(hints="int")
    def parse_int(self):
        return self._parse_literal(nodes.IntNode)

    @_MetaParser_builder(hints="string")
    def parse_string(self):
        return self._parse_literal(nodes.StringNode)

    @_MetaParser_builder(hints="boolean")
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
    @_MetaParser_builder(hints="wirldcard")
    def parse_wildcard(self):
        if self.stream.is_next("*"):
            self.stream.read()
            return nodes.WildcardNode()
        return
