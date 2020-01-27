import re

from ..exceptions import ParsingError
from .nodes import (
    RootNode,
    RuleNode,
    StringNode,
    PatternNode,
    ZeroManyNode,
    OneManyNode,
    OneOfNode,
    SequenceNode,
    OptionalNode,
)


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
        start, end = [offset + self.index for offset in match.span()]
        return self._read(match.group(0), (start, end))

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


class ParserObj:
    def __init__(self, id, parser):
        self.id = id
        self.parser = parser


class Grammar:
    def __init__(self, start=None):
        self.rules = {}
        self.start_rule = start
        self.skip_rules = {}

    def match(self, stream):
        rule = self.start_rule or next(iter(self.rules.values()))
        tree = RootNode()
        tree.add(rule.parser(stream))
        self._parse_skip_rules(stream)
        if not stream.eof:
            raise ParsingError
        return tree

    def rule(self, id, rule):
        self.rules[id] = rule

    def skip(self, id, string):
        def skip_rule_parser(stream):
            try:
                stream.read_pattern(string)
            except ParsingError:
                return

        self.skip_rules[id] = ParserObj(id, skip_rule_parser)

    def zero_many(self, *rules):
        def zero_many_parser(stream):
            node = ZeroManyNode()
            while True:
                try:
                    for rule in rules:
                        node.add(rule.parser(stream))
                except ParsingError:
                    break
            return node
        return ParserObj('id', zero_many_parser)

    def one_many(self, *rules):
        def one_many_parser(stream):
            node = OneManyNode()
            while True:
                try:
                    for rule in rules:
                        node.add(rule.parser(stream))
                except ParsingError:
                    break
            if len(node):
                return node
            raise ParsingError
        return ParserObj('id', one_many_parser)

    def seq(self, *rules):
        def seq_parser(stream):
            node = SequenceNode()
            for rule in rules:
                node.add(rule.parser(stream))
            return node
        return ParserObj('Sequence', seq_parser)

    def one_of(self, *rules):  # TODO: use rules to build error messages
        def one_of_parser(stream):
            node = OneOfNode()
            for rule in rules:
                try:
                    node.add(rule.parser(stream))
                    return node
                except ParsingError:
                    pass
            raise ParsingError
        return ParserObj('One of', one_of_parser)

    def opt(self, rule):
        def opt_parser(stream):
            node = OptionalNode()
            try:
                node.add(rule.parser(stream))
            except ParsingError:
                pass
            return node
        return ParserObj('Optional', opt_parser)

    def r(self, id):
        def rule_parser(stream):
            rule = self.rules[id]
            node = RuleNode(id)
            index = stream.save()
            try:
                node.add(rule.parser(stream))
            except ParsingError as error:
                stream.restore(index)
                raise error
            return node
        return ParserObj(id, rule_parser)

    def p(self, string):
        def pattern_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_pattern(string)
            return PatternNode(text, index)
        return ParserObj(string, pattern_parser)

    def s(self, string):
        def string_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_string(string)
            return StringNode(text, index)
        return ParserObj(string, string_parser)

    def _parse_skip_rules(self, stream):
        rules = self.skip_rules.values()
        while True:
            skipped = [True for rule in rules if rule.parser(stream)]
            if len(skipped) == 0:
                break

    @property
    def NEWLINE(self):
        return self.p(r'[\r\n]+')

    @property
    def INT(self):
        return self.p(r'[0-9]+')

    @property
    def FLOAT(self):
        return self.p(r'-?\d*\.\d+([eE][-+]?\d+)?')

    @property
    def STRING(self):
        return self.p(r'"[^\"]*"|\'[^\']*\'')
