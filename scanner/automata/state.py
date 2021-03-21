class State:
    def __init__(self, unread, token_type, exception_class):
        self.tarnsitions = list()
        self.unread = unread
        self.token_type = token_type
        self.exception_class = exception_class

    def add_transition(self, chars, dest):
        self.transitions.append((chars, dest))

    def transit(self, char):
        for chars, dest in self.transitions:
            if char in chars:
                return dest
        return None

    def raise_exception(self):
        if self.exception_class:
            raise self.exception_class(self)

