class AbstractService:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        raise NotImplementedError('`execute()` method must be implemented in your derived class')

