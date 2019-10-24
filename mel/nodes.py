
class Node:
    skip = False

    def __init__(self, id):
        self.id = id

    def __bool__(self):
        return True

    def __str__(self):
        return self.id

    def __repr__(self):
        return "NODE({})".format(self)

    @property
    def index(self):
        return (0, 0)

    def eval(self):
        return str(self)


class EmptyNode(Node):
    skip = True

    def __init__(self):
        super().__init__('')

    def __bool__(self):
        return False


class TokenNode(Node):
    def __init__(self, id, token):
        super().__init__(id)
        self.token = token

    def __str__(self):
        return self.token.text

    @property
    def index(self):
        return self.token.index


class StringNode(TokenNode):
    skip = True


class RuleNode(Node):
    def __init__(self, id=''):
        super().__init__(id)
        self.children = []

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, index):
        return self.children[index]

    def __str__(self):
        return ''.join(str(child) for child in self.children)

    @property
    def index(self):
        if len(self.children) == 0:
            return super().index()
        first = self.children[0].index()
        last = self.children[-1].index()
        return first[0], last[1]

    def add(self, child):
        if child.skip:
            return
        self.children.append(child)
