from anytree import RenderTree

from parser.cfgtools.grammar_builder import GrammarBuilder
from parser.storages import ErrorStorage
from parser.token_fifo import TokenFifo


class Parser:
    def __init__(self, scanner, grammar_file, tree_file, errors_file):
        self.tree_file = tree_file
        self.errors_file = errors_file
        self.tokens_fifo = TokenFifo(scanner)
        self.grammar = GrammarBuilder.from_file(grammar_file).build()
        self.error_storage = ErrorStorage()
        self.parse_tree = None
        self.grammar.calculate_parse_table()

    def run(self):
        self.parse_tree = self.grammar.start_nt.match(
            self.tokens_fifo,
            self.error_storage,
        )

    def dump_data(self):
        self.error_storage.dump_data(self.errors_file)
        self.render_parse_tree()

    def render_parse_tree(self):
        f = open(self.tree_file, 'w')
        for pre, fill, node in RenderTree(self.parse_tree):
            f.write(f'{pre}{node.name}\n')
        f.close()
