class ReachedAcceptException(Exception):
    def __init__(self, state=None):
        super()
        self.state = state


class InvalidInputException(Exception):
    def __init__(self, state=None):
        super()
        self.msg = 'Invalid input'
        self.state = state


class InvalidNumberException(Exception):
    def __init__(self, state=None):
        super()
        self.msg = 'Invalid number'
        self.state = state


class UnmatchedCommentException(Exception):
    def __init__(self, state=None):
        super()
        self.msg = 'Unmatched comment'
        self.state = state


class UnclosedCommentException(Exception):
    def __init__(self, state=None):
        super()
        self.msg = 'Unclosed comment'
        self.state = state


def get_exception_by_name(name):
    if name == 'ACCEPT':
        return ReachedAcceptException
    if name == 'INVALID_INPUT':
        return InvalidInputException
    if name == 'UNMATCHED':
        return UnmatchedCommentException
    if name == 'UNCLOSED':
        return UnclosedCommentException
    if name == 'INVALID_NUMBER':
        return InvalidNumberException

