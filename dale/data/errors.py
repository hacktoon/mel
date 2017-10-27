import re


class LexingError(Exception):
    def __init__(self, message, line, column):
        super().__init__(message)
        self.line = line
        self.column = column


class ParsingError(Exception):
    def __init__(self, error, text):
        super().__init__(self._build_message(error, text))
        self.line = error.line
        self.column = error.column

    def _build_message(self, error, text):
        lines = text.splitlines()
        prev_line = max(0, error.line - 2)
        snippet = '\n'.join(lines[prev_line:error.line])
        column = error.column - 1
        
        if snippet.strip() == '':
            return 'Syntax error: ' + str(error)
        else:
            template = 'Syntax error: {}\n{}\n{}^'
            return template.format(str(error), snippet, ' ' * column)
