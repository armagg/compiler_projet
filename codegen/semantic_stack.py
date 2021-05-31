class SemanticStack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)
        # print(self.stack)

    def pop(self, cnt):
        for _ in range(cnt):
            self.stack.pop()
        # print(self.stack)

    def __getitem__(self, item):
        return self.stack[-item - 1]

    def __setitem__(self, item, value):
        self.stack[-item - 1] = value
        # print(self.stack)
