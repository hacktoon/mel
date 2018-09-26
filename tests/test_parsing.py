from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.utils.context import Context


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context_class=Context):
    context = context_class()
    context.tree = tree = create_tree(text)
    return tree.eval(context)


def test_basic_parsing():
    context = Context()
    context.tree = tree = create_tree('(a 5)')
    tree.eval(context)
    assert True
