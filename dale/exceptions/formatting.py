class ErrorFormatter:
    def __init__(self, text, error):
        self.error = error
        self.lines = text.splitlines(keepends=True)
        self.line_index, self.column_index = self._get_position()
        self.digits_offset = len(str(len(self.lines)))
        self.delimiter = " |    "

    def format(self, lines_offset=4):
        tpl = "Error at line {line}, column {column}.\n{error}.\n\n{code}\n"
        return tpl.format(
            line=self.line_index + 1,
            column=self.column_index + 1,
            error=self.error,
            code=self._build_code_snippet(lines_offset),
        )

    def _get_position(self):
        chars_read = 0
        for line_index, line in enumerate(self.lines):
            if self.error.index < chars_read + len(line):
                column_index = self.error.index - chars_read
                return line_index, column_index
            else:
                chars_read += len(line)

    def _build_code_snippet(self, lines_offset):
        lines = []
        min_index = max(0, self.line_index - lines_offset)
        max_index = min(self.line_index + lines_offset, len(self.lines))

        for index in range(min_index, max_index):
            line = self._prefix_line(self.lines[index], index)
            lines.append(line.strip("\r\n"))
            if index == self.line_index:
                lines.append(self._build_error_pointer())
        return "\n".join(lines)

    def _prefix_line(self, line, index):
        line_num = str(index + 1).zfill(self.digits_offset)
        return "{}{}{}".format(line_num, self.delimiter, line)

    def _build_error_pointer(self):
        prefix_length = self.digits_offset + len(self.delimiter)
        arrow_length = prefix_length + self.column_index
        return arrow_length * "-" + "^"
