
class ErrorFormatter:
    def __init__(self, error):
        self.error = error
        self.lines = error.token.text.splitlines(keepends=True)
        self.digits_offset = len(str(len(self.lines)))
        self.line = error.token.line - 1
        self.column = error.token.column
        self.delimiter = " | "

    def format(self, lines_offset=4):
        tpl = "Error at line {line}, column {column}.\n{error}\n\n{snippet}\n"
        return tpl.format(
            line=self.error.token.line,
            column=self.error.token.column + 1,
            snippet=self._snippet(lines_offset),
            error=self.error,
        )

    def _snippet(self, lines_offset):
        lines = []
        min_index = max(0, self.line - lines_offset)
        max_index = min(self.line + lines_offset, len(self.lines))

        for index in range(min_index, max_index):
            line = self._prefix_line(self.lines[index], index)
            lines.append(line.strip())
            if index == self.line:
                lines.append(self._build_error_pointer())
        return "\n".join(lines)

    def _prefix_line(self, line, index):
        line_num = str(index + 1).zfill(self.digits_offset)
        return "{}{}{}".format(line_num, self.delimiter, line)

    def _build_error_pointer(self):
        prefix_length = self.digits_offset + len(self.delimiter)
        arrow_length = prefix_length + self.column
        return arrow_length * "-" + "^"
