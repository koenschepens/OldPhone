import os
import sys
import ConfigParser

folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flow'))

from flow import actions
from flow import initial
from flow import contexts

config = ConfigParser.RawConfigParser()
includesDir = folder + '/includes'
configFile = folder + '/conversation.config'

config.read(configFile)

print (configFile)

availableContexts = {
            "context": contexts.Context,
            "kodiContext": contexts.KodiContext,
            "kodiRemoteContext": contexts.KodiRemoteContext,
        }

actionString = None

i = 0
for arg in sys.argv:
    print("arg: " + arg)
    if(arg == '-c'):
        contextString = sys.argv[i + 1]
        print("using context: " + contextString)
        context = availableContexts[contextString](folder)
    if(arg == '-a'):
        actionString = sys.argv[i + 1]
        print("using action: " + actionString)

    i = i + 1

if(context is None):
    context = availableContexts[config.get("flow", "context")](folder)

if(actionString is not None):
    result = context.Conversation.ask(actionString)
    context.State = actions.actionState(context)
    context.State.handle(result)
else:
    context.run()