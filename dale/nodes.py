def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self._nodes = []
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __len__(self):
        return len(self._nodes)

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        return "{}('{}')".format(self.id.upper(), self)

    def __getitem__(self, index):
        return self._nodes[index]

    def add(self, node):
        method_name = "_add_" + node.id
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(node)
        else:
            self._nodes.append(node)

    def eval(self, context):
        return {
            "id": self.id,
            "nodes": [node.eval(context) for node in self._nodes]
        }


class NullNode(Node):
    id = "null"

    def __bool__(self):
        return False

    def __str__(self):
        return ""

    def eval(self, context):
        return


class WildcardNode(Node):
    id = "wildcard"


class ScopeNode(Node):
    id = "scope"

    def __init__(self):
        super().__init__()
        self.key = NullNode()
        self.attributes = {
            "flag": {},
            "uid": {},
            "property": {},
            "variable": {},
            "format": {},
            "doc": {},
        }
        self.flags = {}
        self.uids = {}
        self.properties = {}
        self.variables = {}
        self.formats = {}
        self.docs = {}

    def eval(self, context):
        return {
            "id": self.id,
            "key": self.key.eval(context) if self.key else None,
            "nodes": [node.eval(context) for node in self._nodes]
        }


class RootNode(ScopeNode):
    id = "root"


class QueryNode(ScopeNode):
    id = "query"

    def __init__(self):
        super().__init__()
        self.criteria = []


class ListNode(Node):
    id = "list"


class PropertyNode(Node):
    id = "property"

    def __init__(self):
        super().__init__()
        self.name = ""


class FlagNode(PropertyNode):
    id = "flag"


class UIDNode(PropertyNode):
    id = "uid"


class FormatNode(PropertyNode):
    id = "format"


class VariableNode(PropertyNode):
    id = "variable"


class DocNode(PropertyNode):
    id = "doc"


class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.value = (0, 0)

    def __getitem__(self, index):
        return self.value[index]


class LiteralNode(Node):
    def __init__(self):
        super().__init__()
        self.value = None


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"


class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.target = None
        self.relationship = None
