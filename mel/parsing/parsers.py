from ..lexing.stream import Char
from .nodes import Node


class BaseParser:
    id = ''
    hint = ''

    def parse(self, stream):
        chars = self._read(stream)
        return Node(self.id, chars)

    def _read(self, stream):
        raise NotImplementedError()


# ======================================
class IntParser(BaseParser):
    id = 'integer'
    hint = Char.DIGIT

    def _read(self, stream):
        return stream.one_many_types(Char.DIGIT)


# ======================================
def StringParser(BaseParser):
    id = 'string'  # noqa
    hint = '"'  # noqa

    def _read(self, stream):
        return stream.one_str('"')


# ======================================
def Seq(text):
    def string_parser(stream):
        return stream.one_types(text)
    return string_parser


# ======================================
def zeromany(parser):
    def parse(self, context):
        nodes = []
        # while True:
        #     nodes.append(parser)
        return nodes


# class Start(Symbol):
#     def parse(self, context):
#         node = RootNode()
#         symbols = context.start_rule.symbols
#         children = self.list_parse(symbols, context)
#         node.add(*children)
#         self.skip_parse(context)
#         context.stream.close()
#         return node


# class Sym(Symbol):
#     def __init__(self, id):
#         self.id = id

#     def parse(self, context):
#         symbols = context.rules[self.id].symbols
#         node = RuleNode(self.id)
#         index = context.stream.save()
#         try:
#             children = self.list_parse(symbols, context)
#             node.add(*children)
#         except ParsingError as error:
#             context.stream.restore(index)
#             raise error
#         return node

#     def __repr__(self):
#         classname = self.__class__.__name__
#         return f'{classname}("{self.id}")'


# class OneMany(Symbol):
#     def parse(self, context):
#         node = OneManyNode()
#         node.add(*self.list_parse(self.symbols, context))
#         while True:
#             try:
#                 children = self.list_parse(self.symbols, context)
#                 node.add(*children)
#             except ParsingError:
#                 break
#         return node


# class Opt(Symbol):
#     def parse(self, context):
#         node = OptionalNode()
#         try:
#             children = self.list_parse(self.symbols, context)
#             node.add(*children)
#         except ParsingError:
#             pass
#         return node


# class OneOf(Symbol):
#     def parse(self, context):
#         node = OneOfNode()
#         for symbol in self.symbols:
#             try:
#                 node.add(*symbol.parse(context))
#                 return node
#             except ParsingError:
#                 pass
#         raise ParsingError


# class Str(Symbol):
#     def __init__(self, string):
#         self.string = string

#     def parse(self, context, skip=True):
#         if skip:
#             self.skip_parse(context)
#         text, index = context.stream.read_string(self.string)
#         return StringNode(text, index)

#     def __repr__(self):
#         classname = self.__class__.__name__
#         return f'{classname}("{self.string}")'


# class Regex(Str):
#     def parse(self, context, skip=True):
#         if skip:
#             self.skip_parse(context)
#         text, index = context.stream.read_pattern(self.string)
#         return PatternNode(text, index)
