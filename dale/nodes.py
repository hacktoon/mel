def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.text = ""
        self.index = (0, 0)
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

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
        values = [str(n) for n in self.nodes if n]
        return "{}({})".format(self.id, " ".join(values))


class RootNode(Node):
    id = "root"


class PathNode(Node):
    id = "path"

    def eval_scope(self, context):
        pass

    def eval(self, context):
        # TODO: reserved for language use. Ex: ReferenceParser#scope
        pass

    def __repr__(self):
        values = [str(n) for n in self.nodes]
        return "{}({})".format(self.id, "/".join(values))


class ScopeNode(Node):
    id = "scope"

    def __init__(self):
        super().__init__()
        self.key = None
        self.flags = {}

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)

    def add_flag(self, flag):
        self.add(flag)
        self.flags[flag.name.value] = flag

    def __repr__(self):
        key = str(self.key) if self.key else ""
        values = [key] + [str(n) for n in self.nodes if n]
        return "{}({})".format(self.id, " ".join(values))


class QueryNode(Node):
    id = "query"

    def __init__(self):
        super().__init__()
        self.key = None

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(self.key, values, context)

    def __repr__(self):
        key = str(self.key) if self.key else ""
        values = [key] + [str(n) for n in self.nodes if n]
        return "{}({})".format(self.id, " ".join(values))


class ListNode(Node):
    id = "list"

    def eval(self, context):
        evaluator = context.evaluators.get(self.id, _default_evaluator)
        values = [node.eval(context) for node in self.nodes]
        return evaluator(values, context)

    def __repr__(self):
        values = [str(n) for n in self.nodes]
        return "{}({})".format(self.id, " ".join(values))


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

    def __repr__(self):
        value = str(self.token.value)
        return "{}({})".format(self.id, value)


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"
