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
        self.line_index, self.column_index = self._get_position()
        self.digits_offset = len(str(len(self.lines)))
        self.delimiter = ' |    '

    def build(self, line_range=4):
        code_snippet = self._build_code_snippet(line_range)
        tpl = 'Error at line {line}, column {column}.\n{error}.\n\n{code}'
        return tpl.format(
            line = self.line_index + 1,
            column = self.column_index + 1,
            error = self.error,
            code = code_snippet
        )

    def _get_position(self):
        chars_read = 0
        for line_index, line in enumerate(self.lines):
            if self.error.index >= chars_read:
                column_index = self.error.index - chars_read
                return line_index, column_index
            else:
                chars_read += len(line)

    def _build_code_snippet(self, line_range):
        prefixed_lines = ''
        min_index = max(0, self.line_index - line_range)
        max_index = min(self.line_index + line_range, len(self.lines))

        for index in range(min_index, max_index + 1):
            line = self._prefix_line(self.lines[index], index)
            prefixed_lines += line
            if index == self.line_index:
                prefixed_lines += self._build_error_pointer()
        return prefixed_lines

    def _prefix_line(self, line, index):
        line_num = str(index + 1).zfill(self.digits_offset)
        return '{}{}{}'.format(line_num, self.delimiter, line)

    def _build_error_pointer(self):
        prefix_length = self.digits_offset + len(self.delimiter)
        arrow_length = prefix_length + self.column_index
        return arrow_length * '-' + '^\n'
