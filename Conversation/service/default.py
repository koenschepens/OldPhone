from resources.lib.includes.kodion import runner
from resources.lib import startflow
import os

folder = os.path.dirname(os.path.realpath(__file__))

__provider__ = startflow.Provider(folder)
runner.run(__provider__)
