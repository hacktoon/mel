import errno


def _get_line_column(lines, error_index):
    chars_read = 0
    for line_index, line in enumerate(lines):
        if error_index < len(line) + chars_read:
            column_index = error_index - chars_read
            return line_index, column_index
        else:
            chars_read += len(line)


def _prefix_lines(lines, error_index):
    line_index, column_index = _get_line_column(lines, error_index)
    offset_length = len(str(len(lines)))
    delimiter = '|    '

    def prefix(line, line_index):
        line_num = str(line_index + 1).zfill(offset_length)
        return '{}{}{}'.format(line_num, delimiter, line)

    prefixed_lines = [prefix(line, index) for index, line in enumerate(lines)]

    arrow_length = offset_length + len(delimiter) + column_index
    line_info = arrow_length * '-' + '^\n'
    prefixed_lines.insert(line_index + 1, line_info)

    return prefixed_lines


def build_message(text, error_index):
    display_range = 5
    lines = text.splitlines(keepends=True)
    prefixed_lines = _prefix_lines(lines, error_index)
    return ''.join(prefixed_lines)


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
