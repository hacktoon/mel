import functools

from . import tokens
from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    NameNotFoundError,
    KeywordNotFoundError,
    ObjectNotFoundError,
    InfiniteRangeError
)


_subparsers = {}


@functools.lru_cache()
def get_subparser(id, stream):
    return _subparsers[id](stream)


# decorator - register a Parser class as a subparser
def subparser(cls):
    _subparsers[cls.Node.id] = cls
    return cls


# decorator - add stream data to node instance via parser method
def indexed(parse_method):
    @functools.wraps(parse_method)
    def surrogate(self):
        first = self.stream.peek()
        node = parse_method(self)
        if not node:
            return
        last = self.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        node.text = self.stream.text
        return node
    return surrogate


# BASE PARSER ===========================

class Parser:
    def __init__(self, stream):
        self.stream = stream

    def build_node(self):
        return self.Node()

    def parse(self):
        node = RootParser(self.stream).parse()
        if self.stream.is_eof():
            return node
        token = self.stream.peek()
        raise UnexpectedTokenError(token)

    def subparse(self, Node):
        return get_subparser(Node.id, self.stream).parse()

    def __repr__(self):
        return self.__class__.__name__


# SPECIALIZED PARSERS ===========================

class MultiParser(Parser):
    options = tuple()

    @indexed
    def parse(self):
        for option in self.options:
            node = self.subparse(option)
            if node:
                return node
        return


class TokenParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        node = self.build_node()
        node.value = self.stream.read().value
        return node


class AliasParser(Parser):
    @indexed
    def parse(self):
        node = self.build_node()
        node.node = self.subparse(self.Alias)
        return node


# ROOT ======================================================

class RootParser(Parser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_metadata(node)
        self.parse_objects(node)
        return node

    def parse_metadata(self, node):
        while True:
            metadata = self.subparse(nodes.MetaNode)
            if not metadata:
                return
            node.add(metadata)

    def parse_objects(self, node):
        while True:
            _object = self.subparse(nodes.ObjectNode)
            if not _object:
                break
            node.add(_object)


# METADATA ======================================================

@subparser
class MetaParser(MultiParser):
    Node = nodes.MetaNode
    options = (
        nodes.FlagNode,
        nodes.RelationNode
    )


# RELATION ======================================================

@subparser
class RelationParser(MultiParser):
    Node = nodes.RelationNode
    options = (
        nodes.EqualNode,
        nodes.DifferentNode,
        nodes.GreaterThanNode,
        nodes.GreaterThanEqualNode,
        nodes.LessThanNode,
        nodes.LessThanEqualNode
    )

    @indexed
    def parse(self):
        self.stream.save()
        path = self.subparse(nodes.PathNode)
        if not path:
            return
        node = super().parse()
        if not node:
            self.stream.restore()
            return
        node.path = path
        return node


class ComparisonParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        self.stream.read()
        _object = self.subparse(nodes.ObjectNode)
        if not _object:
            raise ObjectNotFoundError(self.stream.peek())
        node = self.build_node()
        node.value = _object
        return node


@subparser
class EqualParser(ComparisonParser):
    Node = nodes.EqualNode
    Token = tokens.EqualToken


@subparser
class DifferentParser(ComparisonParser):
    Node = nodes.DifferentNode
    Token = tokens.DifferentToken


@subparser
class GreaterThanParser(ComparisonParser):
    Node = nodes.GreaterThanNode
    Token = tokens.GreaterThanToken


@subparser
class GreaterThanEqualParser(ComparisonParser):
    Node = nodes.GreaterThanEqualNode
    Token = tokens.GreaterThanEqualToken


@subparser
class LessThanParser(ComparisonParser):
    Node = nodes.LessThanNode
    Token = tokens.LessThanToken


@subparser
class LessThanEqualParser(ComparisonParser):
    Node = nodes.LessThanEqualNode
    Token = tokens.LessThanEqualToken


# OBJECT ======================================================

@subparser
class ObjectParser(MultiParser):
    Node = nodes.ObjectNode
    options = (
        nodes.ReferenceNode,
        nodes.LiteralNode,
        nodes.ListNode,
        nodes.ScopeNode
    )


# STRUCT ======================================================

class StructParser(MultiParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_key(node)
        self.parse_metadata(node)
        self.parse_objects(node)
        self.stream.read(self.LastToken)
        return node

    def parse_key(self, node):
        if self.stream.is_next(tokens.NullKeyToken):
            self.stream.read()
            return
        node.key = self.subparse(nodes.PathNode)

    def parse_metadata(self, node):
        while True:
            metadata = self.subparse(nodes.MetaNode)
            if not metadata:
                return
            node.add(metadata)

    def parse_objects(self, node):
        while True:
            _object = self.subparse(nodes.ObjectNode)
            if not _object:
                break
            node.add(_object)


@subparser
class ScopeParser(StructParser):
    Node = nodes.ScopeNode
    FirstToken = tokens.StartScopeToken
    LastToken = tokens.EndScopeToken


@subparser
class QueryParser(StructParser):
    Node = nodes.QueryNode
    FirstToken = tokens.StartQueryToken
    LastToken = tokens.EndQueryToken


# LIST ======================================================

@subparser
class ListParser(Parser):
    Node = nodes.ListNode
    FirstToken = tokens.StartListToken
    LastToken = tokens.EndListToken

    @indexed
    def parse(self):
        if not self.stream.is_next(self.FirstToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_objects(node)
        self.stream.read(self.LastToken)
        return node

    def parse_objects(self, node):
        while True:
            _object = self.subparse(nodes.ObjectNode)
            if not _object:
                break
            node.add(_object)


# REFERENCE ======================================================

@subparser
class ReferenceParser(Parser):
    Node = nodes.ReferenceNode
    SubNodes = (nodes.ChildReferenceNode, nodes.MetaKeywordNode)
    Prefixes = (tokens.ChildToken, tokens.MetaPathToken)

    @indexed
    def parse(self):
        head = self.subparse(nodes.HeadReferenceNode)
        if not head:
            return
        node = self.build_node()
        node.add(head)
        while self.stream.peek() in self.Prefixes:
            for Node in self.SubNodes:
                subnode = self.subparse(Node)
                if subnode:
                    node.add(subnode)
        return node


@subparser
class HeadReferenceParser(MultiParser):
    Node = nodes.HeadReferenceNode
    options = (
        nodes.QueryNode,
        nodes.KeywordNode,
        nodes.WildcardNode
    )


@subparser
class ChildReferenceParser(MultiParser):
    Node = nodes.ChildReferenceNode
    options = (
        nodes.HeadReferenceNode,
        nodes.RangeReferenceNode,
        nodes.IntReferenceNode,
        nodes.SubreferenceListNode
    )

    def parse(self):
        if not self.stream.is_next(tokens.ChildToken):
            return
        self.stream.read()
        return super().parse()


@subparser
class RangeReferenceParser(AliasParser):
    Node = nodes.RangeReferenceNode
    Alias = nodes.RangeNode


@subparser
class IntReferenceParser(AliasParser):
    Node = nodes.IntReferenceNode
    Alias = nodes.IntNode


@subparser
class SubreferenceListParser(AliasParser):
    Node = nodes.SubreferenceListNode
    Alias = nodes.ListNode


# PATH ======================================================

@subparser
class PathParser(Parser):
    Node = nodes.PathNode
    SubNodes = (nodes.ChildKeywordNode, nodes.MetaKeywordNode)
    Prefixes = (tokens.ChildToken, tokens.MetaPathToken)

    @indexed
    def parse(self):
        keyword = self.subparse(nodes.KeywordNode)
        if not keyword:
            return
        node = self.build_node()
        node.add(keyword)
        while self.stream.peek() in self.Prefixes:
            for Node in self.SubNodes:
                keyword = self.subparse(Node)
                if keyword:
                    node.add(keyword)
        return node


class SubPathParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        prefix = self.stream.read()
        keyword = self.subparse(nodes.KeywordNode)
        if not keyword:
            raise KeywordNotFoundError(prefix)
        node = self.build_node()
        node.keyword = keyword
        return node


@subparser
class MetaPathParser(SubPathParser):
    Node = nodes.MetaKeywordNode
    Token = tokens.MetaPathToken


@subparser
class ChildPathParser(SubPathParser):
    Node = nodes.ChildKeywordNode
    Token = tokens.ChildToken


# KEYWORD ===========================

@subparser
class KeywordParser(MultiParser):
    Node = nodes.KeywordNode
    options = (
        nodes.NameNode,
        nodes.ReservedNameNode,
        nodes.UIDNode,
        nodes.VariableNode,
        nodes.FormatNode,
        nodes.DocNode
    )


@subparser
class NameParser(TokenParser):
    Node = nodes.NameNode
    Token = tokens.NameToken


@subparser
class ReservedNameParser(TokenParser):
    Node = nodes.ReservedNameNode
    Token = tokens.ReservedNameToken


class PrefixedNameParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        prefix = self.stream.read()
        node = self.build_node()
        if self.stream.is_next(tokens.NameToken):
            node.value = self.stream.read().value
            return node
        raise NameNotFoundError(prefix)


@subparser
class FlagParser(PrefixedNameParser):
    Node = nodes.FlagNode
    Token = tokens.FlagPrefixToken


@subparser
class UIDParser(PrefixedNameParser):
    Node = nodes.UIDNode
    Token = tokens.UIDPrefixToken


@subparser
class VariableParser(PrefixedNameParser):
    Node = nodes.VariableNode
    Token = tokens.VariablePrefixToken


@subparser
class FormatParser(PrefixedNameParser):
    Node = nodes.FormatNode
    Token = tokens.FormatPrefixToken


@subparser
class DocParser(PrefixedNameParser):
    Node = nodes.DocNode
    Token = tokens.DocPrefixToken


# LITERAL ===========================

@subparser
class LiteralParser(MultiParser):
    Node = nodes.LiteralNode
    options = (
        nodes.IntNode,
        nodes.FloatNode,
        nodes.StringNode,
        nodes.BooleanNode
    )


@subparser
class IntParser(TokenParser):
    Node = nodes.IntNode
    Token = tokens.IntToken


@subparser
class FloatParser(TokenParser):
    Node = nodes.FloatNode
    Token = tokens.FloatToken


@subparser
class StringParser(TokenParser):
    Node = nodes.StringNode
    Token = tokens.StringToken


@subparser
class BooleanParser(TokenParser):
    Node = nodes.BooleanNode
    Token = tokens.BooleanToken


@subparser
class WildcardParser(TokenParser):
    Node = nodes.WildcardNode
    Token = tokens.WildcardToken


# RANGE ===========================

@subparser
class RangeParser(Parser):
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
