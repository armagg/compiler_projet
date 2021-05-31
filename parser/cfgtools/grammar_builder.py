from parser.cfgtools.grammar import Grammar
from parser.cfgtools.production import Production


class GrammarBuilder:
    def __init__(self):
        self.grammar = Grammar()

    def add_production(self, prod_str):
        prod = Production(prod_str, self.grammar)
        self.grammar.add_production(prod)

    def set_start(self, start):
        start = self.grammar.get_or_create_nonterminal(start)
        self.grammar.set_start(start)
        return self

    @staticmethod
    def from_file(file_address):
        instance = GrammarBuilder()
        with open(file_address, 'r') as f:
            lines = f.readlines()
        productions_str = [line.split() for line in lines if line.strip()]
        for prod_str in productions_str:
            instance.add_production(prod_str)
        return instance.set_start(productions_str[0][0])

    def build(self):
        return self.grammar
