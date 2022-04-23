from ..stream import CharStream
from ..produce import Produce


########################################################################
# BASE PARSER
########################################################################
class Parser:
    def _hints(self):
        return ''

    def parse(self, stream: CharStream, index: int = 0) -> Produce:
        raise NotImplementedError
