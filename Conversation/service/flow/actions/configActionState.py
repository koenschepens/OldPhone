import re
import ConfigParser
import time
from service.flow import states
from service.flow.states.statebase import StateBase


class configActionState(StateBase):
    def __init__(self, context):
        StateBase.__init__(self, context)
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.context.root_folder + '/actions.config')
        self.context.log('actions config: ' + self.context.root_folder + '/actions.config')
    
    def handleDomainInit(self, domain):
        if(self.config.has_option(domain, "__init__")):
            self.context.send_action(self.config.get(domain, "__init__"))
            time.sleep(1)

    def handle(self, result):
        actionIdentifiers = result.Action.split('.')
        domain = actionIdentifiers[0]
        action = actionIdentifiers[1]

        if(not self.config.has_section(domain)):
            self.context.log("domain " + domain + " not found in config.")
            return False

        for option in self.config.options(domain):
            configAction = re.search('^' + action + '(\[(?P<var>\w*)\-\>(?P<val>\{?\w*\}?)\])?', option)
            if(configAction is not None):
                if(configAction.group('var')):
                    var = configAction.group('var')
                    val = configAction.group('val')

                    self.context.log("var: " + var)
                    self.context.log("value: " + val)
                    self.context.log("params: " + str(result.Parameters))

                    if(var in result.Parameters and result.Parameters[var] == val):
                        self.context.log("exact parameter match for " + option + ":" + self.config.get(domain, option))
                        self.handleDomainInit(domain)
                        self.context.send_action(self.config.get(domain, option))
                        return True
                    elif(var in result.Parameters):
                        self.context.log("free parameter match for " + option + ":" + self.config.get(domain, option))
                        if('{' in option):
                            command = re.sub('{(?P<parameter>\w*)}', lambda match: result.Parameters[match.group(1)], self.config.get(domain, option), flags=re.IGNORECASE)
                            self.context.log("command " + command)
                            self.handleDomainInit(domain)
                            self.context.send_action(command)
                            return True
                else:
                    self.context.log("lame match for " + option + ":" + self.config.get(domain, option))
                    self.handleDomainInit(domain)
                    self.context.send_action(self.config.get(domain, option))
                    return True
        return False