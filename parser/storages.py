class ErrorStorage:
    def __init__(self):
        self.errors = list()

    def add_error(self, line_no, msg):
        self.errors.append((line_no, msg))

    def dump_data(self, file_address):
        with open(file_address, 'w') as f:
            if self.errors:
                for line_no, msg in self.errors:
                    f.write(f'#{line_no} : {msg}\n')
            else:
                f.write('There is no syntax error.\n')
