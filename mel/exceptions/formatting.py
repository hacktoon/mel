
class ErrorFormatter:
    def __init__(self, error):
        self.message = str(error)
        self.lines = error.text.splitlines()
        self.line = error.line
        self.column = error.column
        self._digits_offset = len(str(len(self.lines)))
        self._linenum_sep = " | "

    def format(self, lines_offset=4):
        tpl = "Error at line {line}, column {column}.\n{msg}\n\n{snippet}\n"
        snippet = self._snippet(lines_offset)
        return tpl.format(
            line=self.line + 1,
            column=self.column + 1,
            snippet=snippet,
            msg=self.message
        )

    def _snippet(self, lines_offset):
        lines = []
        min_index, max_index = self._line_range(lines_offset)
        for index in range(min_index, max_index):
            lines.append(self._line_prefix(index))
            if index == self.line:
                lines.append(self._error_pointer())
        return "\n".join(lines)

    def _line_range(self, lines_offset):
        min_index = max(0, self.line - lines_offset)
        max_index = min(self.line + lines_offset, len(self.lines))
        return min_index, max_index

    def _line_prefix(self, index):
        line_num = str(index + 1).zfill(self._digits_offset)
        return "{}{}{}".format(line_num, self._linenum_sep, self.lines[index])

    def _error_pointer(self):
        prefix_length = self._digits_offset + len(self._linenum_sep)
        arrow_length = prefix_length + self.column
        return arrow_length * "-" + "^"
