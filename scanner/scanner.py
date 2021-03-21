from .automata.exceptions import ReachedAcceptException, \
        InvalidInputException, InvalidNumberException, \
        UnmatchedCommentException, UnclosedCommentException
from .automata.dfa import DFA
from .storages import TokenStorage, ErrorStorage, SymbolTableStorage
from .buffer import UnreadableBuffer
from .token_type import TokenType
from . import config

class Scanner:
    def __init__(self):
        self.token_storage = TokenStorage()

        self.error_storage = ErrorStorage()

        self.symbol_table = SymbolTableStorage()
        self.symbol_table.load_keywords(config.KEYWORDS_FILE)

        self.buffer = UnreadableBuffer(config.INPUT_FILE)
        self.pending_str = []

        self.dfa = DFA.from_json_file(config.DFA_JSON_FILE)
        self.line_no = 1

    def dump_data(self):
        self.symbol_table.dump(config.SYMBOL_TABLE_FILE)
        self.error_storage.dump(config.LEXICAL_ERRORS_FILE)
        self.token_storage.dump(config.TOKENS_FILE)

    def get_next_token(self):
        self.dfa.reset()
        self.pending_str.clear()
        first_turn = True
        self.line_no = self.buffer.line_no
        while True:
            char = self.buffer.get()
            if char == '' and first_turn:
                self.dump_data()
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
                    token[0], _ = self.symbol_table.add_symbol(
                        self.get_pending_str(),
                    )

                self.token_storage.add_token(self.line_no, token)
                return token
            except InvalidInputException as e:
                self.handle_panic_mode(e.msg)
                return self.get_next_token()
            except UnclosedCommentException as e:
                current_str = self.get_pending_str(),
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
        self.error_storage.add_error(
            self.line_no,
            msg,
            self.get_pending_str(),
        )

    def get_pending_str(self):
        return ''.join(self.pending_str)

