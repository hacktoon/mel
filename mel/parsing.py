import re

from .nodes import (
    RuleNode,
    SymbolNode,
    EmptyNode
)
from .exceptions import ParsingError


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, text):
        stream = Stream(text)
        return self.grammar.match(stream)


class Stream:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self._index_cache = 0

    def save(self):
        self._index_cache = self.index
        return self.index

    def restore(self, _index):
        self.index = self._index_cache if _index is None else _index

    def read_pattern(self, pattern_string):
        match = re.match(pattern_string, self.text[self.index:])
        if not match:
            raise ParsingError
        index = [offset + self.index for offset in match.span()]
        return self._read(match.group(0), index)

    def read_string(self, string):
        text = self.text[self.index:]
        if not text.startswith(string):
            raise ParsingError
        index = self.index, self.index + len(string)
        return self._read(string, index)

    def _read(self, string, index):
        self.index += len(string)
        return string, index

    @property
    def eof(self):
        return self.index >= len(self.text)


class Grammar:
    def __init__(self, text=''):
        self._root_parser = None
        self._rule_parsers = {}
        self._skip_parsers = {}
        self.text = text

    def match(self, stream):
        rule_parsers = iter(self._rule_parsers.values())
        root_parser = self._root_parser or next(rule_parsers)
        tree = root_parser(stream)
        self._parse_skip_rules(stream)
        if not stream.eof:
            raise ParsingError
        return tree

    def root(self, parser):
        self._root_parser = parser

    def rule(self, id, parser):
        # interceptor to save/restore
        # TODO: maybe use node cache too?
        def rule_parser(stream):
            index = stream.save()
            try:
                return parser(stream)
            except ParsingError as error:
                stream.restore(index)
                raise error

        self._rule_parsers[id] = rule_parser
        return self.parse_wrap(rule_parser)

    def skip(self, id, string):
        def skip_rule_parser(stream):
            try:
                text, index = stream.read_pattern(string)
                return [text]
            except ParsingError:
                return []

        self._skip_parsers[id] = skip_rule_parser
        return self.parse_wrap(skip_rule_parser)

    def zero_many(self, parser):
        def zero_many_parser(stream):
            node = RuleNode('0..n')
            while True:
                try:
                    node.add(parser(stream))
                except ParsingError:
                    break
            return node
        return self.parse_wrap(zero_many_parser)

    def one_many(self, parser):
        def one_many_parser(stream):
            node = RuleNode('1..n')
            node.add(parser(stream))
            while True:
                try:
                    node.append(parser(stream))
                except ParsingError:
                    break
            return node
        return self.parse_wrap(one_many_parser)

    def one_of(self, *parsers):
        def one_of_parser(stream):
            for parser in parsers:
                try:
                    return parser(stream)
                except ParsingError:
                    pass
            raise ParsingError
        return self.parse_wrap(one_of_parser)

    def opt(self, parser):
        def opt_parser(stream):
            try:
                return parser(stream)
            except ParsingError:
                return EmptyNode()
        return self.parse_wrap(opt_parser)

    def seq(self, *parsers):
        def seq_parser(stream):
            node = RuleNode('seq')
            for parser in parsers:
                node.add(parser(stream))
            return node
        return self.parse_wrap(seq_parser)

    def r(self, id):
        def rule_parser(stream):
            return self._rule_parsers[id](stream)
        return self.parse_wrap(rule_parser)

    def p(self, string):
        def pattern_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_pattern(string)
            return SymbolNode(text, index)
        return self.parse_wrap(pattern_parser)

    def s(self, string):
        def string_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_string(string)
            return SymbolNode(text, index)
        return self.parse_wrap(string_parser)

    @property
    def NEWLINE(self):
        def newline_parser(stream):
            self._parse_skip_rules(stream)
            stream.read_pattern(r'[\r\n]*')
            return EmptyNode()
        return newline_parser

    def _parse_skip_rules(self, stream):
        parsers = self._skip_parsers.values()
        while True:
            skipped = [True for parser in parsers if parser(stream)]
            if len(skipped) == 0:
                break

    def parse_wrap(self, parser):
        return parser

    def __str__(self):
        return self.text


def builtin_string_parser(stream):
    pattern = r'"[^"]*"' + r"|'[^']*'"
    text, index = stream.read_pattern(pattern)
    return StringNode(text, index)


# FLOAT = -?\d*\.\d+([eE][-+]?\d+)?
# D-STRING = "[^\"]*"
# S-STRING = '[^\']*'
