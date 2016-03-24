from flow import state
import flow.state
import flow.contexts
import re
import flow.actions
import conversation
import ConfigParser
import time

class configActionState(state.State):
    def __init__(self, context):
        state.State.__init__(self, context)

        self.Config = ConfigParser.SafeConfigParser()
        self.Config.read(self.Context.RootFolder + '/actions.config')
        self.Context.log('actions config: ' + self.Context.RootFolder + '/actions.config')
    
    def handleDomainInit(self, domain):
        if(self.Config.has_option(domain, "__init__")):
            self.Context.send_action(self.Config.get(domain, "__init__"))
            time.sleep(1)

    def handle(self, result):
        actionIdentifiers = result.Action.split('.')
        domain = actionIdentifiers[0]
        action = actionIdentifiers[1]

        if(not self.Config.has_section(domain)):
            self.Context.log("domain " + domain + " not found in config.")
            return False

        for option in self.Config.options(domain):
            configAction = re.search('^' + action + '(\[(?P<var>\w*)\-\>(?P<val>\{?\w*\}?)\])?', option)
            if(configAction is not None):
                if(configAction.group('var')):
                    var = configAction.group('var')
                    val = configAction.group('val')

                    self.Context.log("var: " + var)
                    self.Context.log("value: " + val)
                    self.Context.log("params: " + str(result.Parameters))

                    if(var in result.Parameters and result.Parameters[var] == val):
                        self.Context.log("exact parameter match for " + option + ":" + self.Config.get(domain, option))
                        self.handleDomainInit(domain)
                        self.Context.send_action(self.Config.get(domain, option))
                        return True
                    elif(var in result.Parameters):
                        self.Context.log("free parameter match for " + option + ":" + self.Config.get(domain, option))
                        if('{' in option):
                            command = re.sub('{(?P<parameter>\w*)}', lambda match: result.Parameters[match.group(1)], self.Config.get(domain, option), flags=re.IGNORECASE)
                            self.Context.log("command " + command)
                            self.handleDomainInit(domain)
                            self.Context.send_action(command)
                            return True
                else:
                    self.Context.log("lame match for " + option + ":" + self.Config.get(domain, option))
                    self.handleDomainInit(domain)
                    self.Context.send_action(self.Config.get(domain, option))
                    return True
        return False