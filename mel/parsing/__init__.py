from .constants import ROOT
from .base import BaseParser

from . import ( # noqa
    root,
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
        return self.read_rule(ROOT)
