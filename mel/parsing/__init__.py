from .. import tokens
from .. import nodes

from .literal import LiteralParser, IntParser, RangeParser, WildcardParser
from .keyword import KeywordParser, TagParser

from .base import (
    BaseParser,
    TokenParser,
    MultiParser,
    subparser,
    indexed
)
from ..exceptions import (
    UnexpectedTokenError,
    KeywordNotFoundError,
    ExpectedKeywordError,
    ExpectedValueError,
    KeyNotFoundError
)


class Parser(BaseParser):
    def parse(self):
        node = self.subparse(RootParser)
        if self.stream.is_eof():
            return node
        self.error(UnexpectedTokenError)


# LIST ======================================================

@subparser
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
            _object = self.subparse(ValueParser)
            if not _object:
                break
            node.add(_object)


# PATH ======================================================

@subparser
class PathParser(BaseParser):
    Node = nodes.PathNode

    @indexed
    def parse(self):
        _keyword = self.subparse(KeywordParser)
        if not _keyword:
            return
        node = self.build_node()
        node.add(_keyword)
        self.parse_tail(node)
        return node

    def parse_tail(self, node):
        while self.stream.is_next(tokens.SubNodeToken):
            self.stream.read()
            _keyword = self.subparse(KeywordParser)
            if _keyword:
                node.add(_keyword)
            else:
                self.error(KeywordNotFoundError)


# STRUCT ==================================================

class StructParser(BaseParser):
    def parse_expressions(self, node):
        while True:
            expression = self.subparse(ExpressionParser)
            if not expression:
                break
            node.add(expression)


class KeyStructParser(StructParser):
    KeyParser = None

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
        key = self.subparse(self.KeyParser)
        if not key:
            self.error(KeyNotFoundError)
        node.key = key


# ROOT ======================================================

@subparser
class RootParser(StructParser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
        return node


# STRUCT KEY ====================================================

@subparser
class AnonymKeyParser(TokenParser):
    Node = nodes.AnonymKeyNode
    Token = tokens.AnonymKeyToken


@subparser
class DefaultDocKeyParser(TokenParser):
    Node = nodes.DefaultDocKeyNode
    Token = tokens.DefaultDocKeyToken


@subparser
class DefaultFormatKeyParser(TokenParser):
    Node = nodes.DefaultFormatKeyNode
    Token = tokens.DefaultFormatKeyToken


@subparser
class ObjectKeyParser(MultiParser):
    options = (
        AnonymKeyParser,
        DefaultDocKeyParser,
        DefaultFormatKeyParser,
        PathParser
    )


@subparser
class QueryKeyParser(MultiParser):
    options = (
        AnonymKeyParser,
        PathParser
    )


# OBJECT ======================================================

@subparser
class ObjectParser(KeyStructParser):
    Node = nodes.ObjectNode
    KeyParser = ObjectKeyParser
    FirstToken = tokens.StartObjectToken
    LastToken = tokens.EndObjectToken

    def _build_subtree(self, node):
        key, *keywords = node.path
        node.key = key
        for _keyword in keywords:
            subnode = self.build_node()
            subnode.key = _keyword
            node.add(subnode)
            node = subnode
        return node

    def parse_expressions(self, node):
        # node = self._build_subtree(node)
        super().parse_expressions(node)


# QUERY ======================================================

@subparser
class QueryParser(KeyStructParser):
    Node = nodes.QueryNode
    KeyParser = QueryKeyParser
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken


# REFERENCE ====================================================

@subparser
class ReferenceParser(BaseParser):
    Node = nodes.ReferenceNode

    @indexed
    def parse(self):
        head = self.subparse(HeadReferenceParser)
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
        child = self.subparse(ChildReferenceParser)
        if not child:
            self.error(ExpectedKeywordError)
        node.add(child)
        return child


@subparser
class HeadReferenceParser(MultiParser):
    options = (
        QueryParser,
        KeywordParser
    )


@subparser
class ChildReferenceParser(MultiParser):
    options = (
        WildcardParser,
        TagParser,
        RangeParser,
        IntParser,
        ListParser,
        ObjectParser,
        QueryParser,
        KeywordParser
    )


# RELATION ====================================================

class PathRelationParser(BaseParser):
    @indexed
    def parse(self):
        self.stream.save()
        path = self.subparse(PathParser)
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
        value = self.subparse(ValueParser)
        if not value:
            self.error(ExpectedValueError)
        return value


@subparser
class EqualParser(PathRelationParser):
    Node = nodes.EqualNode
    SignToken = tokens.EqualToken


@subparser
class DifferentParser(PathRelationParser):
    Node = nodes.DifferentNode
    SignToken = tokens.DifferentToken


@subparser
class GreaterThanParser(PathRelationParser):
    Node = nodes.GreaterThanNode
    SignToken = tokens.GreaterThanToken


@subparser
class GreaterThanEqualParser(PathRelationParser):
    Node = nodes.GreaterThanEqualNode
    SignToken = tokens.GreaterThanEqualToken


@subparser
class LessThanParser(PathRelationParser):
    Node = nodes.LessThanNode
    SignToken = tokens.LessThanToken


@subparser
class LessThanEqualParser(PathRelationParser):
    Node = nodes.LessThanEqualNode
    SignToken = tokens.LessThanEqualToken


@subparser
class InParser(PathRelationParser):
    Node = nodes.InNode
    SignToken = tokens.InToken


@subparser
class NotInParser(PathRelationParser):
    Node = nodes.NotInNode
    SignToken = tokens.NotInToken


@subparser
class RelationParser(MultiParser):
    options = (
        EqualParser,
        DifferentParser,
        GreaterThanParser,
        GreaterThanEqualParser,
        LessThanParser,
        LessThanEqualParser,
        InParser,
        NotInParser
    )


# VALUE ======================================================

@subparser
class ValueParser(MultiParser):
    options = (
        ReferenceParser,
        LiteralParser,
        ListParser,
        ObjectParser,
    )


# EXPRESSION ======================================================

@subparser
class ExpressionParser(MultiParser):
    options = (
        TagParser,
        RelationParser,
        ValueParser
    )
