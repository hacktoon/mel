from .. import tokens
from .. import nodes

from .keyword import KeywordParser, TagParser

from .literal import (
    LiteralParser,
    RangeParser,
    IntParser,
)

from .path import PathParser

from .base import (
    BaseParser,
    TokenParser,
    indexed
)

from ..exceptions import (
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
    PrefixToken = tokens.StartListToken
    SuffixToken = tokens.EndListToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.PrefixToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_values(node)
        self.stream.read(self.SuffixToken)
        return node

    def parse_values(self, node):
        while True:
            _object = self.read(ValueParser)
            if not _object:
                break
            node.add(_object)


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
        if not self.stream.is_next(self.PrefixToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_key(node)
        self.parse_expressions(node)
        self.stream.read(self.SuffixToken)
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
    PrefixToken = tokens.StartObjectToken
    SuffixToken = tokens.EndObjectToken
    key_parsers = (
        AnonymKeyParser,
        DefaultDocKeyParser,
        DefaultFormatKeyParser,
        PathParser
    )


# QUERY ======================================================

class QueryParser(KeyStructParser):
    Node = nodes.QueryNode
    PrefixToken = tokens.StartQueryToken
    SuffixToken = tokens.EndQueryToken
    key_parsers = (
        AnonymKeyParser,
        PathParser
    )


# WILDCARD ===============================================

class WildcardParser(TokenParser):
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken


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
