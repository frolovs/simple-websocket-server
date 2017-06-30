# IB sandbox with bots <br>learning TDD is fun
 
## What is it?
This is a simple/sample chat server which uses websockets transport.

The chat server can be extended with  bots.

Bots are located in ```bots``` directory.

## How to start server
run 
```bash
./run_chat_server.sh 
```

## How to run chat in a browser
1. run ```open SimpleWebSocketServer/websocket.html``` in a shell or open ```SimpleWebSocketServer/websocket.html``` in a browser
2. click button ```Connect```
3. can set a name by typing ```/name:MyCoolName``` in input text box and press ```Send```
4. can list bots by running ```/bots:``` in input text box and press ```Send```

## How to run tests
change directory to ```tests``` and run
```
nosetests -v
```

## How to add bots
1. All bots are classes in directory ```bots```.<br>
Look at example ```WazupBot.py``` - a bot. it has method ```runBot```<br>
which gets a string as input and should return a string
2. Create a bot class (for example ```MyCoolBot.py```) in directory ```bots```,<br>
create empty method ```runBot``` that returns 0
```python
class MyCoolBot(object):

    def runBot(self, data):
        return 0
```
3. Create a bot test (```testMyCoolBot.py```) in directory ```bots/tests```<br>
 and import the bot class from step 2
```python
from .. import MyCoolBot
from nose.tools import assert_equals

def testMyCoolBot():
    bot = MyCoolBot()
    result = bot.runBot(u'')
    assert_equals(u'This is my cool bot!', result)
```
4. Ensure that test fails (run tests)
5. Implement method ```runBot``` in your bot class ```MyCoolBot```
6. Run tests and ensure that they pass
7. Add your ```MyCoolBot``` to list of "know" bots:<br>
a) Modify ```bots/__init__.py``` class to include a new bot:
```python
from .WazupBot import WazupBot
from .MyCoolBot import MyCoolBot  <<<--- insert this line

__all__ = [
    "WazupBot"
    , "MyCoolBot"  <<<--- insert this line
]
```

b) Modify ```BotRouter.py``` class to include a new bot:

```python
import re
from bots import *

class BotRouter(object):

    def __init__(self):
        self.__bots = {
            u'/wazup:': WazupBot()
            ,u'/myCoolBot:': MyCoolBot() <<<--- Add this string starting with comma
        }
```
8. Restart chat server (to stop server - press CTRL + C)