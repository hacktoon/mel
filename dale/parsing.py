from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    ValueChainError,
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
            "value": ValueParser,
            "number": NumberParser,
            "range": RangeParser,
            "property": PropertyParser,
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


class StructParser(BaseParser):
    def _parse_key(self, node):
        if self.stream.is_next(":"):
            self.stream.read()
        else:
            node.key = self.parse_value()

    def _parse_value(self, scope):
        value_node = self.parse_value()
        if not value_node:
            return
        relation = self._parse_relation(value_node)
        if relation:
            return relation
        if value_node.id == "flag":
            scope.flags[value_node.value] = value_node
        if value_node.id == "scope":
            self._update_property_map(scope, value_node)
        scope.add(value_node)
        return value_node

    def _parse_relation(self, target):
        return RelationParser(self.stream).parse()

    def _update_property_map(self, scope, value_node):
        key_map = {
            "property": scope.properties,
            "flag": scope.flags,
            "uid": scope.uids,
            "doc": scope.docs,
            "variable": scope.variables,
            "format": scope.formats,
        }
        key_id = value_node.key.id if value_node.key else ''
        if key_id in key_map:
            key_map[key_id][value_node.key.value] = value_node


class RootParser(StructParser):
    @indexed
    def parse(self):
        node = self._create_node(nodes.RootNode)
        while not self.stream.is_eof():
            value = self.parse_value()
            if value:
                node.add(value)
            elif not self.stream.is_eof():
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
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, scope):
        end_token = self.delimiters[1]
        inside_scope = not self.stream.is_next(end_token)
        not_eof = not self.stream.is_eof()
        while inside_scope and not_eof:
            if not self._parse_value(scope):
                break


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
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, node):
        end_token = self.delimiters[1]
        inside_list = not self.stream.is_next(end_token)
        not_eof = not self.stream.is_eof()
        while inside_list and not_eof:
            value = self.parse_value()
            if not value:
                break
            node.add(value)


class ValueParser(BaseParser):
    @indexed
    def parse(self):
        node = self._parse_value()
        if node:
            self._parse_chain(node)
        return node

    def _parse_value(self):
        methods = [
            self.parse_range,
            self.parse_number,
            self.parse_boolean,
            self.parse_string,
            self.parse_property,
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

    def _parse_chain(self, node):
        while self.stream.is_next("/"):
            sep = self.stream.read("/")
            value = self._parse_value()
            if not value:
                raise ValueChainError(sep.index[0])
            node.add(value)


class PropertyParser(BaseParser):
    PREFIX_MAP = {
        "#": nodes.UIDNode,
        "!": nodes.FlagNode,
        "%": nodes.FormatNode,
        "$": nodes.VariableNode,
        "?": nodes.DocNode,
    }

    @indexed
    def parse(self):
        next = self.stream.peek()
        node_class = nodes.PropertyNode
        if next.id in self.PREFIX_MAP:
            node_class = self.PREFIX_MAP[next.id]
            self.stream.read(next.id)
        elif not self.stream.is_next("name"):
            return
        return self._parse_property(node_class)

    def _parse_property(self, node_class):
        if not self.stream.is_next("name"):
            raise NameNotFoundError(self.stream.peek().index[0])
        node = self._create_node(node_class)
        node.value = self.stream.read("name").value
        return node


class RelationParser(BaseParser):
    @indexed
    def parse(self):
        target = self.parse_property()
        if not target:
            return
        if not self.stream.is_next("="):
            return
        node = self._create_node(nodes.RelationNode)
        node.target = target
        node.relationship = self.stream.read()
        node.value = self.parse_value()
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
