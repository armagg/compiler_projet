from .automata.exceptions import ReachedAcceptException, \
        InvalidInputException, InvalidNumberException, \
        UnmatchedCommentException, UnclosedCommentException
from .automata.dfa import DFA
from .storages import TokenStorage, ErrorStorage, SymbolTableStorage
from .buffer import UnreadableBuffer
from .token_type import TokenType

class Scanner:
    def __init__(self, input_file, tokens_file, errors_file,
            symbols_file, dfa_file, keywords_file):
        self.tokens_file = tokens_file
        self.errors_file = errors_file
        self.symbols_file = symbols_file

        self.token_storage = TokenStorage()

        self.error_storage = ErrorStorage()

        self.symbol_table = SymbolTableStorage()
        self.symbol_table.load_keywords(keywords_file)

        self.buffer = UnreadableBuffer(input_file)
        self.pending_str = []

        self.dfa = DFA.from_json_file(dfa_file)
        self.line_no = 1

    def dump_data(self):
        self.symbol_table.dump(self.symbols_file)
        self.error_storage.dump(self.errors_file)
        self.token_storage.dump(self.tokens_file)

    def get_next_token(self):
        self.dfa.reset()
        self.pending_str.clear()
        first_turn = True
        self.line_no = self.buffer.line_no
        while True:
            char = self.buffer.get()
            if first_turn and char == '':
                return None
            self.pending_str += char

            try:
                self.dfa.scan(char)
                first_turn = False
            except ReachedAcceptException as e:
                if e.state.unread:
                    self.buffer.unread(self.pending_str.pop())
                token_type = e.state.token_type

                token = (token_type, self.get_pending_str())
                if token_type == TokenType.IDKEYWORD:
                    tmp = self.symbol_table.add_symbol(
                        self.get_pending_str(),
                    )
                    token = tmp[0], token[1]

                self.token_storage.add_token(self.line_no, token)
                return token
            except InvalidInputException as e:
                if e.state and e.state.unread:
                    self.buffer.unread(self.pending_str.pop())
                self.error_storage.add_error(
                    self.line_no,
                    self.get_pending_str(),
                    e.msg,
                )
                return self.get_next_token()
            except UnclosedCommentException as e:
                current_str = self.get_pending_str()
                if len(current_str) > 7:
                    current_str = current_str[:7] + '...'
                self.error_storage.add_error(
                    self.line_no,
                    current_str,
                    e.msg,
                )
                return self.get_next_token()
            except Exception as e:
                self.error_storage.add_error(
                    self.line_no,
                    self.get_pending_str(),
                    e.msg,
                )
                return self.get_next_token()

    def handle_panic_mode(self, msg):
        self.dfa.reset()
        while True:
            char = self.buffer.get()
            if not char:
                break
            if self.dfa.can_scan(char):
                self.buffer.unread(char)
                break
            self.pending_str.append(char)

    def get_pending_str(self):
        return ''.join(self.pending_str)

