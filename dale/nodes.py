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


# METADATA ============================

class MetadataNode(Node):
    id = "metadata"


class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.path = NullNode()
        self.value = NullNode()


class EqualNode(RelationNode):
    id = "equal"


class DifferentNode(RelationNode):
    id = "different"


class GreaterThanNode(RelationNode):
    id = "greater_than"


class GreaterThanEqualNode(RelationNode):
    id = "greater_than_equal"


class LessThanNode(RelationNode):
    id = "less_than"


class LessThanEqualNode(RelationNode):
    id = "less_than_equal"


class ObjectNode(Node):
    id = "object"


class ReferenceNode(ObjectNode):
    id = "reference"


class StructNode(Node):
    id = "struct"

    def __init__(self):
        super().__init__()
        self.key = NullNode()
        self.props = {
            "flag": {},
            "uid": {},
            "attribute": {},
            "variable": {},
            "format": {},
            "doc": {},
        }
        self.children = {}

    def _add_flag(self, node):
        self.props[node.id][node.name] = node

    def _add_scope(self, scope):
        if scope.key.id in self.props:
            self.props[scope.key.id][scope.key.name] = scope
        else:
            self._nodes.append(scope)

    def _add_equal(self, relation):
        if not relation.key:
            self._nodes.append(relation)
            return
        if relation.key.id == "name":
            key = "attribute"
        else:
            key = relation.key.id
        self.props[key][relation.key.name] = relation

    def eval(self, context):
        return {
            "id": self.id,
            "key": self.key.eval(context) if self.key else None,
            "nodes": [node.eval(context) for node in self._nodes]
        }


class RootNode(Node):
    id = "root"


class ScopeNode(StructNode):
    id = "scope"


class QueryNode(StructNode):
    id = "query"

    def __init__(self):
        super().__init__()
        self.criteria = []


class ListNode(Node):
    id = "list"


class FlagNode(Node):
    id = "flag"


class KeywordNode(Node):
    id = "keyword"

    def __init__(self):
        super().__init__()
        self.value = ""


class NameNode(KeywordNode):
    id = "name"


class ReservedNameNode(NameNode):
    id = "reserved-name"


class UIDNode(KeywordNode):
    id = "uid"


class FormatNode(KeywordNode):
    id = "format"


class VariableNode(KeywordNode):
    id = "variable"


class DocNode(KeywordNode):
    id = "doc"


class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None


class LiteralNode(Node):
    id = "literal"

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


# PATH ============================

class PathNode(Node):
    id = "path"

    def __repr__(self):
        txt = ''.join([str(node) for node in self._nodes])
        return "{}('{}')".format(self.id.upper(), txt)


class SubPathNode(Node):
    def __init__(self):
        super().__init__()
        self.keyword = None


class ChildPathNode(SubPathNode):
    id = "child-path"


class MetadataPathNode(SubPathNode):
    id = "metadata-path"

