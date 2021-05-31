from anytree import Node

from parser.cfgtools.grammar_element import GrammarElement
from scanner.token_type import TokenType


class Terminal(GrammarElement):
    Epsilon = None
    Mapping = dict()

    @staticmethod
    def get_instance(elem_str):
        if Terminal.Mapping.get(elem_str) is None:
            arr = elem_str.split('_')[1:]
            if len(arr) == 1:
                Terminal.Mapping[elem_str] = Terminal(arr[0], None)
            else:
                Terminal.Mapping[elem_str] = Terminal(arr[0], arr[1])
        return Terminal.Mapping.get(elem_str)

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.first = {self}

    def is_terminal(self):
        return True

    @property
    def missing_name(self):
        if self.value:
            return self.value
        else:
            return self.name

    def matches_token(self, token):
        if self.name == Terminal.Epsilon.name:
            return True
        elif self.name in [TokenType.NUM, TokenType.ID, TokenType.EOF]:
            return token[0] == self.name
        else:
            return token == (self.name, self.value)

    def match(self, tokens, errors, ss, pb, symbol_table):
        lookahead = tokens.lookahead
        if lookahead is None:
            return None
        # print('matching', self.name, self.value, lookahead)

        if self.name == Terminal.Epsilon.name:
            return Node('epsilon')
        elif self.name == TokenType.EOF:
            if lookahead[0] == self.name:
                tokens.advance()
                return Node(lookahead[1])
            else:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, missing {self.missing_name}'
                )
        elif self.name in [TokenType.NUM, TokenType.ID]:
            if lookahead[0] == self.name:
                tokens.advance()
                return Node(f'({lookahead[0]}, {lookahead[1]})')
            else:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, missing {self.missing_name}'
                )
        else:
            if lookahead == (self.name, self.value):
                tokens.advance()
                return Node(f'({lookahead[0]}, {lookahead[1]})')
            else:
                errors.add_error(
                    tokens.line_no,
                    f'syntax error, missing {self.missing_name}'
                )
        return None

    def can_empty(self):
        return self is Terminal.Epsilon

    def __str__(self):
        return f'({self.name}, {self.value})'


Terminal.Epsilon = Terminal('epsilon', 'epsilon')
