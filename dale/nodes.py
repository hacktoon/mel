import os

from .tokens import Token
from .exceptions import FileError


class Node():
    def __init__(self):
        self._subnodes = []
        self._named_subnodes = {}

    def add(self, node):
        self._subnodes.append(node)
        if hasattr(node, 'name'):
            self._named_subnodes[node.name.eval()] = node

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._named_subnodes[key]
        return self._subnodes[key]

    def eval(self, context):
        values = [subnode.eval(context) for subnode in self._subnodes]
        return values[0] if len(values) == 1 else values


class ExpressionNode(Node):
    def __init__(self):
        super().__init__()
        self.name = Token()
        self.attributes = {}

    def eval(self, context):
        return super().eval(context)


class QueryNode(Node):
    def __init__(self):
        super().__init__()
        self.source = Token()
        self.query = Token()

    def eval(self, context):
        return self.query.eval()


class FileNode(Node):
    def __init__(self):
        super().__init__()
        self.path = Token()

    def eval(self, context):
        try:
            with open(self.path.eval(), 'r') as file_obj:
                return file_obj.read()
        except IOError as error:
            raise FileError(self.path, error)


class EnvNode(Node):
    def __init__(self):
        super().__init__()
        self.variable = Token()

    def eval(self, context):
        return os.environ.get(self.variable.eval(), '')


class ReferenceNode(Node):
    def __init__(self):
        super().__init__()
        self.names = []

    def add(self, token):
        self.names.append(token.eval())

    def eval(self, context):
        tree = context.var('tree')

        def get(node, names):
            if len(names) == 1:
                return node[names[0]]
            else:
                return get(node[names[0]], names[1:])

        reference_node = get(tree, self.names)
        return reference_node.eval(context)


class ValueNode(Node):
    def __init__(self):
        super().__init__()
        self.value = Token()

    def eval(self, context):
        return self.value.eval()


class ListNode(Node):
    pass


class IntNode(ValueNode):
    pass


class FloatNode(ValueNode):
    pass


class BooleanNode(ValueNode):
    pass


class StringNode(ValueNode):
        pass
