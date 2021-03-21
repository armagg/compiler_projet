"""
Members:
    Majid Garoosi   96109855
    Omid Mesgarha   TODO
"""
import config
from scanner.scanner import Scanner

def main():
    scanner = Scanner(
        dfa_file=config.DFA_JSON_FILE,
        keywords_file=config.KEYWORDS_FILE,

        input_file=config.INPUT_FILE,
        errors_file=config.LEXICAL_ERRORS_FILE,
        tokens_file=config.TOKENS_FILE,
        symbols_file=config.SYMBOL_TABLE_FILE,
    )

    while scanner.get_next_token():
        pass
    scanner.dump_data()

if __name__ == '__main__':
    exit(main())
