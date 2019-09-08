from .. import tokens
from .. import nodes

from .keyword import KeywordParser, TagParser

from .literal import (
    LiteralParser,
    IntParser,
)

from .base import (
    BaseParser,
    TokenParser,
    indexed
)

from ..exceptions import (
    InfiniteRangeError,
    KeywordNotFoundError,
    UnexpectedTokenError,
    ExpectedKeywordError,
    ExpectedValueError,
    KeyNotFoundError
)


# MAIN PARSER ===============================================

class Parser(BaseParser):
    def parse(self):
        node = self.read(RootParser)
        if self.stream.is_eof():
            return node
        self.error(UnexpectedTokenError)


# LIST ======================================================

class ListParser(BaseParser):
    Node = nodes.ListNode
    FirstToken = tokens.StartListToken
    LastToken = tokens.EndListToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_values(node)
        self.stream.read(self.LastToken)
        return node

    def parse_values(self, node):
        while True:
            _object = self.read(ValueParser)
            if not _object:
                break
            node.add(_object)


# RANGE ===========================

class RangeParser(BaseParser):
    Node = nodes.RangeNode

    @indexed
    def parse(self):
        node = self.build_node()
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
            self.error(InfiniteRangeError, _range)
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


class WildcardParser(TokenParser):
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken


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


# BASE STRUCT ===============================================

class StructParser(BaseParser):
    def parse_expressions(self, node):
        while True:
            expression = self.read(ExpressionParser)
            if not expression:
                break
            node.add(expression)


class KeyStructParser(StructParser):
    key_parsers = []

    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_key(node)
        self.parse_expressions(node)
        self.stream.read(self.LastToken)
        return node

    def parse_key(self, node):
        key = self.read_any(self.key_parsers)
        if not key:
            self.error(KeyNotFoundError)
        node.key = key


# ROOT ======================================================

class RootParser(StructParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
        return node


# STRUCT KEY ====================================================

class AnonymKeyParser(TokenParser):
    Node = nodes.AnonymKeyNode
    Token = tokens.AnonymKeyToken


class DefaultDocKeyParser(TokenParser):
    Node = nodes.DefaultDocKeyNode
    Token = tokens.DefaultDocKeyToken


class DefaultFormatKeyParser(TokenParser):
    Node = nodes.DefaultFormatKeyNode
    Token = tokens.DefaultFormatKeyToken


# OBJECT ======================================================

class ObjectParser(KeyStructParser):
    Node = nodes.ObjectNode
    FirstToken = tokens.StartObjectToken
    LastToken = tokens.EndObjectToken
    key_parsers = (
        AnonymKeyParser,
        DefaultDocKeyParser,
        DefaultFormatKeyParser,
        PathParser
    )


# QUERY ======================================================

class QueryParser(KeyStructParser):
    Node = nodes.QueryNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken
    key_parsers = (
        AnonymKeyParser,
        PathParser
    )


# REFERENCE ====================================================

class ReferenceParser(BaseParser):
    Node = nodes.ReferenceNode
    tail_parsers = (
        WildcardParser,
        TagParser,
        RangeParser,
        IntParser,
        ListParser,
        ObjectParser,
        QueryParser,
        KeywordParser
    )

    @indexed
    def parse(self):
        head = self.read_any([QueryParser, KeywordParser])
        if not head:
            return
        node = self.build_node()
        node.add(head)
        self.parse_body(node)
        return node

    def parse_body(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            self.parse_child(node)

    def parse_child(self, node):
        child = self.read_any(self.tail_parsers)
        if not child:
            self.error(ExpectedKeywordError)
        node.add(child)
        return child


# RELATION ====================================================

class PathRelationParser(BaseParser):
    @indexed
    def parse(self):
        self.stream.save()
        path = self.read(PathParser)
        if not path:
            return
        if not self.stream.is_next(self.SignToken):
            self.stream.restore()
            return
        self.stream.read()
        node = self.build_node()
        node.path = path
        node.value = self.parse_value()
        return node

    def parse_value(self):
        value = self.read(ValueParser)
        if not value:
            self.error(ExpectedValueError)
        return value


class EqualParser(PathRelationParser):
    Node = nodes.EqualNode
    SignToken = tokens.EqualToken


class DifferentParser(PathRelationParser):
    Node = nodes.DifferentNode
    SignToken = tokens.DifferentToken


class GreaterThanParser(PathRelationParser):
    Node = nodes.GreaterThanNode
    SignToken = tokens.GreaterThanToken


class GreaterThanEqualParser(PathRelationParser):
    Node = nodes.GreaterThanEqualNode
    SignToken = tokens.GreaterThanEqualToken


class LessThanParser(PathRelationParser):
    Node = nodes.LessThanNode
    SignToken = tokens.LessThanToken


class LessThanEqualParser(PathRelationParser):
    Node = nodes.LessThanEqualNode
    SignToken = tokens.LessThanEqualToken


class InParser(PathRelationParser):
    Node = nodes.InNode
    SignToken = tokens.InToken


class NotInParser(PathRelationParser):
    Node = nodes.NotInNode
    SignToken = tokens.NotInToken


class RelationParser(BaseParser):
    def parse(self):
        return self.read_any([
            EqualParser,
            DifferentParser,
            GreaterThanParser,
            GreaterThanEqualParser,
            LessThanParser,
            LessThanEqualParser,
            InParser,
            NotInParser
        ])


# VALUE ======================================================

class ValueParser(BaseParser):
    def parse(self):
        return self.read_any([
            ReferenceParser,
            LiteralParser,
            ListParser,
            ObjectParser,
        ])


# EXPRESSION ======================================================

class ExpressionParser(BaseParser):
    def parse(self):
        return self.read_any([
            TagParser,
            RelationParser,
            ValueParser
        ])
