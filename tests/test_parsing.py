from dale.lexing import TokenStream
from dale.parsing import Parser
from dale import nodes
from dale.utils.context import Context


def create_tree(text):
    stream = TokenStream(text)
    return Parser(stream).parse()


def eval(text, context_class=Context):
    context = context_class()
    context.tree = tree = create_tree(text)
    return tree.eval(context)


def test_node_type():
    tree = create_tree('(foo bar)')
    assert isinstance(tree, nodes.Node)


def test_string_representation():
    tree = create_tree('(a 5)')
    assert str(tree) == '(a 5)'
