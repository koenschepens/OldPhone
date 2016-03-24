import sys

import abstract_state
import phoneDown
import phoneUp

reload(sys) 
sys.setdefaultencoding('UTF8')

class Initial(abstract_state.State):
    def __init__(self, context):
        self.Context = context

    def handle(self, result):
        pass