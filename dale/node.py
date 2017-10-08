

class Node:
    def __init__(self, token=None):
        self.token = token
        self.children = []
        self.value = token.value if token else ''

    def add(self, value):
        self.children.append(value)

    def eval(self):
        return self.value

    def __eq__(self, node_repr):
        return str(self) == node_repr

    def __ne__(self, node_repr):
        return str(self) != node_repr

    def __repr__(self):
        return str(self)

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}({})'.format(class_name.upper(), self.value)


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


class Identifier(Node):
    def __init__(self, token):
        super().__init__(token)
        self.value = ''

    def eval(self, context):
        pass

    def __str__(self):
        class_name = self.__class__.__name__
        value = '.'.join(self.children)
        return '{}({})'.format(class_name.upper(), value)


class List(Node):
    def eval(self, context):
        pass

    def __str__(self):
        class_name = self.__class__.__name__
        value = ', '.join([str(x) for x in self.children])
        return '{}({})'.format(class_name.upper(), '[{}]'.format(value))


class ParameterList(Node):
    def eval(self, context):
        pass

    def __str__(self):
        class_name = self.__class__.__name__
        value = ', '.join([str(x) for x in self.children])
        return '{}({})'.format(class_name.upper(), value)


class Parameter(Node):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def eval(self, context):
        pass

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}({}:{})'.format(
            class_name.upper(),
            str(self.identifier),
            self.value
        )


class Content(Node):
    def eval(self, context):
        pass

    def __str__(self):
        return ' '.join([str(x) for x in self.children])


class Expression(Node):
    def __init__(self, token):
        super().__init__(token)
        self.identifier = ''
        self.parameter_list = ParameterList()
        self.children = Content()

    def add(self, value):
        self.children.add(value)

    def eval(self, context):
        pass

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}({} {} {})'.format(
            class_name.upper(),
            str(self.identifier),
            str(self.parameter_list),
            str(self.children)
        )
