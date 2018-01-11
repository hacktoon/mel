from . import utils
from .exceptions import FileError


class Node:
    current = None

    def __init__(self, subnodes=None):
        self.subnodes = subnodes or []
        self.references = {}

    def add(self, node):
        self.subnodes.append(node)
        if isinstance(node, ExpressionNode):
            self.references[node.name.value] = node

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.references[key]
        return self.subnodes[key]

    def eval(self, context):
        subnodes = [subnode.eval(context) for subnode in self.subnodes]
        return subnodes[0] if len(subnodes) == 1 else subnodes


class ExpressionNode(Node):
    def __init__(self, name, attributes):
        super().__init__()
        self.name = name
        self.attributes = attributes

    def eval(self, context):
        return super().eval(context)


class QueryNode(Node):
    def __init__(self, source, query):
        super().__init__()
        self.source = source
        self.query = query

    def eval(self, context):
        return self.query.value


class FileNode(Node):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def eval(self, context):
        try:
            return utils.read_file(self.path.value)
        except IOError as error:
            raise FileError(self.path, error)


class EnvNode(Node):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def eval(self, context):
        return utils.read_environment(self.variable.value, '')


class ReferenceNode(Node):
    def __init__(self):
        self.names = []

    def add(self, name):
        self.names.append(name)

    def eval(self, context):
        tree = context.var('tree')

        def get_node(node, names):
            name = names[0].value
            if len(names) == 1:
                return node[name]
            return get_node(node[name], names[1:])

        node = get_node(tree, self.names)
        return node.eval(context)


class ValueNode(Node):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def eval(self, context):
        return self.token.value


class ListNode(Node):
    def eval(self, context):
        return [subnode.eval(context) for subnode in self.subnodes]


class IntNode(ValueNode):
    pass


class FloatNode(ValueNode):
    pass


class BooleanNode(ValueNode):
    pass


class StringNode(ValueNode):
        pass
