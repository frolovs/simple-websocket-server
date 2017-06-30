import re
from bots import *

class BotRouter(object):

    def __init__(self):
        self.__bots = {
            u'/wazup:': WazupBot()
        }

    def routeToBotAndGetResult(self, data):
        m = re.match("/.*:", data)
        if not m:
            return u''
        else:
            botName = m.group(0)
            if botName == u'/bots:':
                return u'\n' + u'bots list (commands): ' + str(self.__bots.keys())
            elif botName in self.__bots:
                bot = self.__bots[botName]
                return u'\n' + botName + u' ' + bot.runBot(data)
            else:
                return u''
