# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
# project     : Lisa plugins
# module      : Chatterbot
# file        : chatterbot.py
# description : Chat with user
# author      : G.Dumee
#-----------------------------------------------------------------------------
# copyright   : Neotique
#-----------------------------------------------------------------------------

# TODO :


#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from datetime import datetime
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os, sys
from lisa.Neotique.NeoTrans import NeoTrans


#-----------------------------------------------------------------------------
# ChatterBot class
#-----------------------------------------------------------------------------
class ChatterBot(IPlugin):
    #-----------------------------------------------------------------------------
    def __init__(self):
        super(ChatterBot, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "ChatterBot"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], os.path.normpath("../lang/"))))
        self._ = NeoTrans(domain='chatterbot', localedir=self.path, fallback=True, languages=[self.configuration_lisa['lang']]).Trans

    #-----------------------------------------------------------------------------
    def getTime(self, jsonInput):
        """
        Return time to user
        """
        # Get context
        context = jsonInput['context']

        # Get time
        now = datetime.now()

        # Round to 5 min
        h = now.hour
        m = int((((now.minute + now.second / 60.0 + 2.5) // 5) * 5) % 60)
        if m == 0 and now.minute > 50:
            h += 1

        # Inverted time (ex: a quarter to five")
        h1 = h + 1
        m1 = 60 - m

        # Convert hour to string
        h_str = self._("hours_{0}".format(h)).format(h = h)
        if h_str == "hours_{0}".format(h):
            h_str = self._("hours").format(h = h)
        h1_str = self._("hours_{0}".format(h1)).format(h = h1)
        if h1_str == "hours_{0}".format(h1):
            h1_str = self._("hours").format(h = h1)

        # Set message
        message = self._("time_{0}".format(m)).format(h_str = h_str, m = m, h1_str = h1_str, m1 = m1)

        # Return message to client
        self.speakToClient(text = message, context = context)

    #-----------------------------------------------------------------------------
    def getDate(self, jsonInput):
        """
        Return date to user
        """
        # Get context
        context = jsonInput['context']

        # Get date
        now = datetime.now()

        # Round to 5 min
        wd = self._("day_{0}".format(now.weekday()))
        d = now.day
        m = self._("month_{0}".format(now.month))

        # Set message
        message = self._("date").format(wd = wd, d = d, m = m)

        # Return message to client
        self.speakToClient(text = message, context = context)

    #-----------------------------------------------------------------------------
    def sayHello(self, jsonInput):
        # Get context
        context = jsonInput['context']
        context.createClientVar(name = 'chatterbot_said_hello', default = False)
        context.createClientVar(name = 'chatterbot_got_how_are_you', default = False)
        context.createClientVar(name = 'chatterbot_said_status', default = False)
        message = ""

        # Get greetings
        try:
            # If assignemnt is valid, user is fine
            a = jsonInput['outcome']['entities']['chatterbot_greetings']
            message = "Bonjour, "
        except:
            pass

        # Ask for system state
        context.chatterbot_said_status = False
        try:
            # If assignemnt is valid, user is fine
            a = jsonInput['outcome']['entities']['chatterbot_ask_state']
            message += " " + "Je vais bien merci."
            context.chatterbot_said_status = True
        except:
            pass

        # Get if user is fine or not
        try:
            # If assignemnt is valid, user is fine
            a = jsonInput['outcome']['entities']['chatterbot_state_fine']
            context.chatterbot_got_how_are_you = True
            message += " " + "J'en suis ravie, c'est une bonne journée."
        except:
            try:
                # If assignemnt is valid, user is fine
                a = jsonInput['outcome']['entities']['chatterbot_state_not_fine']
                context.chatterbot_got_how_are_you = True
                message += " " + "J'espère que vous irez mieux."
            except:
                pass

        # Ask user if he's fine
        if context.chatterbot_got_how_are_you == False:
            if context.chatterbot_said_status == True:
                message += " " + "Et vous,"
            message += " " + "Comment allez vous ?"


            # Ask client if user is fine
            self.askClient(text = message, context = context, wit_context = {'state': "ask_how_are_you"}, answer_cbk = self._how_are_you_cbk)
        else:
            # Return message to client
            self.speakToClient(text = message, context = context)

    #-----------------------------------------------------------------------------
    def insult(self, jsonInput):
        # Get context
        context = jsonInput['context']

        #TODO
        message = "Veuillez rester poli s'il vous plait"

        # Return message to client
        self.speakToClient(text = message, context = context)

    #-----------------------------------------------------------------------------
    def _how_are_you_cbk(self, context, jsonAnswer):
        if jsonAnswer is None:
            return

        # Retry
        self.sayHello(jsonAnswer)

    #-----------------------------------------------------------------------------
    def get_name(self, jsonInput):
        # Get context
        context = jsonInput['context']

        #TODO
        message = "Mon nom est " + self.configuration_lisa['bot_name']

        # Return message to client
        self.speakToClient(text = message, context = context)

    #-----------------------------------------------------------------------------
    def get_user_name(self, jsonInput):
        # Get context
        context = jsonInput['context']

        #TODO
        message = "Votre nom est maître"

        # Return message to client
        self.speakToClient(text = message, context = context)


# --------------------- End of chatterbot.py  ---------------------
