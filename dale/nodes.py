class BaseNode:
    def __init__(self):
        self.text = ''
        self.text_range = (0, 0)

    def __repr__(self):
        first, last = self.text_range
        return self.text[first: last]


class Node(BaseNode):
    def __init__(self):
        self.values = []
        self.refs = {}

    def add(self, node, alias=None):
        self.values.append(node)
        if alias is not None:
            self.refs[alias] = node

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.refs[key]
        return self.values[key]

    def eval(self, context):
        values = [value.eval(context) for value in self.values]
        return values[0] if len(values) == 1 else values


class ReferenceNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.names = []

    def add(self, name):
        self.names.append(name)

    def read(self, node, name):
        try:
            return node[name.value]
        except KeyError:

    defeval(self, context):
     def get_node(node, names):
            name = names[0]
            if len(names) == 1:
                return self.read(node, name)
            node = self.read(node, name)
            return get_node(node, names[1:])

        node = get_node(context.tree, self.names)
        return node.eval(context)


class ScopeNode(Node):
    def _eval_items(self, kwargs, context):
        return {key: attr.eval(context) for key, attr in kwargs.items()}

    def eval(self, context):
        def default_evaluator(value, context):
            return value

        evaluator = context.evaluators.get('scope', default_evaluator)
        return evaluator({
            'name': self.name.value,
            'flags': [flag.value for flag in self.flags],
            'attrs': self._eval_items(self.attrs, context),
            'refs': self._eval_items(self.refs, context),
            'values': [value.eval(context) for value in self.values]
        }, context)


class WriteScopeNode(Node):
    pass


class ReadScopeNode(Node):
    pass


class ListScopeNode(Node):
    def __init__(self):
        super().__init__()
        self.items = []

    def add(self, item):
        self.items.append(item)

    def eval(self, context):
        evaluator = context.evaluators.get('list', lambda val, ctx: val)
        return evaluator([item.eval(context) for item in self.items], context)


class PropertyNode(BaseNode):
    def eval(self, context):
        node_name = self.__class__.__name__
        default_eval = lambda evaluator, context: evaluator
        evaluator = context.evaluators.get(node_name, default_eval)
        return evaluator(self.token.value, context)


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
    def eval(self, context):
        node_name = self.__class__.__name__
        default_eval = lambda evaluator, context: evaluator
        evaluator = context.evaluators.get(node_name, default_eval)
        return evaluator(self.token.value, context)


class IntNode(LiteralNode):
    pass


class FloatNode(LiteralNode):
    pass


class BooleanNode(LiteralNode):
    pass


class StringNode(LiteralNode):
        pass
