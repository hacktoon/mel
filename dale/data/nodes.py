

class Node:
    def __init__(self, token=None):
        self.token = token
        self.children = []
        self.value = token.value if token else ''

    def add(self, value):
        self.children.append(value)

    def eval(self, context):
        return ''

    def __eq__(self, node_repr):
        return str(self) == node_repr

    def __ne__(self, node_repr):
        return str(self) != node_repr

    def __repr__(self):
        return str(self)

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}<{}>'.format(class_name.upper(), self.value)


class Content(Node):
    def eval(self, context):
        pass

    def __str__(self):
        return ' '.join([str(x) for x in self.children])


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


class Alias(Node):
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value.split('.')

    def __str__(self):
        class_name = self.__class__.__name__
        value = '.'.join(self.value)
        return '{}<{}>'.format(class_name.upper(), value)


class Expression(Node):
    def __init__(self, token):
        super().__init__(token)
        self.keyword = ''
        self.parameters = ParameterList()
        self.children = Content()

    def add(self, value):
        self.children.add(value)

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}<{} {} {}>'.format(
            class_name.upper(),
            str(self.keyword),
            str(self.parameters),
            str(self.children)
        )


class Keyword(Node):
    def eval(self, context):
        pass


class ParameterList(Node):
    def __str__(self):
        class_name = self.__class__.__name__
        value = ', '.join([str(x) for x in self.children])
        return '{}<{}>'.format(class_name.upper(), value)


class Parameter(Node):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        class_name = self.__class__.__name__
        return '{}:{}'.format(
            self.key.value,
            self.value
        )


class List(Node):
    def __str__(self):
        class_name = self.__class__.__name__
        value = ', '.join([str(x) for x in self.children])
        return '{}<{}>'.format(class_name.upper(), value)
