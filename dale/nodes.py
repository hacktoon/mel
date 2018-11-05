def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.text = ""
        self.index = (0, 0)
        self._chain = []
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def chain(self, node):
        self._chain.append(node)

    def property_id(self):
        return

    def property_name(self):
        return

    def eval(self, context):
        pass

    def __getitem__(self, index):
        return self.nodes[index]

    def __len__(self):
        return len(self.nodes)

    def __bool__(self):
        return True

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        return "{}('{}')".format(self.id.upper(), self)


class RootNode(Node):
    id = "root"


class ScopeNode(Node):
    id = "scope"

    def __init__(self):
        super().__init__()
        self.key = None
        self.properties = {P.id: dict() for P in PropertyNode.__subclasses__()}

    def add(self, node):
        property_id = node.property_id()
        if property_id in self.properties.keys():
            self.properties[property_id][node.property_name()] = node
        else:
            super().add(node)

    def property_id(self):
        return self.key.id if self.key else None

    def property_name(self):
        return self.key.name if self.key else None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)


class QueryNode(Node):
    id = "query"

    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)


class ListNode(Node):
    id = "list"

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(values, context)


class PropertyNode(Node):
    id = "property"

    def __init__(self):
        super().__init__()
        self.name = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        return evaluator(self.name, context)


class FlagNode(PropertyNode):
    id = "flag"
    prefix = "!"

    def property_id(self):
        return self.id

    def property_name(self):
        return self.name


class UIDNode(PropertyNode):
    id = "uid"
    prefix = "#"


class AttributeNode(PropertyNode):
    id = "attribute"
    prefix = "@"


class FormatNode(PropertyNode):
    id = "format"
    prefix = "%"


class VariableNode(PropertyNode):
    id = "variable"
    prefix = "$"


class DocNode(PropertyNode):
    id = "doc"
    prefix = "?"


class LiteralNode(Node):
    def __init__(self):
        super().__init__()
        self.value = None  # TODO: use Token

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        return evaluator(self.value, context)


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"
