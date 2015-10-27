import contexts

class State:
    def __init__(self, context):
        self.Context = context

    def handle(self, context):
        pass