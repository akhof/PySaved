#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime

class Connector():
    def __init__(self, project):
        self.project = project
        
        self.finished = False
        self.error = False
        self.errormsg = None
        self.log = []
    
    def FINISH(self):
        self.finished = True
    
    def ERROR(self, msg=""):
        self.LOG(u"ERROR: {0}".format(msg))
        self.error = True
        self.errormsg = msg
    
    def LOG(self, msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append(u"{}   -   {}".format(timestamp, msg))