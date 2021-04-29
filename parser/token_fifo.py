from scanner.token_type import TokenType


class TokenFifo:
    def __init__(self, scanner):
        self.scanner = scanner
        self.lookahead = self.scanner.get_next_token()

    def advance(self):
        if self.lookahead and self.lookahead[0] == TokenType.EOF:
            self.lookahead = None
        else:
            self.lookahead = self.scanner.get_next_token()

    @property
    def line_no(self):
        return self.scanner.line_no
