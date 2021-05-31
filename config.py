import os

from scanner.token_type import TokenType

BASE_DIR = '.'

INPUT_FILE = os.path.join(BASE_DIR, 'input.txt')
SYMBOL_TABLE_FILE = os.path.join(BASE_DIR, 'symbol_table.txt')
LEXICAL_ERRORS_FILE = os.path.join(BASE_DIR, 'lexical_errors.txt')
TOKENS_FILE = os.path.join(BASE_DIR, 'tokens.txt')

SCANNER_DIR = os.path.join(BASE_DIR, 'scanner')
LSD_DIR = os.path.join(BASE_DIR, 'lsd')
DFA_JSON_FILE = os.path.join(LSD_DIR, 'dfa.json')
KEYWORDS_FILE = os.path.join(LSD_DIR, 'keywords.txt')

GRAMMAR_FILE = os.path.join(LSD_DIR, 'grammar.txt')
TREE_FILE = os.path.join(BASE_DIR, 'parse_tree.txt')
PARSER_ERRORS_FILE = os.path.join(BASE_DIR, 'syntax_errors.txt')

INTERMEDIATE_CODE_FILE = 'output.txt'

DEFAULT_TOKEN_STORAGE_CONFIG = {
    "care_about": [
        TokenType.ID,
        TokenType.KEYWORD,
        TokenType.NUM,
        TokenType.SYMBOL,
        TokenType.EOF,
    ],
}
