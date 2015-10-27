import resources.lib.flow.contexts

class State:
    def __init__(self, context):
        self.Context = context

    def __call__(self, context):
        self.Context.log("Calling state")

    def handle(self, context):
        pass