class Index:  # pragma: nocover
    def __init__(self, start=0, end=None):
        self.start = start
        self.end = end

    def __bool__(self):
        return all([self.start, self.end])


class Context:
    def __init__(self):
        self.tree = {}
        self.evaluators = {}
        self.text = ""
        self.stream = None
