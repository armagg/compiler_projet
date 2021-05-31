from anytree import RenderTree

from parser.cfgtools.grammar_builder import GrammarBuilder
from parser.storages import ErrorStorage
from parser.token_fifo import TokenFifo
from codegen.semantic_stack import SemanticStack
from codegen.symbol_table import SymbolTable
from codegen.program_block import ProgramBlock


class Parser:
    def __init__(self, scanner, grammar_file, tree_file, errors_file,
                 code_file):
        self.tree_file = tree_file
        self.errors_file = errors_file
        self.code_file = code_file
        self.tokens_fifo = TokenFifo(scanner)
        self.grammar = GrammarBuilder.from_file(grammar_file).build()
        self.error_storage = ErrorStorage()
        self.parse_tree = None
        self.grammar.calculate_parse_table()
        self.ss = SemanticStack()
        self.symtable = SymbolTable()
        self.pb = ProgramBlock()

    def run(self):
        self.parse_tree = self.grammar.start_nt.match(
            self.tokens_fifo,
            self.error_storage,
            self.ss,
            self.pb,
            self.symtable,
        )

    def dump_data(self):
        # self.error_storage.dump_data(self.errors_file)
        # self.render_parse_tree()
        self.generate_code()

    def render_parse_tree(self):
        f = open(self.tree_file, 'w')
        for pre, fill, node in RenderTree(self.parse_tree):
            f.write(f'{pre}{node.name}\n')
        f.close()

    def generate_code(self):
        with open(self.code_file, 'w') as f:
            f.write(str(self.pb))
