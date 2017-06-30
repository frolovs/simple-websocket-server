'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import signal
import sys
import ssl
from BotRouter import BotRouter
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

class SimpleEcho(WebSocket):

   def handleMessage(self):
      self.sendMessage(self.data)

   def handleConnected(self):
      pass

   def handleClose(self):
      pass

clients = []
class SimpleChat(WebSocket):

   def __init__(self, server, sock, address):
      WebSocket.__init__(self, server, sock, address)
      self.botRouter = BotRouter()

   def handleMessage(self):
      self.__setUserNameConditionally()
      self.data += self.botRouter.activateBots(self.data)
      message = self.__getUserName() + u' - ' + self.data
      for client in clients:
         client.sendMessage(message)

   def handleConnected(self):
      print (self.address, 'connected')
      for client in clients:
         client.sendMessage(self.address[0] + u' - connected')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      for client in clients:
         client.sendMessage(self.address[0] + u' - disconnected')

   def __setUserNameConditionally(self):
      if self.data.startswith(u'/name:') and not hasattr(self, 'user_name'):
         self.user_name = self.data.replace(u'/name:', '')

   def __getUserName(self):
      if hasattr(self, 'user_name'):
         return self.user_name
      else:
         return self.address[0] + u':' + str(self.address[1])

if __name__ == "__main__":

   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   cls = SimpleEcho
   if options.example == 'chat':
      cls = SimpleChat

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

   signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
