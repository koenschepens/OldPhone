import os
import sys
import ConfigParser
from Conversation.service import flow
from Conversation.service.flow.engines.context import Context

folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flow'))

from flow import actions
from flow import engines

config = ConfigParser.RawConfigParser()
includes_dir = folder + '/includes'
configFile = folder + '/conversation.config'

config.read(configFile)

def get_engine(type, context):
    import importlib
    engine = context.config.get("engines", type)
    class_name = ''.join(s[0].upper() + s[1:] for s in engine.split('_'))
    engine_class = getattr(importlib.import_module("Conversation.service.flow.engines.{0}.{1}".format(type,engine)), class_name)
    return engine_class

actionString = None
context = None

i = 0
for arg in sys.argv:
    print("arg: " + arg)
    if(arg == '-c'):
        contextString = sys.argv[i + 1]
        print("using context: " + contextString)
        context = get_engine("target", contextString)(folder)
    if(arg == '-a'):
        actionString = sys.argv[i + 1]
        print("using action: " + actionString)
    if(arg == '-e'):
        actionString = sys.argv[i + 1]
        print("execute: " + actionString)

    i = i + 1

if(context is None):
    tts_gender = config.get("tts", "gender")

    context = Context(config, folder, includes_dir, config.get("settings", "language"))

    context.sound_engine = get_engine("sound", context)(context)
    context.tts_engine = get_engine("tts", context)(context, config.get("tts", "gender"), context.language)
    context.target_engine = get_engine("target", context)(context)
    context.input_engine = get_engine("input", context)(context)
    context.personal_assistant = get_engine("personal_assistant", context)(context)
    language = config.get("settings", "language")

if(actionString is not None):
    result = context.Conversation.ask(actionString)
    context.state = actions.actionState(context)
    context.state.handle(result)
else:
    context.run()


