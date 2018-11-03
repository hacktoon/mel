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

    def eval(self, context):
        # TODO: reserved for language use. Ex: ReferenceParser#scope
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
        self.properties = {  # TODO: get this from PropertyNode subclasses
            "uid": {},
            "flag": {},
            "attribute": {},
            "variable": {},
            "doc": {},
            "format": {},
        }

    def add(self, value_node):
        super().add(value_node)
        if value_node.id in self.properties.keys():
            prop = self.properties[value_node.id]
            prop[value_node.name] = value_node

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
        return evaluator(self.name.value, context)


class UIDNode(PropertyNode):
    id = "uid"


class FlagNode(PropertyNode):
    id = "flag"


class AttributeNode(PropertyNode):  # TODO rename to MetaNode
    id = "attribute"


class FormatNode(PropertyNode):
    id = "format"


class VariableNode(PropertyNode):
    id = "variable"


class DocNode(PropertyNode):
    id = "doc"


class LiteralNode(Node):
    def __init__(self):
        super().__init__()
        self.token = None  # TODO: use Token

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        return evaluator(self.token.value, context)


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"
