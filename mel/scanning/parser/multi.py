from ..stream import CharStream
from ..produce import Produce
from .base import Parser


########################################################################
# MULTI RULE PARSER
########################################################################
class MultiRuleParser(Parser):
    def __init__(self, *parsers: list[Parser]):
        self._parsers = parsers

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        raise NotImplementedError


class SeqParser(MultiRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = Produce(index=index)
        current_index = index
        for parser in self._parsers:
            if subproduce := parser.parse(stream, current_index):
                produce += subproduce
                current_index += len(subproduce)
            else:
                return Produce(index=index)
        return produce


class OneOfParser(MultiRuleParser):
    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        produce = Produce(index=index)
        for parser in self._parsers:
            if subproduce := parser.parse(stream, index):
                return produce + subproduce
        return produce
