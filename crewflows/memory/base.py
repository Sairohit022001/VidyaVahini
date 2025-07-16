class BaseMemoryHandler:
    def load(self):
        raise NotImplementedError

    def save(self, data):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError
