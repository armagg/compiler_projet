class GrammarElement:
    def is_terminal(self):
        pass

    def can_empty(self):
        pass

    def match(self, tokens, errors, ss, pb, symbol_table):
        pass
