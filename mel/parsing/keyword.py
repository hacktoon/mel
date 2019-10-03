from .. import nodes

from .constants import (
    KEYWORD,
    NAME,
    CONCEPT,
    LOG,
    ALIAS,
    CACHE,
    FORMAT,
    DOC,
    TAG
)
from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)


@subparser
class NameParser(TokenParser):
    id = NAME
    Node = nodes.NameKeywordNode
    token = 'name'


@subparser
class ConceptParser(TokenParser):
    id = CONCEPT
    Node = nodes.ConceptKeywordNode
    token = 'concept'


class PrefixedNameParser(BaseParser):
    @indexed
    def parse(self):
        self.parse_token(self.token)
        node = self.build_node()
        node.value = self.parse_token('name')
        return node


@subparser
class TagParser(PrefixedNameParser):
    id = TAG
    Node = nodes.TagKeywordNode
    token = 'tag'


@subparser
class LogParser(PrefixedNameParser):
    id = LOG
    Node = nodes.LogKeywordNode
    token = 'log'


@subparser
class AliasParser(PrefixedNameParser):
    id = ALIAS
    Node = nodes.AliasKeywordNode
    token = 'alias'


@subparser
class CacheParser(PrefixedNameParser):
    id = CACHE
    Node = nodes.CacheKeywordNode
    token = 'cache'


@subparser
class FormatParser(PrefixedNameParser):
    id = FORMAT
    Node = nodes.FormatKeywordNode
    token = 'format'


@subparser
class DocParser(PrefixedNameParser):
    id = DOC
    Node = nodes.DocKeywordNode
    token = 'doc'


@subparser
class KeywordParser(BaseParser):
    id = KEYWORD

    def parse(self):
        return self.parse_alternative(
            NAME,
            CONCEPT,
            LOG,
            ALIAS,
            CACHE,
            FORMAT,
            DOC,
        )
