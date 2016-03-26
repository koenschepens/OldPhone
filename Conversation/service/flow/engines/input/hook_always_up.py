from service.flow.engines.input.console import Console

class HookAlwaysUp(Console):
    def isUp(self):
        return True