
class Node:
    def __init__(self, text='', index=(0, 0)):
        self.text = text
        self.index = index

    def __bool__(self):
        return True

    def __str__(self):
        return self.text

    def __repr__(self):
        return "NODE({})".format(self)

    def eval(self):
        return str(self)


class StringNode(Node):
    pass


class PatternNode(Node):
    pass


class EmptyNode(Node):
    def __bool__(self):
        return False


class RuleNode(Node):
    def __init__(self, id=''):
        self.id = id
        self.children = []

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def __iter__(self):
        for child in self.children:
            yield child

    def __str__(self):
        return ''.join(str(child) for child in self.children)

    @property
    def index(self):
        if len(self.children) == 0:
            return super().index
        first = self.children[0].index
        last = self.children[-1].index
        return first[0], last[1]

    def add(self, child):
        self.children.append(child)
