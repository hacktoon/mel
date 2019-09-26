from ..exceptions import ParsingError, UnexpectedTokenError

from .constants import ROOT
from .base import BaseParser

from . import ( # noqa
    expression,
    keyword,
    literal,
    path,
    reference,
    relation,
    struct,
    value,
)


class Parser(BaseParser):
    def parse(self):
        try:
            node = self.read(ROOT)
        except ParsingError:
            self.error(UnexpectedTokenError)
        if self.stream.is_eof():
            return node
        self.error(UnexpectedTokenError)
