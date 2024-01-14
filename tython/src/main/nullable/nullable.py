class Nullable(None):
    def __init__(self, contained):
        self.contained = contained

    def __getitem__(self, item):
        return Nullable(item)
