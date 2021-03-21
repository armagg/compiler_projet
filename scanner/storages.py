from .token_type import TokenType
import config

class BaseStorage:
    def dump(self, file_name):
        raise Exception('Called abstract method')


class TokenStorage(BaseStorage):
    def __init__(self, conf=config.DEFAULT_TOKEN_STORAGE_CONFIG):
        self.tokens = dict()
        self.conf = conf

    def care_about(self, tok_type):
        return tok_type in self.conf['care_about']

    def add_token(self, line_no, token):
        if not self.care_about(token[0]):
            return
        if not self.tokens.get(line_no, None):
            self.tokens[line_no] = list()
        self.tokens[line_no].append(token)

    def dump(self, file_name):
        with open(file_name, 'w') as f:
            for line in sorted(self.tokens.keys()):
                rendered_tokens = list(map(
                    lambda token: f'({token[0]}, {token[1]})',
                    self.tokens.get(line),
                ))
                payload = ' '.join(rendered_tokens)
                f.write(f'{line}.\t{payload}\n')


class ErrorStorage(BaseStorage):
    def __init__(self):
        self.errors = dict()

    def add_error(self, line_no, lexeme, msg):
        if not self.errors.get(line_no, None):
            self.errors[line_no] = list()
        self.errors[line_no].append((lexeme, msg))

    def dump(self, file_name):
        with open(file_name, 'w') as f:
            if len(self.errors) == 0:
                f.write('There is no lexical error.')
                return
            for line in sorted(self.errors.keys()):
                rendered_errors = list(map(
                    lambda error: f'({error[0]}, {error[1]})',
                    self.errors.get(line),
                ))
                payload = ' '.join(rendered_errors)
                f.write(f'{line}.\t{payload}\n')


class SymbolTableStorage(BaseStorage):
    KEYWORDS_COUNT = 11

    def __init__(self):
        self.symbols = []

    def add_symbol(self, symbol):
        if symbol in self.symbols:
            index = self.symbols.index(symbol)
        else:
            index = len(self.symbols)
            self.symbols.append(symbol)

        if index < self.KEYWORDS_COUNT:
            token_type = TokenType.KEYWORD
        else:
            token_type = TokenType.ID

        return token_type, index + 1

    def load_keywords(self, file_name):
        with open(file_name, 'r') as f:
            for keyword in f.read().split():
                self.add_symbol(keyword)

    def dump(self, file_name):
        with open(file_name, 'w') as f:
            for idx, symbol in enumerate(self.symbols):
                f.write(f'{idx + 1}.\t{symbol}\n')

