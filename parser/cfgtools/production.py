from parser.cfgtools.terminal import Terminal
from parser.cfgtools.action_symbol import ActionSymbol
from parser.cfgtools.grammar_element import GrammarElement


class Production:
    def __init__(self, prod_str, grammar):
        self.grammar = grammar
        self.elems = []
        for elem_str in prod_str:
            if elem_str.startswith('_'):
                elem = Terminal.get_instance(elem_str)
            elif elem_str.startswith('#'):
                elem = ActionSymbol(elem_str)
            else:
                elem = self.grammar.get_or_create_nonterminal(elem_str)
            self.elems.append(elem)

    @property
    def lhs(self):
        return self.elems[0]

    @property
    def rhs(self):
        return self.elems[1:]

    @property
    def hard_elements(self):
        return list(filter(
            lambda e: isinstance(e, GrammarElement),
            self.rhs,
        ))
