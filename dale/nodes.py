
def _default_evaluator(value, context):
    return value


class Node:
    def __init__(self):
        self.id = self.__class__.__name__
        self.text = ''
        self.index = (0, 0)
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def eval(self, context):
        # TODO: reserved for language use. Ex: ReferenceParser#scope
        pass

    def __getitem__(self, index):
        return self.nodes[index]

    def __str__(self):
        first, last = self.index
        return self.text[first: last]

    def __repr__(self):
        values = [str(n) for n in self.nodes]
        return "{}({})".format(self.id, ' '.join(values))


class ReferenceNode(Node):
    def eval_scope(self, context):
        pass

    def eval(self, context):
        # TODO: reserved for language use. Ex: ReferenceParser#scope
        pass

    def __repr__(self):
        values = [str(n) for n in self.nodes]
        return "{}({})".format(self.id, '/'.join(values))


class ScopeNode(Node):
    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)

    def __repr__(self):
        values = [str(self.key)]
        values.extend([str(n) for n in self.nodes])
        return "{}({})".format(self.id, ' '.join(values))


class QueryNode(Node):
    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)

    def __repr__(self):
        values = [str(self.key)]
        values.extend([str(n) for n in self.nodes])
        return "{}({})".format(self.id, ' '.join(values))


class ListNode(Node):
    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(values, context)

    def __repr__(self):
        values = [str(n) for n in self.nodes]
        return "{}({})".format(self.id, ' '.join(values))


class PropertyNode(Node):
    def __init__(self):
        super().__init__()
        self.name = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        return evaluator(self.name.value, context)

    def __repr__(self):
        return "{}({})".format(self.id, self.name.value)


class UIDNode(PropertyNode):
    pass


class FlagNode(PropertyNode):
    pass


class AttributeNode(PropertyNode):   # TODO rename to MetaNode
    pass


class FormatNode(PropertyNode):
    pass


class AliasNode(PropertyNode):
    pass


class DocNode(PropertyNode):
    pass


class LiteralNode(Node):
    def __init__(self):
        super().__init__()
        self.token = None  # TODO: use Token

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        return evaluator(self.token.value, context)

    def __repr__(self):
        value = str(self.token.value)
        return "{}({})".format(self.id, value)


class IntNode(LiteralNode):
    pass


class FloatNode(LiteralNode):
    pass


class BooleanNode(LiteralNode):
    pass


class StringNode(LiteralNode):
        pass
