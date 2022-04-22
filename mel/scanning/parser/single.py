from ..stream import CharStream
from ..produce import Produce, ValidProduce
from .base import Parser


########################################################################
# SINGLE RULE PARSER
########################################################################
class SingleRuleParser(Parser):
    def __init__(self, parser: Parser):
        self._parser = parser

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        raise NotImplementedError


########################################################################
# SUB SINGLE RULE PARSER
########################################################################
class OptionalParser(SingleRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = ValidProduce(index=index)
        if subproduce := self._parser.parse(stream, index):
            return subproduce
        return produce


class ZeroManyParser(SingleRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = ValidProduce(index=index)
        current_index = index
        while subproduce := self._parser.parse(stream, current_index):
            current_index += len(subproduce)
            produce += subproduce
        return produce


class OneManyParser(SingleRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        parser = self._parser
        produce = parser.parse(stream, index)
        current_index = index + len(produce)
        while subproduce := parser.parse(stream, current_index):
            current_index += len(subproduce)
            produce += subproduce
        return produce
