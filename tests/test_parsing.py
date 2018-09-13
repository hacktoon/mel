import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context

from dale.exceptions import (
    UnexpectedTokenError
)


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context=Context()):
    tree = create_tree(text)
    context.tree = tree
    return tree.eval(context)


def test_list_parsing():
    output = eval('(a 5) [1, 2.3, True, a "str" ]')
    assert True
