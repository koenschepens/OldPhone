import os
import resources.lib.includes.kodion.impl
from resources.lib.includes.kodion import runner
from resources.lib import startflow
import re
import sys

folder = os.path.dirname(os.path.realpath(__file__))
__provider__ = startflow.Provider(folder)

if(len(sys.argv) > 1):
    path = sys.argv[1]
else:
    path = "/context/initial/"

context = resources.lib.includes.kodion.impl.mock.mock_context.MockContext(path=path, params=None, plugin_name='MOCK Plugin', plugin_id='mock.plugin')

runner.run(__provider__, context)
#result = p.on_phone_picked_up_during_keyboard(context)
#print("result is: " + str(result))