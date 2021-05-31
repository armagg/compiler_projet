from anytree import Node

from parser.cfgtools.grammar_element import GrammarElement
from parser.cfgtools.terminal import Terminal
from scanner.token_type import TokenType


class NonTerminal(GrammarElement):
    def __init__(self, value):
        self.productions = []
        self.value = value
        self.first = set()
        self.follow = set()
        self.parse_table = dict()
        pass

    def is_terminal(self):
        return False

    def add_production(self, prod):
        self.productions.append(prod)

    def can_empty(self):
        return Terminal.Epsilon in self.first

    def update_first_set(self):
        initial_size = len(self.first)
        for prod in self.productions:
            prod = prod.hard_elements
            empty_count = 0
            for elem in prod:
                self.first = self.first.union(elem.first - {Terminal.Epsilon})
                if not elem.can_empty():
                    break
                empty_count += 1
            if empty_count == len(prod):
                self.first.add(Terminal.Epsilon)
        return len(self.first) > initial_size

    def update_follow_set(self):
        updated = False
        for prod in self.productions:
            prod = prod.hard_elements
            for idx, cur in enumerate(prod):
                if not isinstance(cur, NonTerminal):
                    continue

                initial_size = len(cur.follow)
                empty_count = 0
                for nxt in prod[idx + 1:]:
                    cur.follow = cur.follow.union(
                        nxt.first - {Terminal.Epsilon}
                    )
                    if not nxt.can_empty():
                        break
                    empty_count += 1
                if empty_count == len(prod[idx + 1:]):
                    cur.follow = cur.follow.union(self.follow)

                if len(cur.follow) > initial_size:
                    updated = True

        return updated

    def build_parse_table(self):
        for idx, prod in enumerate(self.productions):
            prod = prod.hard_elements
            empty_count = 0
            for elem in prod:
                for terminal in elem.first:
                    self.parse_table[terminal] = idx
                if not elem.can_empty():
                    break
                empty_count += 1
            if empty_count == len(prod):
                for terminal in self.follow:
                    if terminal not in self.parse_table:
                        self.parse_table[terminal] = idx
        for terminal in self.follow:
            if terminal not in self.parse_table:
                self.parse_table[terminal] = -1

    def match(self, tokens, errors):
        while True:
            lookahead = tokens.lookahead
            if lookahead is None:
                return None
            node = Node(self.value)
            for key, prod_idx in self.parse_table.items():
                if key.matches_token(lookahead):
                    if prod_idx == -1:
                        errors.add_error(
                            tokens.line_no,
                            f'syntax error, missing {self.value}',
                        )
                        return None
                    else:
                        cur_prod = self.productions[prod_idx].hard_elements
                        if cur_prod:
                            for elem in cur_prod:
                                child_node = elem.match(tokens, errors)
                                if child_node:
                                    child_node.parent = node
                        else:
                            child_node = Terminal.Epsilon.match(tokens, errors)
                            child_node.parent = node
                        return node
            if lookahead[0] == TokenType.EOF:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, unexpected EOF'
                )
            elif lookahead[0] in [TokenType.NUM, TokenType.ID]:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, illegal {lookahead[0]}'
                )
            else:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, illegal {lookahead[1]}'
                )
            tokens.advance()

    def print_follow(self):
        print('Follows:')
        for terminal in self.follow:
            print(terminal)
        print()

    def print_first(self):
        print('Firsts:')
        for terminal in self.first:
            print(terminal)
        print()

    def __str__(self):
        return f'<{self.value}>'
