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
        self.file = open(file_name, 'r')
        self.eof = False
        self.line_no = 1

    def __del__(self):
        if self.file:
            self.file.close()

    def __fetch(self):
        if self.eof:
            return
        read_str = self.file.read(self.BLOCK_SIZE)
        if len(read_str) < self.BLOCK_SIZE:
            self.eof = True
        self.buffer += read_str

    def get(self):
        if len(self.buffer) == 0:
            self.__fetch()

        char = self.buffer.popleft() if len(self.buffer) else ''
        if char == '\n':
            self.line_no += 1
        return char

    def unread(self, char):
        self.buffer.appendleft(char)
        if char == '\n':
            self.line_no -= 1
