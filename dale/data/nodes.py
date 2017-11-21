

class Node:
    def __init__(self):
        self._children = []
        self._properties = {}

    def add(self, *args):
        if len(args) == 2:
            name, child = args
            self._add(name, child)
        elif len(args) == 1:
            self._add(None, args[0])
        else:
            raise TypeError('invalid number of arguments')

    def _add(self, name, child):
        if name:
            if name in self.__dict__:
                raise ValueError(name + ' attribute is already defined')
            self._properties[name] = child
            self.__dict__[name] = child
        else:
            self._children.append(child)

    def value(self):
        if len(self._children) == 1:
            return self._children[0].value()
        return [child.value() for child in self._children]

    def __getitem__(self, key):
        try:
            if key in self._properties:
                return self._properties[key]
            else:
                return self._children[key]
        except (KeyError, IndexError):
            raise ValueError(key + ' is not a valid key or index')

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        return str(self._children)

    def __str__(self):
        return repr(self)


class Expression(Node):
    def value(self):
        exp = {'keyword': self.keyword.value()}

        if self.parameters.value().items():
            exp['parameters'] = self.parameters.value()
        if len(self._children) > 1:
            exp['values'] = [child.value() for child in self._children]
        elif len(self._children) == 1:
            exp['values'] = self._children[0].value()
        return exp


class Keyword(Node):
    pass


class Parameters(Node):
    def value(self):
        return {key:child.value() for key, child in self._properties.items()}


class String(Node):
    pass


class Int(Node):
    pass


class Float(Node):
    pass


class Boolean(Node):
    pass


class Query(Node):
    pass


class Reference(Node):
    pass


class List(Node):
    def value(self):
        if len(self._children) == 1:
            return self._children[0].value()
        return [child.value() for child in self._children]