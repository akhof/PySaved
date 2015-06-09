#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tempfile, base64, cPickle, os, sys, platform

class Project():
    def __init__(self):
        self.name = u""
        self.icon = u""
        self.execfile = u""
        self.console = True
        self.pathstosearchin = []
        self.allhiddenmodules = []
        self.hiddenmodules = []
        self.outpath = unicode(os.environ['HOME']) if platform.system() == "Linux" else unicode(os.getenv("USERPROFILE"))
        self.temppath = unicode(os.path.join(tempfile.gettempdir(), "PySaved"))
        self.saveasfile = False
        self.debug = False
        self.unicode = True
        
        for basepath in sys.path:
            if basepath not in self.pathstosearchin:
                self.pathstosearchin.append(unicode(basepath))
    
        self.__lastsaved = None
        self.__keys = ["name", "icon", "execfile", "console", "pathstosearchin", "hiddenmodules", "outpath", "temppath", "saveasfile", "debug", "unicode"]
    
    def load(self, frame, path):
        f = open(path, "r")
        serial = f.read()
        f.close()
        
        self.__unserial(serial)
        self.loadAllhiddenmodules(frame)
        self.__lastsaved = serial
        self.__loadFromProjectIntoFrame(frame)
        
    def save(self, frame, path):
        self.__loadFromFrameIntoProject(frame)
        self.__lastsaved = self.__serial()
        
        f = open(path, "w")
        f.write(self.__lastsaved)
        f.close()

    def loadAllhiddenmodules(self, frame):
        mods = []
        for basepath in self.pathstosearchin:
            if basepath not in self.pathstosearchin: self.pathstosearchin.append(unicode(basepath))
            
            if len(basepath.strip()) == 0: continue
            if not os.path.isdir(basepath): continue
            for path in os.listdir(basepath):
                if os.path.isfile(os.path.join(basepath, path)):
                    if ".py" in path:
                        mods.append(path.split(".py")[0])
                elif os.path.isdir(os.path.join(basepath, path)):
                    if "__init__.py" in os.listdir(os.path.join(basepath, path)):
                        mods.append(path)
        self.allhiddenmodules = []
        for m in mods:
            try:
                if not m in self.allhiddenmodules and not "_" == m[0]:
                    self.allhiddenmodules.append(unicode(m))
            except: pass
        self.__loadFromProjectIntoFrame(frame)

    def initialFrame(self, frame):
        self.__loadFromProjectIntoFrame(frame)
    def loadFromFrame(self, frame):
        self.__loadFromFrameIntoProject(frame)

    def needSave(self, frame):
        return  self.__lastsaved != self.__serial() 
    
    def isEmpty(self, frame):
        self.__loadFromFrameIntoProject(frame)
        
        return self.__serial() == Project().__serial()
    
    def __loadFromProjectIntoFrame(self, frame):
        frame.input_name.SetValue(self.name)
        frame.input_icon.SetValue(self.icon)
        frame.input_execfile.SetValue(self.execfile)
        frame.radiobox_console.SetSelection(int(not self.console))
        frame.input_outpath.SetValue(self.outpath)
        frame.input_temppath.SetValue(self.temppath)
        frame.radiobox_saveas.SetSelection(int(self.saveasfile))
        frame.checkbox_debug.SetValue(self.debug)
        frame.checkbox_unicode.SetValue(self.unicode)
        
        frame.list_pathstosearchin.SetItems(self.pathstosearchin)
        frame.list_hiddenmodules.SetItems(self.allhiddenmodules)
        frame.list_hiddenmodules.SetCheckedStrings(self.hiddenmodules)
        
    def __loadFromFrameIntoProject(self, frame):
        self.name = unicode(frame.input_name.GetValue().strip())
        self.icon = unicode(frame.input_icon.GetValue().strip())
        self.execfile = unicode(frame.input_execfile.GetValue().strip())
        self.console = not frame.radiobox_console.GetSelection()
        self.outpath = unicode(frame.input_outpath.GetValue().strip())
        self.temppath = unicode(frame.input_temppath.GetValue().strip())
        self.saveasfile = bool(frame.radiobox_saveas.GetSelection())
        self.debug = frame.checkbox_debug.GetValue()
        self.unicode = frame.checkbox_unicode.GetValue()
        
        self.pathstosearchin = frame.list_pathstosearchin.GetItems()
        self.allhiddenmodules = frame.list_hiddenmodules.GetItems()
        self.hiddenmodules = list(frame.list_hiddenmodules.GetCheckedStrings())
    
    def __serial(self):
        o = {}
        for key in self.__keys:
            o[key] = eval("self." + key)
        
        return base64.b64encode( cPickle.dumps( o ) )
        
    def __unserial(self, serial):
        o = cPickle.loads( base64.b64decode( serial ) )
        
        for key in o.keys():
            cmd = "self.{0} = o[\"{0}\"]".format(key)
            exec(cmd)