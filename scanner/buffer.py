import collections

class UnreadableBuffer:
    """
    Note that it's not an unreadable buffer; This is a buffer with
    the support of "unread"ing a character. Refer to the slides for
    more info.
    """

    BLOCK_SIZE = 16

    def __init__(self, file_name):
        self.buffer = collections.deque()
        self.file = open('file_name', 'r')
        self.eof = False

    def __del__(self):
        if self.file:
            self.file.close()

    def __fetch(self):
        if self.eof:
            return
        self.buffer += self.file.read(BLOCK_SIZE)

    def get():
        if len(self.buffer) == 0:
            self.__fetch()
        return self.buffer.popleft() if len(self.buffer) else ''

    def unread(char):
        self.buffer.appendleft(char)

