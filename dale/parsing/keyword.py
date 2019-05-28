from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)

from ..exceptions import NameNotFoundError



@subparser
class KeywordParser(MultiParser):
    Node = nodes.KeywordNode
    options = (
        nodes.NameNode,
        nodes.ConceptNode,
        nodes.AliasNode,
        nodes.FormatNode,
        nodes.DocNode,
        nodes.MetaNode
    )


@subparser
class NameParser(TokenParser):
    Node = nodes.NameNode
    Token = tokens.NameToken


@subparser
class ConceptParser(TokenParser):
    Node = nodes.ConceptNode
    Token = tokens.ConceptToken


class PrefixedNameParser(BaseParser):
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
class TagParser(PrefixedNameParser):
    Node = nodes.TagNode
    Token = tokens.TagPrefixToken


@subparser
class AliasParser(PrefixedNameParser):
    Node = nodes.AliasNode
    Token = tokens.AliasPrefixToken


@subparser
class FormatParser(PrefixedNameParser):
    Node = nodes.FormatNode
    Token = tokens.FormatPrefixToken


@subparser
class DocParser(PrefixedNameParser):
    Node = nodes.DocNode
    Token = tokens.DocPrefixToken


@subparser
class MetaParser(PrefixedNameParser):
    Node = nodes.MetaNode
    Token = tokens.MetaPrefixToken