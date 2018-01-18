from . import utils
from .exceptions import UnknownReferenceError, FileError


class BaseNode:
    def __init__(self):
        self.text = ''
        self.text_range = (0, 0)

    def __repr__(self):
        first, last = self.text_range
        return self.text[first: last]


class Node(BaseNode):
    def __init__(self):
        self.values = []
        self.refs = {}

    def add(self, node, alias=None):
        self.values.append(node)
        if alias is not None:
            self.refs[alias] = node

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.refs[key]
        return self.values[key]

    def eval(self, context):
        values = [value.eval(context) for value in self.values]
        return values[0] if len(values) == 1 else values


class ExpressionNode(Node):
    def eval(self, context):
        evaluator = context.evaluators.get('expression', lambda e, c: e)

        id = self.id.value
        attrs = {key: attr.eval(context) for key, attr in self.attrs.items()}
        refs = {key: attr.eval(context) for key, attr in self.refs.items()}
        values = [value.eval(context) for value in self.values]

        return evaluator({
            'id': id,
            'attrs': attrs,
            'refs': refs,
            'values': values
        }, context)


class ListNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.items = []

    def add(self, item):
        self.items.append(item)

    def eval(self, context):
        return [item.eval(context) for item in self.items]


class QueryNode(BaseNode):
    def eval(self, context):
        return self.query.value


class FileNode(BaseNode):
    def eval(self, context):
        try:
            return utils.read_file(self.path.value)
        except IOError as error:
            raise FileError(self.path, error)


class EnvNode(BaseNode):
    def eval(self, context):
        return utils.read_environment(self.variable.value, '')


class ReferenceNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.names = []

    def add(self, name):
        self.names.append(name)

    def read(self, node, name):
        try:
            return node[name.value]
        except KeyError:
            raise UnknownReferenceError(name)

    def eval(self, context):
        def get_node(node, names):
            name = names[0]
            if len(names) == 1:
                return self.read(node, name)
            node = self.read(node, name)
            return get_node(node, names[1:])

        node = get_node(context.tree, self.names)
        return node.eval(context)


class ValueNode(BaseNode):
    def eval(self, context):
        return self.token.value


class IntNode(ValueNode):
    pass


class FloatNode(ValueNode):
    pass


class BooleanNode(ValueNode):
    pass


class StringNode(ValueNode):
        pass
