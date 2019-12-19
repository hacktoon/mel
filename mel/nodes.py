
class Node:
    def __bool__(self):
        return True

    def __repr__(self):
        name = self.__class__.__name__.upper()
        return "{}({})".format(name, self)


class SymbolNode(Node):
    def __init__(self, text='', index=(0, 0)):
        self.text = text
        self.index = index

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text


class EmptyNode(Node):
    def __bool__(self):
        return False

    def __str__(self):
        return ''


class RuleNode(Node):
    def __init__(self, id=''):
        self.id = id
        self.children = []

    def __bool__(self):
        return len(self.children) > 0

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def __str__(self):
        return ' '.join(str(child) for child in self.children)

    @property
    def index(self):
        if len(self.children) == 0:
            return ('aa', 0)
        first = self.children[0].index
        last = self.children[-1].index
        return first[0], last[1]

    def add(self, child):
        if not child:
            return
        self.children.append(child)
