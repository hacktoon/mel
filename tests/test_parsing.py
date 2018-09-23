import pytest

from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context

from dale.exceptions import (
    UnexpectedTokenError
)


def create_tree(text):
    return Parser().parse(text)


def eval(text, context_class=Context):
    context = context_class()
    context.tree = create_tree(text)
    return tree.eval(context)


def test_list_parsing():
    context = Context()
    context.tree = create_tree('(a 5) [1, 2.3, True, a "str" ]')
    tree.eval(context)
    assert True
