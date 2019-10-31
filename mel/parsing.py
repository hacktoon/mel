import re

from .nodes import (
    RuleNode,
    StringNode,
    PatternNode,
    EmptyNode
)
from .exceptions import ParsingError


ROOT_PARSER_ID = '_MEL_ROOT_ID'

_PARSERS = {}
_SKIP_PARSERS = {}


# CLASSES =======================================

class Parser:
    def __init__(self, source, grammar=None):
        self.source = source
        self.grammar = grammar

    def parse(self):
        stream = Stream(self.source)
        parser = _PARSERS[ROOT_PARSER_ID]
        return parser(stream)


class Stream:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self._index_cache = 0
        self._log = []

    def log(self, msg):
        self._log.append(msg)

    def save(self):
        self._index_cache = self.index
        return self.index

    def restore(self, _index):
        self.index = self._index_cache if _index is None else _index

    def read_pattern(self, pattern_string):
        match = re.match(pattern_string, self.text[self.index:])
        if not match:
            raise ParsingError
        string, index = match.group(0), match.span()
        return self._read(string, index)

    def read_string(self, string):
        text = self.text[self.index:]
        if not text.startswith(string):
            raise ParsingError
        index = self.index, self.index + len(string)
        return self._read(string, index)

    def _read(self, string, index):
        self.index += len(string)
        return string, index


# PARSER REGISTERS =======================================

def rule(id, parser):
    def rule_parser(stream):
        index = stream.save()
        try:
            return parser(stream)
        except ParsingError as error:
            stream.restore(index)
            raise error

    _PARSERS[id] = rule_parser
    return rule_parser


def skp(id, pattern_string):
    def skip_rule_parser(stream):
        try:
            text, index = stream.read_pattern(pattern_string)
            return PatternNode(text, index)
        except ParsingError:
            return EmptyNode()

    _SKIP_PARSERS[id] = skip_rule_parser
    return skip_rule_parser


def root(parser):
    return rule(ROOT_PARSER_ID, parser)


# PARSER GENERATORS =======================================

def zero_many(parser):
    def zero_many_parser(stream):
        node = RuleNode()
        while True:
            try:
                child = parser(stream)
                node.add(child)
            except ParsingError:
                break
        return node
    return zero_many_parser


def one_of(*parsers):
    def one_of_parser(stream):
        for parser in parsers:
            try:
                return parser(stream)
            except ParsingError:
                pass
        raise ParsingError
    return one_of_parser


def opt(parser):
    def opt_parser(stream):
        try:
            return parser(stream)
        except ParsingError:
            return EmptyNode()
    return opt_parser


def seq(*parsers):
    def seq_parser(stream):
        node = RuleNode()
        for parser in parsers:
            child = parser(stream)
            node.add(child)
        return node
    return seq_parser


def r(id):
    def rule_parser(stream):
        return _PARSERS[id](stream)
    return rule_parser


def p(string):
    def pattern_parser(stream):
        _parser_skip(stream)
        text, index = stream.read_pattern(string)
        return PatternNode(text, index)
    return pattern_parser


def s(string):
    def string_parser(stream):
        _parser_skip(stream)
        text, index = stream.read_string(string)
        return StringNode(text, index)
    return string_parser


def _parser_skip(stream):
    while True:
        count = [True for parser in _SKIP_PARSERS.values() if parser(stream)]
        if len(count) == 0:
            break


# GRAMMAR ===================================================

skp('space', r'[\s\n\r,]+')
skp('comment', r'--[^\n\r]*')

root(zero_many(r('expression')))

rule('expression', one_of(r('tag'), r('relation'), r('value')))
rule('tag', seq(s('#'), r('name')))
rule('relation', seq(r('path'), one_of(
    r('equal'), r('diff'), r('lte'), r('lt'),
    r('gte'), r('gt'), r('in'), r('out')
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
    r('name'), r('concept'), r('log'), r('alias'),
    r('cache'), r('format'), r('meta'), r('doc')
))
rule('log', seq(s('!'), r('name')))
rule('alias', seq(s('@'), r('name')))
rule('cache', seq(s('$'), r('name')))
rule('format', seq(s('%'), r('name')))
rule('meta', seq(s('_'), r('name')))
rule('doc', seq(s('?'), r('name')))
rule('value', one_of(r('reference'), r('literal'), r('list'), r('object')))
rule('reference', seq(
    one_of(r('query'), r('keyword')),
    zero_many(r('sub-reference'))
))
rule('sub-reference', seq(s('/'), one_of(
    r('range'), r('int'), r('tag'), r('list'), r('object'),
    r('query'), r('keyword'), r('wildcard')
)))
rule('literal', one_of(r('int'), r('float'), r('string')))
rule('list', seq(s('['), zero_many(r('value')), s(']')))
rule('range', one_of(
    seq(s('..'), r('int')),
    seq(r('int'), s('..'), opt(r('int')))
))
rule('object', seq(
    s('('), r('object-key'), zero_many(r('expression')), s(')')
))
rule('object-key', one_of(
    r('default-path'), r('default-format'), r('default-doc'), r('path')
))
rule('query', seq(s('{'), r('query-key'), zero_many(r('expression')), s('}')))
rule('query-key', one_of(r('anonym-path'), r('path')))
rule("default-format", s('%:'))
rule("default-doc", s('?:'))
rule("default-path", s(':'))
rule("wildcard", s('*'))
rule("string", p(r"'[^']*'|\"[^\"]*\""))
rule("float", p(r"-?\d*\.\d+([eE][-+]?\d+)?\b"))
rule("int", p(r"-?\d+\b"))
rule("name", p(r"[a-z]\w*"))
rule("concept", p(r"[A-Z]\w*"))
