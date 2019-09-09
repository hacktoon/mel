from .constants import EXPRESSION, TAG, RELATION, VALUE
from .base import BaseParser, subparser


@subparser
class ExpressionParser(BaseParser):
    id = EXPRESSION

    def parse(self):
        return self.read_any([TAG, RELATION, VALUE])
