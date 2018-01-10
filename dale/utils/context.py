

class Context:
    def __init__(self):
        self._variables = {}
        self._evaluators = {}
        self._settings = {}

    def var(self, key, value=None, default=''):
        if value is None:
            return self._variables.get(key, default)
        self._variables[key] = value

    def evaluator(self, key, function=None, default=lambda x: x):
        if function is None:
            return self._evaluators.get(key, default)
        self._evaluators[key] = function

    def config(self, key, value=None, default=''):
        if value is None:
            return self._settings.get(key, default)
        self._settings[key] = value
