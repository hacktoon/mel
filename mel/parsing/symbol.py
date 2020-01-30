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


class Symbol:
    def parse(self, _):
        raise NotImplementedError

    def skip_parse(self, context):
        symbols = context.skip_symbols.values()

        def finished_skipping():
            total = 0
            for sym in symbols:
                if sym.parse(context):
                    total += 1
            return total == 0

        while True:
            if finished_skipping():
                break

    def __repr__(self):
        return self.__class__.__name__


class ZeroMany(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = ZeroManyNode()
        while True:
            try:
                node.add(self.symbol.parse(context))
            except ParsingError:
                break
        return node


class Seq(Symbol):
    def __init__(self, *symbols):
        self.symbols = symbols

    def parse(self, context):
        node = SequenceNode()
        index = context.stream.save()
        try:
            for symbol in self.symbols:
                node.add(symbol.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node


class OneMany(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = OneManyNode()
        node.add(self.symbol.parse(context))
        while True:
            try:
                node.add(self.symbol.parse(context))
            except ParsingError:
                break
        return node


class OneOf(Symbol):
    def __init__(self, *symbols):
        self.symbols = symbols

    def parse(self, context):
        node = OneOfNode()
        for symbol in self.symbols:
            try:
                node.add(symbol.parse(context))
                return node
            except ParsingError:
                pass
        raise ParsingError


class Opt(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = OptionalNode()
        try:
            node.add(self.symbol.parse(context))
        except ParsingError:
            pass
        return node


class Rule(Symbol):
    def __init__(self, id):
        self.id = id

    def parse(self, context):
        symbol = context.symbols[self.id]
        node = RuleNode(self.id)
        index = context.stream.save()
        try:
            node.add(symbol.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}("{self.id}")'


class Str(Symbol):
    def __init__(self, string):
        self.string = string

    def parse(self, context, skip=True):
        if skip:
            self.skip_parse(context)
        text, index = context.stream.read_string(self.string)
        return StringNode(text, index)

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}("{self.string}")'


class Regex(Str):
    def parse(self, context, skip=True):
        if skip:
            self.skip_parse(context)
        text, index = context.stream.read_pattern(self.string)
        return PatternNode(text, index)


class Skip(Str):
    def parse(self, context):
        try:
            context.stream.read_pattern(self.string)
        except ParsingError:
            return


class Root(Symbol):
    def parse(self, context):
        symbols = iter(context.symbols.values())
        symbol = next(symbols)
        node = RootNode()
        node.add(symbol.parse(context))
        self.skip_parse(context)
        context.stream.close()
        return node
