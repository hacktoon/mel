import os
import errno

from .tokens import Token
from .exceptions import FileError


class Node:
    def __init__(self):
        self.values = []

    def add(self, token):
        self.values.append(token)

    def eval(self, context=None):
        return [value.eval(context) for value in self.values]

    def __repr__(self):
        return str(self.eval())


class ExpressionNode(Node):
    def __init__(self):
        super().__init__()
        self.keyword = Token()
        self.parameters = {}

    def eval(self, context=None):
        return {
            'keyword': self.keyword.eval(),
            'parameters': {k: v.eval() for k, v in self.parameters.items()},
            'values': super().eval()
        }


class QueryNode(Node):
    def __init__(self):
        self.source = Token()
        self.query = Token()

    def eval(self, context=None):
        return self.query.eval(context)


class FileNode(Node):
    def __init__(self):
        self.path = Token()

    def eval(self, context=None):
        try:
            with open(self.path.eval(), 'r') as file_obj:
                return file_obj.read()
        except IOError as error:
            raise FileError(self.path, error)


class EnvNode(Node):
    def __init__(self):
        self.variable = Token()

    def eval(self, context=None):
        return os.environ.get(self.variable.eval(), '')


class ReferenceNode(Node):
    pass


class ValueNode:
    def __init__(self):
        self.value = Token()

    def eval(self, context=None):
        return self.value.eval()


class IntNode(ValueNode):
    pass


class FloatNode(ValueNode):
    pass


class BooleanNode(ValueNode):
    pass


class StringNode(ValueNode):
        pass
