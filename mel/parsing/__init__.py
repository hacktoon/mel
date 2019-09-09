from ..exceptions import UnexpectedTokenError

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
        node = self.read(ROOT)
        if self.stream.is_eof():
            return node
        self.error(UnexpectedTokenError)
