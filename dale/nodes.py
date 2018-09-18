
def _default_evaluator(value, context):
    return value


class BaseNode:
    def __init__(self):
        self.text = ''
        self.text_range = (0, 0)

    def __repr__(self):
        first, last = self.text_range
        return self.text[first: last]


class RootNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)


class ReferenceNode(RootNode):
    def eval(self, context):
        pass


class ScopeNode(RootNode):
    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get('ScopeNode', _default_evaluator)
        values = [value.eval(context) for value in self.values]
        return evaluator(values, context)


class QueryNode(ScopeNode):
    def eval(self, context):
        evaluator = context.evaluators.get('QueryNode', _default_evaluator)
        values = [value.eval(context) for value in self.values]
        return evaluator(values, context)


class ListNode(RootNode):
    def eval(self, context):
        evaluator = context.evaluators.get('ListNode', _default_evaluator)
        values = [value.eval(context) for value in self.values]
        return evaluator(values, context)


class PropertyNode(BaseNode):
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


class AttributeNode(PropertyNode):
    pass


class FormatNode(PropertyNode):
    pass


class AliasNode(PropertyNode):
    pass


class DocNode(PropertyNode):
    pass


class LiteralNode(BaseNode):
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
