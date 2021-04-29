"""
Members:
    Majid Garoosi   96109855
    Omid Mesgarha   96110645
"""
import sys

import config
from parser.parser import Parser
from scanner.scanner import Scanner

sys.setrecursionlimit(200)


def main():
    scanner = Scanner(
        dfa_file=config.DFA_JSON_FILE,
        keywords_file=config.KEYWORDS_FILE,

        input_file=config.INPUT_FILE,
        errors_file=config.LEXICAL_ERRORS_FILE,
        tokens_file=config.TOKENS_FILE,
        symbols_file=config.SYMBOL_TABLE_FILE,
    )

    parser = Parser(
        scanner=scanner,
        grammar_file=config.GRAMMAR_FILE,
        tree_file=config.TREE_FILE,
        errors_file=config.PARSER_ERRORS_FILE,
    )

    parser.run()
    parser.dump_data()

    # nt = parser.grammar.get_or_create_nonterminal('Declaration-list')
    # for key, rhs in nt.parse_table.items():
    #     print(key, rhs)

    # for nt in parser.grammar.non_terminals:
    #     print(nt.value)
    #     nt.print_follow()
    #     nt.print_first()
    # else:
    #     print('The end')


if __name__ == '__main__':
    exit(main())
