import urllib2 as url
import urllib
import httplib as http
import json
import time
from pprint import pprint

class OmegleHandler:
	def __init(self):
		""" creates an OmegleHandler """
		self.omegle = None
	
	def on_wait(self):
		""" called when a 'waiting' message is received """
		pass
	
	def on_interests(self, interests):
		""" called when common interests are found """
		pass
	
	def on_question(self, question):
		""" called when you receive the spy's question """
		pass
	
	def on_connect(self):
		""" called when the stranger connects """
		pass
	
	def on_disconnect(self):
		""" called when the stranger disconnects"""
		pass
	
	def on_message(self, message):
		""" called when a message is received from the stranger """
		pass
	
	def on_typing_start(self):
		""" called when the stranger starts typing """
		pass
	
	def on_typing_stop(self):
		""" called when the stranger starts typing """
		pass

class OmegleChat:
	Classic = "Classic"
	Spy = "Spy"
	Interests = "Interests"
	
	def __init__(self, handler = None):
		""" create an omegle chat instance """
		self.id = None
		self.handlers = []
		self.interests = []
		
		if not handler == None:
			self.add_handler(handler)
	
	def add_handler(self, omegle_handler):
		""" attach an omegle chat handler to this omegle instance """
		omegle_handler.omegle = self
		self.handlers.append(omegle_handler)
	
	def add_interest(self, interest):
		""" add an interest to the list of interests """
		self.interests.append(interest)
	
	def add_interests(self, interests):
		""" add a list of interests to the preexisting list of interests """
		for i in interests:
			self.interests.append(i)
	
	def get_topic_string(self):
		""" used internally. formats the interest list in a way omegle understands """
		if len(self.interests) > 0:
			return "topics=" + urllib.quote("[" + (",".join("\"" + i + "\"" for i in self.interests)) + "]")
		else:
			return ""
	
	def get_id(self, mode = "Classic"):
		""" fetches the stranger ID from omegle """
		if self.id == None:
			if mode == "Interests":
				start = url.urlopen("http://bajor.omegle.com/start?rcs=1&" + self.get_topic_string(), "")
			elif mode == "Spy":
				start = url.urlopen("http://bajor.omegle.com/start?rcs=1&wantsspy=1", "")
			else:
				start = url.urlopen("http://bajor.omegle.com/start?rcs=1", "")
			self.id = start.read()[1:-1]
		return self.id
	
	def disconnect(self):
		""" used internally. sends a "disconnect" message to the stranger. """
		encoded_data = urllib.urlencode({"id": self.get_id()})
		request = url.Request("http://bajor.omegle.com/disconnect", encoded_data)
		return url.urlopen(request).read()
	
	def start_typing(self):
		""" notifies the stranger that you've started typing. """
		encoded_data = urllib.urlencode({"id": self.get_id()})
		request = url.Request("http://bajor.omegle.com/typing", encoded_data)
		return url.urlopen(request).read()
	
	def stop_typing(self):
		""" notifies the stranger that you've stopped typing. """
		encoded_data = urllib.urlencode({"id": self.get_id()})
		request = url.Request("http://bajor.omegle.com/stoppedtyping", encoded_data)
		return url.urlopen(request).read()
	
	def send(self, message):
		""" sends a message to the stranger. """
		encoded_data = urllib.urlencode({"id": self.get_id(), "msg": message})
		request = url.Request("http://bajor.omegle.com/send", encoded_data)
		return url.urlopen(request).read()
	
	def start_chat(self, mode = "Classic"):
		""" starts a new omegle chat. """
		self.get_id(mode)
		self.listen()
	
	def stop_chat(self):
		""" stops the existing omegle chat. """
		self.disconnect()
		self.chatting = False
		self.id = None
	
	def listen(self):
		""" listens for omegle events and forwards them to all handlers. """
		encoded_data = urllib.urlencode({"id": self.get_id()})
		request = url.Request("http://bajor.omegle.com/events", encoded_data)
		chatting = True
		
		while chatting:
			response = url.urlopen(request)
			response_text = response.read()
			messages = json.loads(response_text)
			if not messages == None:
				for message in messages:
					if message[0] == "waiting":
						for h in self.handlers:
							h.on_wait()
					elif message[0] == "commonLikes":
						for h in self.handlers:
							h.on_interests(message[1])
					elif message[0] == "question":
						for h in self.handlers:
							h.on_question(message[1])
					elif message[0] == "connected":
						for h in self.handlers:
							h.on_connect()
					elif message[0] == "strangerDisconnected":
						chatting = False
						self.id = None
						for h in self.handlers:
							h.on_disconnect()
					elif message[0] == "typing":
						for h in self.handlers:
							h.on_typing_start()
					elif message[0] == "stoppedTyping":
						for h in self.handlers:
							h.on_typing_stop()
					elif message[0] == "gotMessage":
						for h in self.handlers:
							h.on_message(message[1])
			time.sleep(0.5)