from .. import WazupBot
from nose.tools import assert_equals

def testWazupBot():
    bot = WazupBot()
    result = bot.runBot(u'')
    assert_equals(u'Wazup!', result)
