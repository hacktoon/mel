def builder(node_class):
    def decorator(method):
        def surrogate(self, *args):
            first = self.stream.current()
            node = self._create_node(node_class)
            node = method(self, node)
            if not node:
                return
            last = self.stream.current(-1)
            node.index = first.index[0], last.index[1]
            return node
        return surrogate
    return decorator


def mapbuilder(node_map):
    def decorator(method):
        def surrogate(self, *args):
            first = self.stream.current()
            if first.id not in node_map:
                return
            node = self._create_node(node_map[first.id])
            node = method(self, node)
            if not node:
                return
            last = self.stream.current(-1)
            node.index = first.index[0], last.index[1]
            return node
        return surrogate
    return decorator
