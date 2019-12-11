import re

from .nodes import (
    RuleNode,
    StringNode,
    PatternNode,
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


class Grammar:
    def __init__(self, name=''):
        self._root_parser = lambda stream: EmptyNode()
        self._rule_parsers = {}
        self._skip_parsers = {}
        self.name = name

    def match(self, stream):
        return self._root_parser(stream)

    def root(self, parser):
        self._root_parser = parser

    def rule(self, id, parser):
        def rule_parser(stream):
            index = stream.save()
            try:
                return parser(stream)
            except ParsingError as error:
                stream.restore(index)
                raise error

        self._rule_parsers[id] = rule_parser
        return rule_parser

    def skip(self, id, pattern_string):
        def skip_rule_parser(stream):
            try:
                text, index = stream.read_pattern(pattern_string)
                return PatternNode(text, index)
            except ParsingError:
                return EmptyNode()

        self._skip_parsers[id] = skip_rule_parser
        return skip_rule_parser

    def zero_many(self, parser):
        def zero_many_parser(stream):
            node = RuleNode()
            while True:
                try:
                    node.add(parser(stream))
                except ParsingError:
                    break
            return node
        return zero_many_parser

    def one_many(self, parser):
        def one_many_parser(stream):
            node = RuleNode()
            node.add(parser(stream))
            while True:
                try:
                    node.add(parser(stream))
                except ParsingError:
                    break
            return node
        return one_many_parser

    def one_of(self, *parsers):
        def one_of_parser(stream):
            for parser in parsers:
                try:
                    return parser(stream)
                except ParsingError:
                    pass
            raise ParsingError
        one_of_parser.name = 'one of'
        return one_of_parser

    def opt(self, parser):
        def opt_parser(stream):
            try:
                return parser(stream)
            except ParsingError:
                return EmptyNode()
        return opt_parser

    def seq(self, *parsers):
        def seq_parser(stream):
            node = RuleNode()
            for parser in parsers:
                node.add(parser(stream))
            return node
        return seq_parser

    def r(self, id):
        def rule_parser(stream):
            node = self._rule_parsers[id](stream)
            node.id = id
            return node
        return rule_parser

    def p(self, string):
        def pattern_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_pattern(string)
            return PatternNode(text, index)
        return pattern_parser

    def s(self, string):
        def string_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_string(string)
            return StringNode(text, index)
        return string_parser

    def _parse_skip_rules(self, stream):
        parsers = self._skip_parsers.values()
        while True:
            skipped = [True for parser in parsers if parser(stream)]
            if len(skipped) == 0:
                break
