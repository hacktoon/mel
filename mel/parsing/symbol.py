from ..exceptions import ParsingError
from .nodes import (
    RootNode,
    RuleNode,
    StringNode,
    PatternNode,
    ZeroManyNode,
    OneManyNode,
    OneOfNode,
    OptionalNode,
)


class Symbol:
    def __init__(self, *symbols):
        self.symbols = symbols

    def parse(self, _):
        raise NotImplementedError

    def list_parse(self, symbols, context):
        nodes = []
        index = context.stream.save()
        try:
            for symbol in symbols:
                nodes.append(symbol.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return nodes

    def skip_parse(self, context):
        skip_symbols = context.skip_symbols.values()

        def skipped():
            return len([s for s in skip_symbols if skip(context, s)])

        def skip(context, symbols):
            try:
                for symbol in symbols:
                    symbol.parse(context, skip=False)  # TODO: remove skip
            except ParsingError:
                return False
            return True

        while skipped():
            pass

    def __repr__(self):
        children = ', '.join([repr(s) for s in self.symbols])
        return f"{self.__class__.__name__}({children})"


class Root(Symbol):
    def parse(self, context):
        node = RootNode()
        children = self.list_parse(context.start_symbols, context)
        node.add(*children)
        self.skip_parse(context)
        context.stream.close()
        return node


class Rule(Symbol):
    def __init__(self, id):
        self.id = id

    def parse(self, context):
        symbols = context.symbols[self.id]
        node = RuleNode(self.id)
        index = context.stream.save()
        try:
            children = self.list_parse(symbols, context)
            node.add(*children)
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}("{self.id}")'


class ZeroMany(Symbol):
    def parse(self, context):
        node = ZeroManyNode()
        while True:
            try:
                children = self.list_parse(self.symbols, context)
                node.add(*children)
            except ParsingError:
                break
        return node


class OneMany(Symbol):
    def parse(self, context):
        node = OneManyNode()
        node.add(*self.list_parse(self.symbols, context))
        while True:
            try:
                children = self.list_parse(self.symbols, context)
                node.add(*children)
            except ParsingError:
                break
        return node


class Opt(Symbol):
    def parse(self, context):
        node = OptionalNode()
        try:
            children = self.list_parse(self.symbols, context)
            node.add(*children)
        except ParsingError:
            pass
        return node


class OneOf(Symbol):
    def parse(self, context):
        node = OneOfNode()
        for symbol in self.symbols:
            try:
                node.add(*symbol.parse(context))
                return node
            except ParsingError:
                pass
        raise ParsingError


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
