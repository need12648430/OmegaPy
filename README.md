OmegaPy
=====
OmegaPy is a small but complete Python interface to Omegle.

 * Supports Classic, Interests, and Spy mode.
 * Simple programmable behavior using event handlers.
 * 2 simple usage demos - a Chatbot and a Man in the Middle attack.

Simple usage example:

    from Omegle import *
    
    class SimpleGreeter(OmegleHandler):
        def on_connect(self):
            print "y > hi!"
            self.omegle.send("hi!")
        
        def on_message(self, message):
            print "s > " + message
        
        def on_disconnect(self):
            self.omegle.start_chat(OmegleChat.Classic)
    
    greeter = SimpleGreeter()
    omegle = OmegleChat(greeter)
    omegle.start_chat(OmegleChat.Classic)

Spy mode:

    class QuestionDisplay(OmegleHandler):
        def on_connect(self):
            print "connected"
        
        def on_spy_question(self, question):
            print question
    
    question_dis = QuestionDisplay()
    omegle = OmegleChat(question_dis)
    omegle.start_chat(OmegleChat.Spy)

Interests mode:

    class InterestsDisplay(OmegleHandler):
        def on_connect(self):
            print "connected"
        
        # called when common interests were found
        def on_interests(self, interests):
            for i in interests:
                print i
    
    interests_dis = InterestsDisplay()
    omegle = OmegleChat(interests_dis)
    omegle.add_interests(["omegle", "github", "python", "beer"])
    omegle.start_chat(OmegleChat.Interests)