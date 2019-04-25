import functools

from . import tokens
from . import nodes
from .exceptions import (
    UnexpectedTokenError,
    NameNotFoundError
)


_subparsers = {}


@functools.lru_cache()
def get_subparser(id, stream):
    return _subparsers[id](stream)


# decorator - register a Parser class as a subparser
def subparser(cls):
    _subparsers[cls.Node.id] = cls
    return cls


# decorator - enriches a node instance with stream data
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


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = RootParser(self.stream).parse()
        if self.stream.is_eof():
            return node
        token = self.stream.peek()
        raise UnexpectedTokenError(token)

    def subparse(self, id):
        return get_subparser(id, self.stream).parse()

    def __repr__(self):
        return self.__class__.__name__


class MultiParser(Parser):
    @indexed
    def parse(self):
        for option in self.options:
            node = self.subparse(option.id)
            if node:
                return node
        return


class TokenParser(Parser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        node = self.Node()
        node.value = self.stream.read().value
        return node


class RootParser(Parser):
    Node = nodes.RootNode

    @indexed
    def parse(self):
        pass


class MetadataParser(Parser):
    Node = nodes.MetadataNode

    @indexed
    def parse(self):
        pass


class ObjectParser(MultiParser):
    Node = nodes.ObjectNode
    options = (
        nodes.LiteralNode,
        nodes.ListNode,
        nodes.ReferenceNode,
        nodes.ScopeNode
    )


# NAMESPACE

class NamespaceParser(Parser):
    Node = nodes.NamespaceNode

    @indexed
    def parse(self):
        raise NotImplementedError


# IDENTIFIER

@subparser
class IdentifierParser(MultiParser):
    Node = nodes.IdentifierNode
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
        node = self.Node()
        if self.stream.is_next(tokens.NameToken):
            node.value = self.stream.read().value
            return node
        raise NameNotFoundError(prefix)


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


# LITERAL

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
