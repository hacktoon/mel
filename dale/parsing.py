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


class Parser:
    priority = 0
    hints = []
    node = nodes.Node

    def __init__(self, stream):
        self.stream = stream

    def buildNode(self):
        return self.node()

    @functools.lru_cache()
    def get_subparsers(self, parser, hint):
        classes = parser.subparsers[hint.id]
        sorted_cls = sorted(classes, key=lambda p: p.priority, reverse=True)
        return [cls(self.stream) for cls in sorted_cls]

    @indexed
    def parse(self):
        node = nodes.RootNode()
        self.parse_expressions(node)
        if not self.stream.is_eof():
            token = self.stream.peek()
            raise UnexpectedTokenError(token)
        return node

    def parse_expressions(self, node):
        while True:
            exp = self.parse_expression()
            if not exp:
                break
            node.add(exp)

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
        subparsers = self.get_subparsers(ObjectParser, token)
        for parser in subparsers:
            node = parser.parse()
            if node:
                self._parse_subnode(node)
                break
        return node

    def _parse_subnode(self, node):
        if not self.stream.is_next(tokens.SubOperatorToken):
            return
        token = self.stream.read()
        obj = self.parse_object()
        if not obj:
            raise SubNodeError(token)
        node.add(obj)
        self._parse_subnode(obj)

    @indexed
    def parse_relation(self):
        token = self.stream.peek()
        subparsers = self.get_subparsers(CriteriaParser, token)
        for parser in subparsers:
            return parser.parse()
        return

    def parse_objects(self, node):
        while True:
            obj = self.parse_object()
            if not obj:
                break
            node.add(obj)


class ObjectParser(Parser):
    subparsers = defaultdict(list)

    @classmethod
    def __init_subclass__(cls):
        for hint in cls.hints:
            ObjectParser.subparsers[hint.id].append(cls)


class StructParser(ObjectParser):
    def parse(self):
        start, end = self.delimiters
        node = self.buildNode()
        self.stream.read(start)
        self._parse_key(node)
        self.parse_expressions(node)
        self.stream.read(end)
        return node

    def _parse_key(self, node):
        if self.stream.is_next(tokens.NullKeyToken):
            self.stream.read()
        else:
            node.key = self.parse_expression() or nodes.NullNode()


class ScopeParser(StructParser):
    node = nodes.ScopeNode
    delimiters = (tokens.StartScopeToken, tokens.EndScopeToken)
    hints = [tokens.StartScopeToken]


class QueryParser(StructParser):
    node = nodes.QueryNode
    delimiters = (tokens.StartQueryToken, tokens.EndQueryToken)
    hints = [tokens.StartQueryToken]


class ListParser(ObjectParser):
    node = nodes.ListNode
    hints = [tokens.StartListToken]

    def parse(self):
        node = self.buildNode()
        self.stream.read(tokens.StartListToken)
        self.parse_objects(node)
        self.stream.read(tokens.EndListToken)
        return node


class IdentifierParser2():
    node = nodes.IdentifierNode
    hints = [
        tokens.NameToken,
        tokens.SymbolToken,
        tokens.FlagPrefixToken,
        tokens.UIDPrefixToken,
        tokens.VariablePrefixToken,
        tokens.FormatPrefixToken,
        tokens.DocPrefixToken
    ]

    def parse(self):
        node = self.buildNode()
        token = self.stream.read(tokens.NameToken)
        node.name = token.value
        return node


class IdentifierParser(ObjectParser):
    node = nodes.IdentifierNode
    hints = [tokens.NameToken]

    def parse(self):
        node = self.buildNode()
        token = self.stream.read(tokens.NameToken)
        node.name = token.value
        return node


class PrefixedIdentifierParser(ObjectParser):
    def parse(self):
        symbol = self.stream.read(self.hints[0])
        node = self.buildNode()
        if self.stream.is_next(tokens.NameToken):
            node.name = self.stream.read().value
            return node
        raise NameNotFoundError(symbol)


class FlagParser(PrefixedIdentifierParser):
    node = nodes.FlagNode
    hints = [tokens.FlagPrefixToken]


class UIDParser(PrefixedIdentifierParser):
    node = nodes.UIDNode
    hints = [tokens.UIDPrefixToken]


class VariableParser(PrefixedIdentifierParser):
    node = nodes.VariableNode
    hints = [tokens.VariablePrefixToken]


class FormatParser(PrefixedIdentifierParser):
    node = nodes.FormatNode
    hints = [tokens.FormatPrefixToken]


class DocParser(PrefixedIdentifierParser):
    node = nodes.DocNode
    hints = [tokens.DocPrefixToken]


class RangeParser(ObjectParser):
    node = nodes.RangeNode
    hints = [tokens.IntToken, tokens.RangeToken]
    priority = 1

    def parse(self):
        node = self.buildNode()
        if self._parse_left_open(node):
            return node
        if self._parse_left_bound(node):
            return node
        return

    def _parse_left_open(self, node):
        if not self.stream.is_next(tokens.RangeToken):
            return
        _range = self.stream.read()
        if not self.stream.is_next(tokens.IntToken):
            raise InfiniteRangeError(_range)
        node.end = self.stream.read().value
        return True

    def _parse_left_bound(self, node):
        first_is_int = self.stream.is_next(tokens.IntToken)
        range_is_next = self.stream.peek(1) == tokens.RangeToken
        if not (first_is_int and range_is_next):
            return
        node.start = self.stream.read().value
        self.stream.read()
        if self.stream.is_next(tokens.IntToken):
            node.end = self.stream.read().value
        return True


class LiteralParser(ObjectParser):
    def parse(self):
        node = self.buildNode()
        token = self.stream.read(self.hints[0])
        node.value = token.value
        return node


class FloatParser(LiteralParser):
    node = nodes.FloatNode
    hints = [tokens.FloatToken]


class IntParser(LiteralParser):
    node = nodes.IntNode
    hints = [tokens.IntToken]


class StringParser(LiteralParser):
    node = nodes.StringNode
    hints = [tokens.StringToken]


class BooleanParser(LiteralParser):
    node = nodes.BooleanNode
    hints = [tokens.BooleanToken]


class CriteriaParser(Parser):
    subparsers = defaultdict(list)

    @classmethod
    def __init_subclass__(cls):
        for hint in cls.hints:
            CriteriaParser.subparsers[hint.id].append(cls)

    def parse(self):
        token = self.stream.read(self.hints[0])
        obj = self.parse_object()
        if not obj:
            raise RelationError(token)
        node = self.buildNode()
        node.value = obj
        return node


class EqualsParser(CriteriaParser):
    node = nodes.EqualNode
    hints = [tokens.EqualsToken]


class DifferentParser(CriteriaParser):
    node = nodes.DifferentNode
    hints = [tokens.DifferentToken]


class GreaterThanParser(CriteriaParser):
    node = nodes.GreaterThanNode
    hints = [tokens.GreaterThanToken]


class GreaterThanEqualParser(CriteriaParser):
    node = nodes.GreaterThanEqualNode
    hints = [tokens.GreaterThanEqualToken]


class LessThanParser(CriteriaParser):
    node = nodes.LessThanNode
    hints = [tokens.LessThanToken]


class LessThanEqualParser(CriteriaParser):
    node = nodes.LessThanEqualNode
    hints = [tokens.LessThanEqualToken]


class WildcardParser(ObjectParser):
    node = nodes.WildcardNode
    hints = [tokens.WildcardToken]

    def parse(self):
        node = self.buildNode()
        token = self.stream.read(self.hints[0])
        node.value = token.value
        return node
