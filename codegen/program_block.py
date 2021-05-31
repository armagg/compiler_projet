class ProgramBlock(list):
    def __init__(self):
        super().__init__()

    def advance(self):
        self.append(None)
        return len(self) - 1

    @property
    def next_line(self):
        return len(self)

    def __str__(self):
        result = ''
        for idx, inst in enumerate(self):
            result += f'{idx}\t{inst}\n'
        return result
