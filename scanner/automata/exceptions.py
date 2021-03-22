class ReachedAcceptException(Exception):
    def __init__(self, state=None):
        super()
        self.state = state


class InvalidInputException(Exception):
    msg = 'Invalid input'

    def __init__(self, state=None):
        super()
        self.state = state


class InvalidNumberException(Exception):
    msg = 'Invalid number'

    def __init__(self, state=None):
        super()
        self.state = state


class UnmatchedCommentException(Exception):
    msg = 'Unmatched comment'

    def __init__(self, state=None):
        super()
        self.state = state


class UnclosedCommentException(Exception):
    msg = 'Unclosed comment'

    def __init__(self, state=None):
        super()
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

