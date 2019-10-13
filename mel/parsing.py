import re

from .nodes import Node
from .exceptions import ParsingError


_parsers = {}


# CLASSES =======================================

class Parser:
    def __init__(self, source, grammar=None):
        self.source = source
        self.grammar = grammar

    def parse(self):
        stream = TokenStream(self.source)
        return _parsers['root'](stream)


class TokenStream:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.index_cache = 0

    def save(self):
        self.index_cache = self.index
        return self.index

    def restore(self, _index):
        index = self.index_cache if _index is None else _index
        self.index = index

    def read(self, id):
        parser = _parsers[id]
        token = parser(self.text, self.index)
        self.index += len(token)
        return token


class Token:
    def __init__(self, id, text, index):
        self.id = id
        self.text = text
        self.index = index

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return "TOKEN({!r})".format(self.text)

    def __str__(self):
        start, end = self.index
        return self.text[start:end]


# REGISTERS =======================================

def rule(id, parser):
    def base_rule_parser(stream):
        index = stream.save()
        try:
            return parser(stream)
        except ParsingError as error:
            stream.restore(index)
            raise error
    _parsers[id] = base_rule_parser
    return base_rule_parser


def token(id, string=None):
    pattern = re.compile(string or re.escape(id))

    def base_token_parser(text, index=0):
        match = pattern.match(text, index)
        if match:
            text, index = match.group(0), match.span()
            return Token(id, text, index)
        raise ParsingError
    _parsers[id] = base_token_parser
    return base_token_parser


# PARSERS =======================================

def zero_many(parser):
    def zero_many_parser(stream):
        nodes = []
        while True:
            try:
                node = parser(stream)
                nodes.append(node)
            except ParsingError:
                break
        return nodes
    return zero_many_parser


def one_of(*parsers):
    def one_of_parser(stream):
        for parser in parsers:
            try:
                node = parser(stream)
                return node
            except ParsingError:
                pass
        raise ParsingError
    return one_of_parser


def maybe(parser):
    def maybe_parser(stream):
        try:
            return parser(stream)
        except ParsingError:
            return
    return maybe_parser


def seq(*parsers):
    def seq_parser(stream):
        nodes = []
        for parser in parsers:
            node = parser(stream)
            nodes.append(node)
        return nodes
    return seq_parser


def group(*parsers):
    pass


def r(id):
    def rule_parser(stream):
        return _parsers[id](stream)
    return rule_parser


def t(id):
    def token_parser(stream):
        token = stream.read(id)
        return Node(token.text)
    return token_parser


def s(id):
    def string_parser(stream):
        return stream.read(id)
    return string_parser


# GRAMMAR TOKENS ===================================

token("space", r"(\s|;|,)*")
token("comment", r"--[^\n\r]*")
token("string", r"'[^']*'|\"[^\"]*\"")
token("float", r"-?\d*\.\d+([eE][-+]?\d+)?\b")
token("int", r"-?\d+\b")
token("name", r"[a-z]\w*")
token("concept", r"[A-Z]\w*")
token("default-format", r"%:")
token("default-doc", r"\?:")
token("anonym", r":")
token("wildcard", r"\*")
token("..")
token("><")
token(">=")
token("<>")
token("<=")
token("!=")
token("/")
token(".")
token(">")
token("<")
token("#")
token("?")
token("=")
token("!")
token("%")
token("@")
token("$")
token("_")
token("[")
token("]")
token("(")
token(")")
token("{")
token("}")


# GRAMMAR RULES ===================================

rule('root', zero_many(r('expression')))

rule('expression', one_of(r('tag'), r('relation'), r('value')))

rule('tag', seq(s('#'), t('name')))

rule('relation', seq(r('path'), one_of(
    t('equal'), t('diff'), t('lte'), t('lt'),
    t('gte'), t('gt'), t('in'), t('out')
)))
rule('equal', seq(s('='), r('value')))
rule('diff', seq(s('!='), r('value')))
rule('lt', seq(s('<'), r('value')))
rule('lte', seq(s('<='), r('value')))
rule('gt', seq(s('>'), r('value')))
rule('gte', seq(s('>='), r('value')))
rule('in', seq(s('><'), r('value')))
rule('out', seq(s('<>'), r('value')))

rule('path', seq(r('keyword'), zero_many(
    one_of(r('sub-path'), r('meta-path')))
))
rule('sub-path', seq(s('/'), r('keyword')))
rule('meta-path', seq(s('.'), r('keyword')))

rule('keyword', one_of(
    t('name'), t('concept'), r('log'), r('alias'),
    r('cache'), r('format'), r('meta'), r('doc')
))
rule('log', seq(s('!'), t('name')))
rule('alias', seq(s('@'), t('name')))
rule('cache', seq(s('$'), t('name')))
rule('format', seq(s('%'), t('name')))
rule('meta', seq(s('_'), t('name')))
rule('doc', seq(s('?'), t('name')))

rule('value', one_of(r('reference'), r('literal'), r('list'), r('object')))

rule('reference', seq(
    one_of(r('query'), r('keyword')),
    zero_many(r('sub-reference'))
))
rule('sub-reference', seq(s('/'), one_of(
    r('range'), t('int'), r('tag'), r('list'), r('object'),
    r('query'), r('keyword'), t('wildcard')
)))

rule('literal', one_of(t('int'), t('float'), t('string'), t('boolean')))

rule('list', seq(s('['), zero_many(r('value')), s(']')))

rule('range', one_of(
    seq(s('..'), t('int')),
    seq(t('int'), s('..'), maybe(t('int')))
))

rule('object', seq(
    s('('), r('object-key'), zero_many(r('expression')), s(')')
))
rule('object-key', one_of(
    t('anonym-path'), t('default-format'), t('default-doc'), r('path')
))

rule('query', seq(s('{'), r('query-key'), zero_many(r('expression')), s('}')))
rule('query-key', one_of(t('anonym-path'), r('path')))
