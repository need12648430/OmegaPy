"""
	demo: simple chatbot
	connects with a stranger greeting them with "hi, i'm a chatbot"
	then proceeds to echo all messages sent to it
"""

from Omegle import *
import time

class SimpleChatbot(OmegleHandler):
	def on_connect(self):
		print "stranger connected"
		greeting = "hi, i'm a chatbot"
		self.omegle.send(greeting)
		print "y > " + greeting
	
	def on_typing_start(self):
		print "stranger is typing..."
	
	def on_typing_stop(self):
		print "stranger stopped typing."
	
	def on_message(self, message):
		print "s > " + message
		
		# pretend to type for 1 second to look real
		self.omegle.start_typing()
		time.sleep(1)
		# send message
		self.omegle.send(message)
		# tell omegle we're done "typing"
		self.omegle.stop_typing()
		
		print "y > " + message
	
	def on_disconnect(self):
		print "stranger disconnected, next please"
		self.omegle.start_chat(OmegleChat.Classic)

chatbot = SimpleChatbot()
omegle = OmegleChat(chatbot)
omegle.start_chat(OmegleChat.Classic)