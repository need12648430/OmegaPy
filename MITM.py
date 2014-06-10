"""
	demo: simple man in the middle attack
	connects with 2 strangers and relays messages/statuses between them
"""

from Omegle import *
import time
import thread

class ManInTheMiddle(OmegleHandler):
	def __init__(self):
		self.name = "Anon"
		self.other = None
	
	def set_stranger(self, name, stranger):
		self.name = name
		self.other = stranger
	
	def on_connect(self):
		print self.other.name + " connected"
		
	def on_typing_start(self):
		print self.name + " is typing..."
		self.other.omegle.start_typing()
		
	def on_typing_stop(self):
		print self.name + " stopped typing."
		self.other.omegle.stop_typing()
		
	def on_message(self, m):
		print self.name + " > " + m
		self.other.omegle.send(m)
	
	def on_disconnect(self):
		print self.name + " disconnected"
		self.omegle.stop_chat()
		self.other.omegle.stop_chat()


# create 2 ManInTheMiddle handlers - one for each stranger
strangerAhandler = ManInTheMiddle()
strangerBhandler = ManInTheMiddle()

# point them to each-other
strangerAhandler.set_stranger("A", strangerBhandler)
strangerBhandler.set_stranger("B", strangerAhandler)

# create 2 OmegleChats, one for each handler
omegleA = OmegleChat(strangerAhandler)
omegleB = OmegleChat(strangerBhandler)

# start both chats in their own thread so they can listen for messages
thread.start_new_thread(omegleA.start_chat, (OmegleChat.Classic, ))
thread.start_new_thread(omegleB.start_chat, (OmegleChat.Classic, ))

# loop to keep the script running while they chat, sleep for the sake of your CPU
while True:
	time.sleep(1)