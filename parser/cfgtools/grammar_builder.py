from parser.cfgtools.grammar import Grammar
from parser.cfgtools.terminal import Terminal


class GrammarBuilder:
    def __init__(self):
        self.grammar = Grammar()

    def add_production(self, prod_str):
        prod = []
        for elem_str in prod_str:
            if elem_str.startswith('_'):
                elem = Terminal.get_instance(elem_str)
            else:
                elem = self.grammar.get_or_create_nonterminal(elem_str)
            prod.append(elem)
        self.grammar.add_production(prod[0], prod[1:])

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
