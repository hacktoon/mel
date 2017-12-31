import errno


class DaleError(Exception):
    pass


class InvalidSyntaxError(DaleError):
    def __init__(self, index):
        super().__init__('Invalid syntax')
        self.index = index


class FileError(DaleError):
    def __init__(self, token, original_error):
        if original_error.errno == errno.ENOENT:
            template = 'File {!r} could not be found or doesn\'t exist.'
        elif original_error.errno == errno.EPERM:
            template = 'No permission to open file {!r}.'
        super().__init__(template.format(token.value))
        self.index = token.index


class UnexpectedTokenError(DaleError):
    def __init__(self, token, allowed_values=None):
        message = 'Found a {!r} token.'.format(token.id)
        if allowed_values:
            message += ' Expected token(s): ' + str(allowed_values)
        super().__init__(message)
        self.index = token.index


class ErrorMessage:
    def __init__(self, text, error):
        self.error = error
        self.lines = text.splitlines(keepends=True)
        self.line, self.column = self.get_position()

        self.line_prefix_length = len(str(len(self.lines)))
        self.delimiter = ' |    '

    def build(self):
        annotated_code = ''.join(self.prefix_lines())
        return '{}\n\n{}'.format(str(self.error), annotated_code)

    def get_position(self):
        chars_read = 0
        for line_index, line in enumerate(self.lines):
            if self.error.index < len(line) + chars_read:
                column_index = self.error.index - chars_read
                return line_index, column_index
            else:
                chars_read += len(line)

    def prefix_lines(self):
        def prefix(line, index):
            line_num = str(index + 1).zfill(self.line_prefix_length)
            return '{}{}{}'.format(line_num, self.delimiter, line)

        lines = enumerate(self.lines)
        prefixed_lines = [prefix(line, index) for index, line in lines]

        self.prefix_error_pointer(prefixed_lines)
        return prefixed_lines

    def prefix_error_pointer(self, prefixed_lines):
        prefix_length = self.line_prefix_length + len(self.delimiter)
        arrow_length = prefix_length + self.column
        error_pointer = arrow_length * '-' + '^\n'
        prefixed_lines.insert(self.line + 1, error_pointer)

    


