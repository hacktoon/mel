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
        prev_index = max(0, error.line - 2)
        prev_line = '{}\t{}'.format(prev_index + 1, lines[prev_index])
        index = error.line - 1
        line = '{}\t{}'.format(index + 1, lines[index])
        snippet = '\n'.join([prev_line, line])
        column = error.column - 1

        if snippet.strip() == '':
            return 'Syntax error: ' + str(error)
        else:
            template = 'Syntax error: {}\n\n{}\n\t{}^'
            return template.format(str(error), snippet, ' ' * column)
