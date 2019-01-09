from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    SubNodeError,
    NameNotFoundError
)


def indexed(method):
    def surrogate(self):
        first = self.stream.peek()
        node = method(self)
        if not node:
            return
        last = self.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        return node

    return surrogate


class BaseParser:
    def __init__(self, stream):
        self.stream = stream
        self.PARSER_MAP = {
            "string": StringParser,
            "boolean": BooleanParser,
            "wildcard": WildcardParser,
            "object": ObjectParser,
            "number": NumberParser,
            "range": RangeParser,
            "name": NameParser,
            "scope": ScopeParser,
            "query": QueryParser,
            "list": ListParser,
        }

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node

    def __getattr__(self, attr_name):
        if not attr_name.startswith("parse_"):
            raise AttributeError("Invalid parsing method.")
        parser_id = attr_name.replace("parse_", "")
        if parser_id not in self.PARSER_MAP:
            raise AttributeError("Invalid parsing id.")
        parser_class = self.PARSER_MAP[parser_id]
        return parser_class(self.stream).parse


class Parser(BaseParser):
    @indexed
    def parse(self):
        return RootParser(self.stream).parse()


class ObjectParser(BaseParser):
    @indexed
    def parse(self):
        node = self._parse_object()
        if node:
            self._parse_subnode(node)
        return node

    def _parse_object(self):
        methods = [
            self.parse_range,
            self.parse_number,
            self.parse_boolean,
            self.parse_string,
            self.parse_name,
            self.parse_scope,
            self.parse_query,
            self.parse_list,
            self.parse_wildcard,
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    def _parse_subnode(self, node):
        if not self.stream.is_next("/"):
            return
        separator = self.stream.read()
        obj = self._parse_object()
        if not obj:
            raise SubNodeError(separator.index[0])
        node.add(obj)
        self._parse_subnode(obj)


class StructParser(BaseParser):
    def _parse_objects(self, scope):
        while True:
            obj = self._parse_object(scope)
            if not obj:
                break
            scope.add(obj)

    def _parse_object(self, scope):
        obj = self.parse_object()
        if not obj:
            return
        relation = self._parse_relation(obj)
        if relation:
            return relation
        return obj

    def _parse_relation(self, target):
        return RelationParser(self.stream).parse()


class RootParser(StructParser):
    @indexed
    def parse(self):
        node = self._create_node(nodes.RootNode)
        self._parse_objects(node)
        if not self.stream.is_eof():
            index = self.stream.peek().index[0]
            raise UnexpectedTokenError(index)
        return node


class ScopeParser(StructParser):
    node_class = nodes.ScopeNode
    delimiters = "()"

    @indexed
    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_next(start_token):
            return
        node = self._create_node(self.node_class)
        self.stream.read(start_token)
        self._parse_key(node)
        self._parse_objects(node)
        self.stream.read(end_token)
        return node

    def _parse_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read()
        else:
            node.key = self.parse_object()


class QueryParser(ScopeParser):
    node_class = nodes.QueryNode
    delimiters = "{}"


class ListParser(BaseParser):
    delimiters = "[]"

    @indexed
    def parse(self):
        start_token, end_token = self.delimiters
        if not self.stream.is_next(start_token):
            return
        node = self._create_node(nodes.ListNode)
        self.stream.read(start_token)
        self._parse_items(node)
        self.stream.read(end_token)
        return node

    def _parse_items(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)


class NameParser(BaseParser):
    PREFIX_MAP = {
        "#": nodes.UIDNode,
        "!": nodes.FlagNode,
        "%": nodes.FormatNode,
        "@": nodes.AttributeNode,
        "$": nodes.VariableNode,
        "?": nodes.DocNode,
    }

    @indexed
    def parse(self):
        next = self.stream.peek()
        node_class = nodes.NameNode
        if next.id in self.PREFIX_MAP:
            node_class = self.PREFIX_MAP[next.id]
            self.stream.read(next.id)
        elif not self.stream.is_next("name"):
            return
        return self._parse_name(node_class)

    def _parse_name(self, node_class):
        if not self.stream.is_next("name"):
            raise NameNotFoundError(self.stream.peek().index[0])
        node = self._create_node(node_class)
        node.name = self.stream.read("name").value
        return node


class RelationParser(BaseParser):
    @indexed
    def parse(self):
        target = self.parse_name()
        if not target:
            return
        if not self.stream.is_next("="):
            return
        node = self._create_node(nodes.RelationNode)
        node.target = target
        node.relationship = self.stream.read()
        node.value = self.parse_object()
        return node


class NumberParser(BaseParser):
    @indexed
    def parse(self):
        current = self.stream.peek()
        if current.id == "float":
            node_class = nodes.FloatNode
        elif current.id == "int":
            node_class = nodes.IntNode
        else:
            return
        node = self._create_node(node_class)
        node.value = self.stream.read().value
        return node


class RangeParser(BaseParser):
    @indexed
    def parse(self):
        _range = self._parse_range()
        if not _range:
            return
        node = self._create_node(nodes.RangeNode)
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


class StringParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next("string"):
            return
        node = self._create_node(nodes.StringNode)
        node.value = self.stream.read().value
        return node


class BooleanParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next("boolean"):
            return
        node = self._create_node(nodes.BooleanNode)
        node.value = self.stream.read().value
        return node


class WildcardParser(BaseParser):
    @indexed
    def parse(self):
        if self.stream.is_next("*"):
            self.stream.read()
            return self._create_node(nodes.WildcardNode)
        return
