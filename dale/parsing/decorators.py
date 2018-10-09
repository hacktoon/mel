

def indexed(method):
    def surrogate(self):
        first = self.stream.current()
        node = method(self)
        if not node:
            return
        last = self.stream.current(-1)
        node.index = first.index[0], last.index[1]
        return node
    return surrogate
