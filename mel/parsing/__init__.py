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


class SubParser:
    def __init__(self, id, parser):
        self.id = id
        self.parser = parser


# ZERO MANY PARSER GENERATOR ==========================================

class ZeroMany(SubParser):
    def __init__(self, *rules):
        self.rules = rules

    # HELPER FUNCTION
    def _parse_rules(self, stream, node):
        index = stream.save()
        try:
            for rule in self.rules:
                node.add(rule.parser(stream))
        except ParsingError as error:
            stream.restore(index)
            raise error
        return node

    def parser(self, stream):
        node = ZeroManyNode()
        while True:
            try:
                node = self._parse_rules(stream, node)
            except ParsingError:
                break
        return node


# SEQUENCE PARSER GENERATOR ==========================================

class Seq(SubParser):
    def __init__(self, *rules):
        self.rules = rules

    def parser(self, stream):
        node = SequenceNode()
        index = stream.save()
        try:
            for rule in self.rules:
                node.add(rule.parser(stream))
        except ParsingError as error:
            stream.restore(index)
            raise error
        return node


# ONE MANY PARSER GENERATOR ==========================================

class OneMany(SubParser):
    def __init__(self, *rules):
        self.rules = rules

    def parser(self, stream):
        node = OneManyNode()
        while True:
            try:
                for rule in self.rules:
                    node.add(rule.parser(stream))
            except ParsingError:
                break
        if len(node):  # TODO: remove this check
            return node
        raise ParsingError


# ONE OF PARSER GENERATOR ==========================================

class OneOf(SubParser):
    def __init__(self, *rules):
        self.rules = rules
        # TODO: use `rules` to build error messages

    def parser(self, stream):
        node = OneOfNode()
        for rule in self.rules:
            try:
                node.add(rule.parser(stream))
                return node
            except ParsingError:
                pass
        raise ParsingError


# OPTIONAL PARSER GENERATOR ==========================================

class Opt(SubParser):
    def __init__(self, rule):
        self.rule = rule

    def parser(stream):
        node = OptionalNode()
        try:
            node.add(self.rule.parser(stream))
        except ParsingError:
            pass
        return node


# BASE PARSER GENERATOR ==========================================

class ParserGenerator:
    def __init__(self):
        self.subparsers = {}
        self.skip_subparsers = {}

    def match(self, stream):
        rule = next(iter(self.subparsers.values()))
        tree = RootNode()
        tree.add(rule.parser(stream))
        self._skip_subparsers(stream)
        if not stream.eof:
            raise ParsingError
        return tree

    def rule(self, id, rule):
        self.subparsers[id] = rule

    def skip(self, id, string):
        def skip_rule_parser(stream):
            try:
                stream.read_pattern(string)
            except ParsingError:
                return

        self.skip_subparsers[id] = SubParser(id, skip_rule_parser)

    def r(self, id):
        def rule_parser(stream):
            rule = self.subparsers[id]
            node = RuleNode(id)
            index = stream.save()
            try:
                node.add(rule.parser(stream))
            except ParsingError as error:
                stream.restore(index)
                raise error
            return node
        return SubParser(id, rule_parser)

    def p(self, string):
        def pattern_parser(stream):
            self._skip_subparsers(stream)
            text, index = stream.read_pattern(string)
            return PatternNode(text, index)
        return SubParser(string, pattern_parser)

    def s(self, string):
        def string_parser(stream):
            self._skip_subparsers(stream)
            text, index = stream.read_string(string)
            return StringNode(text, index)
        return SubParser(string, string_parser)

    def _skip_subparsers(self, stream):
        rules = self.skip_subparsers.values()
        while True:
            skipped = [True for rule in rules if rule.parser(stream)]
            if len(skipped) == 0:
                break
