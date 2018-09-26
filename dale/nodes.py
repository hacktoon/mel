
def _default_evaluator(value, context):
    return value


class Node:
    def __init__(self):
        self.text = ''
        self.index = (0, 0)       # TODO change to Snippet class
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def __repr__(self):
        first, last = self.index
        return self.text[first: last]


class ReferenceNode(Node):
    def eval_scope(self, context):
        pass

    def eval(self, context):
        pass


class ScopeNode(Node):
    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get('ScopeNode', _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)


class QueryNode(Node):
    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get('QueryNode', _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)


class ListNode(Node):
    def eval(self, context):
        evaluator = context.evaluators.get('ListNode', _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(values, context)


class PropertyNode(Node):
    def __init__(self):
        super().__init__()
        self.name = None

    def eval(self, context):
        node_name = self.__class__.__name__
        evaluator = context.evaluators.get(node_name, _default_evaluator)
        return evaluator(self.name.value, context)


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
        self.token = None

    def eval(self, context):
        node_name = self.__class__.__name__
        evaluator = context.evaluators.get(node_name, _default_evaluator)
        return evaluator(self.token.value, context)


class IntNode(LiteralNode):
    pass


class FloatNode(LiteralNode):
    pass


class BooleanNode(LiteralNode):
    pass


class StringNode(LiteralNode):
        pass
