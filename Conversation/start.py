import os
import sys
import ConfigParser
from service.flow.engines import context

folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flow'))

from service.flow import actions

config = ConfigParser.RawConfigParser()
includes_dir = folder + '/includes'
configFile = folder + '/settings.config'

config.read(configFile)

def get_engine(type, context):
    import importlib
    engine = context.config.get("engines", type)
    class_name = ''.join(s[0].upper() + s[1:] for s in engine.split('_'))
    engine_class = getattr(importlib.import_module("service.flow.engines.{0}.{1}".format(type,engine)), class_name)
    return engine_class

actionString = None
_context = None

i = 0
for arg in sys.argv:
    print("arg: " + arg)
    if(arg == '-c'):
        contextString = sys.argv[i + 1]
        print("using context: " + contextString)
        _context = get_engine("target", contextString)(folder)
    if(arg == '-a'):
        actionString = sys.argv[i + 1]
        print("using action: " + actionString)
    if(arg == '-e'):
        actionString = sys.argv[i + 1]
        print("execute: " + actionString)

    i = i + 1

if(_context is None):
    tts_gender = config.get("tts", "gender")

    _context = context.Context(config, folder, includes_dir, config.get("settings", "language"))

    _context.sound_engine = get_engine("sound", _context)(_context)
    _context.tts_engine = get_engine("tts", _context)(_context, config.get("tts", "gender"), _context.language)
    _context.target_engine = get_engine("target", _context)(_context)
    _context.input_engine = get_engine("input", _context)(_context)
    _context.personal_assistant = get_engine("personal_assistant", _context)(_context)
    language = config.get("settings", "language")

if(actionString is not None):
    result = _context.Conversation.ask(actionString)
    _context.state = actions.actionState(_context)
    _context.state.handle(result)
else:
    _context.run()


