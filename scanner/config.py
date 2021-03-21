import os

BASE_DIR = './scanner'
KEYWORDS_FILE = os.path.join(BASE_DIR, 'keywords.txt')
INPUT_FILE = os.path.join(BASE_DIR, 'input.txt')
DFA_JSON_FILE = os.path.join(BASE_DIR, 'dfa.json')
SYMBOL_TABLE_FILE = os.path.join(BASE_DIR, 'symbol_table.txt')
LEXICAL_ERRORS_FILE = os.path.join(BASE_DIR, 'lexical_errors.txt')
TOKENS_FILE = os.path.join(BASE_DIR, 'tokens.txt')

