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
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = NeoTrans(domain='chatterbot', localedir=self.path, fallback=True, languages=[self.configuration_lisa['lang']]).Trans

    #-----------------------------------------------------------------------------
    def getTime(self, jsonInput):
        """
        Return time to user
        """
        # Get time
        now = datetime.now()
        
        # Round to 5 min
        h = now.hour
        m = int((((now.minute + now.second / 60.0 + 2.5) // 5) * 5) % 60)
        if m == 0 and now.minute > 50:
            h += 1
        
        # Inverted time
        h1 = h + 1
        m1 = 60 - m
        
        # Set message
        message = self._("time_{0}".format(m)).format(h = h, m = m, h1 = h1, m1 = m1)
        
        return {"plugin": __name__.split('.')[-1],
                "method": sys._getframe().f_code.co_name,
                "body": message
        }

    #-----------------------------------------------------------------------------
    def getDate(self, jsonInput):
        """
        Return date to user
        """
        # Get date
        now = datetime.now()
        
        # Round to 5 min
        wd = self._("day_{0}".format(now.weekday()))
        d = now.day
        m = self._("month_{0}".format(now.month))
        
        # Set message
        message = self._("date").format(wd = wd, d = d, m = m)
        
        return {"plugin": __name__.split('.')[-1],
                "method": sys._getframe().f_code.co_name,
                "body": message
        }

    #-----------------------------------------------------------------------------
    def sayHello(self, jsonInput):
        return {"plugin": __name__.split('.')[-1],
                "method": sys._getframe().f_code.co_name,
                "body": self._('Hello. How are you ?')
        }
