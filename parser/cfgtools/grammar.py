from parser.cfgtools.non_terminal import NonTerminal
from parser.cfgtools.terminal import Terminal


class Grammar:
    def __init__(self):
        self.non_terminals = []
        self.start_nt = None

    def set_start(self, nt):
        self.start_nt = nt
        nt.follow.add(Terminal.get_instance('_EOF'))

    def get_or_create_nonterminal(self, new_nt):
        for nt in self.non_terminals:
            if nt.value == new_nt:
                return nt
        return self.add_nt(new_nt)

    def add_nt(self, nt):
        new_nt = NonTerminal(nt)
        self.non_terminals.append(new_nt)
        return new_nt

    @staticmethod
    def add_production(lhs, rhs):
        lhs.add_production(rhs)

    def calculate_parse_table(self):
        self.calculate_follow_sets()
        for nt in self.non_terminals:
            nt.build_parse_table()

    def calculate_follow_sets(self):
        self.calculate_first_sets()
        updated = True
        while updated:
            updated = False
            for nt in self.non_terminals:
                if nt.update_follow_set():
                    updated = True

    def calculate_first_sets(self):
        updated = True
        while updated:
            updated = False
            for nt in self.non_terminals:
                if nt.update_first_set():
                    updated = True
