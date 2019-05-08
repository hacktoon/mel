def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.children = []
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.children)

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        return "{}('{}')".format(self.id.upper(), self)

    def __getitem__(self, index):
        return self.children[index]

    def add(self, node):
        method_name = "_add_" + node.id
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(node)
        else:
            self.children.append(node)

    def eval(self, context):
        return {
            "id": self.id,
            "nodes": [node.eval(context) for node in self.children]
        }


class NullNode(Node):
    id = "null"

    def __bool__(self):
        return False

    def __str__(self):
        return ""

    def eval(self, context):
        return


# ROOT ========================================================

class RootNode(Node):
    id = "root"


# META ========================================================

class MetaNode(Node):
    id = "meta"


class StatementNode(Node):
    id = "statement"

    def __init__(self):
        super().__init__()
        self.key = NullNode()
        self.symbol = NullNode()
        self.value = NullNode()


class SymbolNode(Node):
    pass


class EqualNode(SymbolNode):
    id = "equal"


class DifferentNode(SymbolNode):
    id = "different"


class GreaterThanNode(SymbolNode):
    id = "greater_than"


class GreaterThanEqualNode(SymbolNode):
    id = "greater_than_equal"


class LessThanNode(SymbolNode):
    id = "less_than"


class LessThanEqualNode(SymbolNode):
    id = "less_than_equal"


# OBJECT ========================================================

class ObjectNode(Node):
    id = "object"


# REFERENCE ========================================================

class ReferenceNode(Node):
    id = "reference"


class HeadReferenceNode(Node):
    id = "head-reference"


class SubreferenceNode(Node):
    id = "subreference"


class ChildReferenceNode(Node):
    id = "child-reference"


class RangeReferenceNode(SubreferenceNode):
    id = "range-reference"


class IntReferenceNode(SubreferenceNode):
    id = "int-reference"


class SubreferenceListNode(SubreferenceNode):
    id = "subreference-list"


# STRUCT ========================================================

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

    def eval(self, context):
        return {
            "id": self.id,
            "key": self.key.eval(context) if self.key else None,
            "nodes": [node.eval(context) for node in self.children]
        }


class ScopeNode(StructNode):
    id = "scope"


class QueryNode(StructNode):
    id = "query"

    def __init__(self):
        super().__init__()
        self.criteria = []


# LIST ========================================================

class ListNode(Node):
    id = "list"


# KEYWORD ========================================================

class KeywordNode(Node):
    id = "keyword"

    def __init__(self):
        super().__init__()
        self.value = ""


class NameNode(KeywordNode):
    id = "name"


class ReservedNameNode(NameNode):
    id = "reserved-name"


class FlagNode(KeywordNode):
    id = "flag"


class UIDNode(KeywordNode):
    id = "uid"


class FormatNode(KeywordNode):
    id = "format"


class VariableNode(KeywordNode):
    id = "variable"


class DocNode(KeywordNode):
    id = "doc"


# RANGE ========================================================

class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None


# LITERAL ========================================================

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


# PATH ========================================================

class PathNode(Node):
    id = "path"

    def __repr__(self):
        txt = ''.join([str(node) for node in self.children])
        return "{}('{}')".format(self.id.upper(), txt)


# WILDCARD ========================================================

class WildcardNode(Node):
    id = "wildcard"
