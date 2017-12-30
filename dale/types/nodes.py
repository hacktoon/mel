from .tokens import Token
from .errors import ParsingError


class Node:
    def __init__(self):
        self._children = []

    def add(self, child):
        self._children.append(child)

    def __getitem__(self, index):
        return self._children[index]

    @property
    def value(self):
        if len(self._children) == 1:
            return self._children[0].value
        return [child.value for child in self._children]

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        if len(self._children) == 1:
            return str(self._children[0].value)
        return [str(child.value) for child in self._children]


class ExpressionNode(Node):
    def __init__(self):
        super().__init__()
        self.keyword = Token()
        self.parameters = Token()

    @property
    def value(self):
        if len(self) == 1:
            values = self._children[0].value
        else:
            values = [child.value for child in self._children]
        return {
            'keyword': self.keyword.value,
            'parameters': self.parameters.value,
            'values': values
        }


class ParametersNode(Node):
    def __init__(self):
        super().__init__()
        self._parameters = {}

    def __setitem__(self, key, value):
        self._parameters[key] = value

    def __getitem__(self, key):
        return self._parameters[key]

    @property
    def value(self):
        return {k: v.value for k, v in self._parameters.items()}


class QueryNode(Node):
    def __init__(self):
        super().__init__()
        self.source = Token()
        self.query = Token()

    @property
    def value(self):
        if self.source.value == 'file':
            try:
                with open(self.query.value, 'r') as file_obj:
                    return file_obj.read()
            except IOError as e:
                raise ParsingError("I/O error: {}".format(e))
            except Exception:
                raise ParsingError("Unexpected error")
        else:
            return self.query.value


class ReferenceNode(Node):
    pass


class ListNode(Node):
    pass


class IntNode(Node):
    pass


class FloatNode(Node):
    pass


class BooleanNode(Node):
    pass


class StringNode(Node):
    pass
