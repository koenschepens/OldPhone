import conversation
import os

tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }
includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
language = 'dutch'

c = conversation.Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')
c.ask("play YouTube movie kittens")
