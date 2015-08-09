#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx, sys, thread, time, os
import statics, builder
from Project import Project

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.menubar = wx.MenuBar()
        self.menu_file = wx.Menu()
        self.menu_new = wx.MenuItem(self.menu_file, 101, "&New", "", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_new)
        self.menu_open = wx.MenuItem(self.menu_file, 102, "&Open", "", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_open)
        self.menu_save = wx.MenuItem(self.menu_file, 103, "&Save", "", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_save)
        self.menu_saveas = wx.MenuItem(self.menu_file, 104, "Save &As", "", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_saveas)
        self.menu_file.AppendSeparator()
        self.menu_close = wx.MenuItem(self.menu_file, 105, "&Close", "", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_close)
        self.menubar.Append(self.menu_file, "&File")
        self.menu_about = wx.Menu()
        self.menu_about_pysaved = wx.MenuItem(self.menu_about, 201, "&About PySaved", "", wx.ITEM_NORMAL)
        self.menu_about.AppendItem(self.menu_about_pysaved)
        self.menubar.Append(self.menu_about, "&About")
        self.SetMenuBar(self.menubar)
        
        self.nb = wx.Notebook(self, wx.ID_ANY, style=0)
        self.nb_panel_1 = wx.Panel(self.nb, wx.ID_ANY)
        self.label_name = wx.StaticText(self.nb_panel_1, wx.ID_ANY, "Name:")
        self.input_name = wx.TextCtrl(self.nb_panel_1, wx.ID_ANY, "")
        self.label_icon = wx.StaticText(self.nb_panel_1, wx.ID_ANY, "Icon (Windows only):")
        self.input_icon = wx.TextCtrl(self.nb_panel_1, wx.ID_ANY, "")
        self.button_search_icon = wx.BitmapButton(self.nb_panel_1, wx.ID_ANY, statics.search(), style=wx.NO_BORDER)
        self.label_execfile = wx.StaticText(self.nb_panel_1, wx.ID_ANY, "Executable file:")
        self.input_execfile = wx.TextCtrl(self.nb_panel_1, wx.ID_ANY, "")
        self.button_search_execfile = wx.BitmapButton(self.nb_panel_1, wx.ID_ANY, statics.search(), style=wx.NO_BORDER)
        self.radiobox_console = wx.RadioBox(self.nb_panel_1, wx.ID_ANY, "Console (Windows only)", choices=["show", "hide"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
        self.sl1 = wx.StaticLine(self.nb_panel_1, wx.ID_ANY)
        self.label_pathstosearchin = wx.StaticText(self.nb_panel_1, wx.ID_ANY, "Paths to search in:")
        self.list_pathstosearchin = wx.ListBox(self.nb_panel_1, wx.ID_ANY, choices=[])
        self.button_pathstosearchin_add = wx.BitmapButton(self.nb_panel_1, wx.ID_ANY, statics.add(), style=wx.NO_BORDER)
        self.button_pathstosearchin_edit = wx.BitmapButton(self.nb_panel_1, wx.ID_ANY, statics.edit(), style=wx.NO_BORDER)
        self.button_pathstosearchin_del = wx.BitmapButton(self.nb_panel_1, wx.ID_ANY, statics.dele(), style=wx.NO_BORDER)
        self.label_hiddenmodules = wx.StaticText(self.nb_panel_1, wx.ID_ANY, "Hidden modules:")
        self.list_hiddenmodules = wx.CheckListBox(self.nb_panel_1, wx.ID_ANY, choices=[])
        self.nb_pane_2 = wx.Panel(self.nb, wx.ID_ANY)
        self.label_outpath = wx.StaticText(self.nb_pane_2, wx.ID_ANY, "Output path:")
        self.input_outpath = wx.TextCtrl(self.nb_pane_2, wx.ID_ANY, "")
        self.search_outpath = wx.BitmapButton(self.nb_pane_2, wx.ID_ANY, statics.search(), style=wx.NO_BORDER)
        self.label_temppath = wx.StaticText(self.nb_pane_2, wx.ID_ANY, "Temporary path:")
        self.input_temppath = wx.TextCtrl(self.nb_pane_2, wx.ID_ANY, "")
        self.search_temppath = wx.BitmapButton(self.nb_pane_2, wx.ID_ANY, statics.search(), style=wx.NO_BORDER)
        self.sl2 = wx.StaticLine(self.nb_pane_2, wx.ID_ANY)
        self.radiobox_saveas = wx.RadioBox(self.nb_pane_2, wx.ID_ANY, "Save as", choices=["multiple files in one folder", "one file"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
        self.checkbox_debug = wx.CheckBox(self.nb_pane_2, wx.ID_ANY, "Debug-mode")
        self.checkbox_unicode = wx.CheckBox(self.nb_pane_2, wx.ID_ANY, "Support unicode")
        self.sl3 = wx.StaticLine(self.nb_pane_2, wx.ID_ANY)
        self.bitmap_start = wx.BitmapButton(self.nb_pane_2, wx.ID_ANY, statics.start(), style=wx.NO_BORDER)
        self.sl4 = wx.StaticLine(self.nb_pane_2, wx.ID_ANY)
        self.label_log = wx.StaticText(self.nb_pane_2, wx.ID_ANY, "Log:")
        self.list_log = wx.ListBox(self.nb_pane_2, wx.ID_ANY, choices=[])

        self.Bind(wx.EVT_MENU, self.new, self.menu_new)
        self.Bind(wx.EVT_MENU, self.open, self.menu_open)
        self.Bind(wx.EVT_MENU, self.save, self.menu_save)
        self.Bind(wx.EVT_MENU, self.saveas, self.menu_saveas)
        self.Bind(wx.EVT_MENU, self.exit, self.menu_close)
        self.Bind(wx.EVT_MENU, self.about, self.menu_about_pysaved)
        self.Bind(wx.EVT_BUTTON, self.search_icon, self.button_search_icon)
        self.Bind(wx.EVT_BUTTON, self.search_execfile, self.button_search_execfile)
        self.Bind(wx.EVT_BUTTON, self.addPath, self.button_pathstosearchin_add)
        self.Bind(wx.EVT_BUTTON, self.editPath, self.button_pathstosearchin_edit)
        self.Bind(wx.EVT_BUTTON, self.delPath, self.button_pathstosearchin_del)
        self.Bind(wx.EVT_BUTTON, self.event_search_outpath, self.search_outpath)
        self.Bind(wx.EVT_BUTTON, self.event_search_temppath, self.search_temppath)
        self.Bind(wx.EVT_BUTTON, self.start, self.bitmap_start)
        self.Bind(wx.EVT_CLOSE, self.exit)

        self.__set_properties()
        self.__do_layout()

        self.project = Project()
        self.project.loadAllhiddenmodules(self)
        self.project.initialFrame(self)
        self.path = None
        self.progress= False
        
    def __set_properties(self):
        self.SetTitle("PySaved")
        self.SetMinSize(wx.Size(780, 820))
        self.label_name.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.input_name.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_icon.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.input_icon.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_search_icon.SetSize(self.button_search_icon.GetBestSize())
        self.label_execfile.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.input_execfile.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_search_execfile.SetSize(self.button_search_execfile.GetBestSize())
        self.radiobox_console.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.radiobox_console.SetSelection(0)
        self.label_pathstosearchin.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.list_pathstosearchin.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.list_pathstosearchin.SetSelection(0)
        self.button_pathstosearchin_add.SetSize(self.button_pathstosearchin_add.GetBestSize())
        self.button_pathstosearchin_edit.SetSize(self.button_pathstosearchin_edit.GetBestSize())
        self.button_pathstosearchin_del.SetSize(self.button_pathstosearchin_del.GetBestSize())
        self.label_hiddenmodules.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.list_hiddenmodules.SetSelection(0)
        self.label_outpath.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.input_outpath.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.search_outpath.SetSize(self.search_outpath.GetBestSize())
        self.label_temppath.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.input_temppath.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.search_temppath.SetSize(self.search_temppath.GetBestSize())
        self.radiobox_saveas.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.radiobox_saveas.SetSelection(0)
        self.checkbox_debug.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.checkbox_unicode.SetValue(1)
        self.bitmap_start.SetSize(self.bitmap_start.GetBestSize())
        self.label_log.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.list_log.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.list_log.SetSelection(0)

    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(3, 3, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(9, 1, 10, 0)
        grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 10)
        grid_sizer_3 = wx.FlexGridSizer(2, 3, 15, 15)
        grid_sizer_5 = wx.FlexGridSizer(4, 1, 15, 0)
        grid_sizer_7 = wx.FlexGridSizer(2, 3, 15, 15)
        grid_sizer_8 = wx.FlexGridSizer(3, 1, 5, 0)
        grid_sizer_6 = wx.FlexGridSizer(3, 3, 10, 10)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        grid_sizer_6.Add(self.label_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.input_name, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add((10, 30), 0, 0, 0)
        grid_sizer_6.Add(self.label_icon, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.input_icon, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.button_search_icon, 0, 0, 0)
        grid_sizer_6.Add(self.label_execfile, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.input_execfile, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self.button_search_execfile, 0, 0, 0)
        grid_sizer_6.AddGrowableCol(1)
        grid_sizer_5.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_5.Add(self.radiobox_console, 0, 0, 0)
        grid_sizer_5.Add(self.sl1, 0, wx.EXPAND, 0)
        grid_sizer_7.Add(self.label_pathstosearchin, 0, 0, 0)
        grid_sizer_7.Add(self.list_pathstosearchin, 0, wx.EXPAND, 0)
        grid_sizer_8.Add(self.button_pathstosearchin_add, 0, 0, 0)
        grid_sizer_8.Add(self.button_pathstosearchin_edit, 0, 0, 0)
        grid_sizer_8.Add(self.button_pathstosearchin_del, 0, 0, 0)
        grid_sizer_7.Add(grid_sizer_8, 1, wx.EXPAND, 0)
        grid_sizer_7.Add(self.label_hiddenmodules, 0, 0, 0)
        grid_sizer_7.Add(self.list_hiddenmodules, 0, wx.EXPAND, 0)
        grid_sizer_7.Add((20, 20), 0, 0, 0)
        grid_sizer_7.AddGrowableRow(0)
        grid_sizer_7.AddGrowableRow(1)
        grid_sizer_7.AddGrowableCol(1)
        grid_sizer_5.Add(grid_sizer_7, 1, wx.EXPAND, 0)
        self.nb_panel_1.SetSizer(grid_sizer_5)
        grid_sizer_5.AddGrowableRow(3)
        grid_sizer_5.AddGrowableCol(0)
        grid_sizer_3.Add(self.label_outpath, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.input_outpath, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.search_outpath, 0, 0, 0)
        grid_sizer_3.Add(self.label_temppath, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.input_temppath, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.search_temppath, 0, 0, 0)
        grid_sizer_3.AddGrowableCol(1)
        grid_sizer_2.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.sl2, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.radiobox_saveas, 0, 0, 0)
        grid_sizer_4.Add(self.checkbox_debug, 0, 0, 0)
        grid_sizer_4.Add(self.checkbox_unicode, 0, 0, 0)
        grid_sizer_2.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.sl3, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.bitmap_start, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_2.Add(self.sl4, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_log, 0, 0, 0)
        grid_sizer_2.Add(self.list_log, 0, wx.EXPAND, 0)
        self.nb_pane_2.SetSizer(grid_sizer_2)
        grid_sizer_2.AddGrowableRow(8)
        grid_sizer_2.AddGrowableCol(0)
        self.nb.AddPage(self.nb_panel_1, "Project")
        self.nb.AddPage(self.nb_pane_2, "Build")
        main_sizer.Add(self.nb, 1, wx.EXPAND, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        main_sizer.Add((20, 20), 0, 0, 0)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        main_sizer.AddGrowableRow(1)
        main_sizer.AddGrowableCol(1)
        self.Layout()

    def askForSavingIfNeed(self):
        if (self.path == None or self.project.needSave(self)) and not self.project.isEmpty(self):
            res = wx.MessageDialog(self, "Do you want to save this project?", "Save?", wx.ICON_QUESTION | wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT).ShowModal()
            
            if res == wx.ID_CANCEL:
                return False
            elif res == wx.ID_YES:
                self.save(None)
        return True
    
    def new(self, event):
        if self.askForSavingIfNeed():
            self.project = Project()
            self.project.loadAllhiddenmodules(self)
            self.project.initialFrame(self)
            self.path = None

    def open(self, event=None, path=None):
        if self.askForSavingIfNeed():
            if path == None:
                dia = wx.FileDialog(self, "Select a file to open", wildcard="PySaved-files (*.pysa)|*.pysa", style=wx.FD_OPEN)
                if dia.ShowModal() == wx.ID_OK:
                    path = dia.GetPath()
                else: return

            try:
                print(u"Loading project from: '{0}'".format(path))                
                p = Project()
                p.load(self, path)
                self.project = p
                self.project.loadAllhiddenmodules(self)
                self.path = path
            except:
                wx.MessageDialog(self, u"Cannot open file: '{0}'".format(path), "Cannot open file", wx.ICON_ERROR).ShowModal()
                raise

    def save(self, event):
        if self.path == None:
            self.saveas(None)
        else:
            try:
                print(u"Saving project at: '{}'".format(self.path))
                self.project.save(self, self.path)
            except:
                wx.MessageDialog(self, u"Cannot save file: '{0}'".format(self.path), "Cannot save file", wx.ICON_ERROR).ShowModal()
                self.path = None

    def saveas(self, event):
        dia = wx.FileDialog(self, "Select a file to save", wildcard="PySaved-files (*.pysa)|*.pysa", style=wx.FD_SAVE)
        if dia.ShowModal() == wx.ID_OK:
            self.path = dia.GetPath()
            if ".pysa" not in self.path:
                self.path += ".pysa"
            self.save(None)

    def exit(self, event):
        if self.askForSavingIfNeed() and not self.progress:
            print("\nQuit PySaved...")
            sys.exit(0)

    def search_icon(self, event):
        dia = wx.FileDialog(self, "Select a file to open", wildcard="Icon-files (*.ico)|*.ico", style=wx.FD_OPEN)
        if dia.ShowModal() == wx.ID_OK:
            self.input_icon.SetValue(dia.GetPath())

    def search_execfile(self, event):
        dia = wx.FileDialog(self, "Select a file to open", wildcard="Python-files (*.py)|*.py", style=wx.FD_OPEN)
        if dia.ShowModal() == wx.ID_OK:
            self.input_execfile.SetValue(dia.GetPath())

    def addPath(self, event):
        dia = wx.DirDialog(self, "Select a dir")
        if dia.ShowModal() == wx.ID_OK:
            if dia.GetPath() not in self.project.pathstosearchin:
                self.project.pathstosearchin.append(dia.GetPath())
                self.project.loadAllhiddenmodules(self)
            
    def editPath(self, event):
        sel = self.list_pathstosearchin.GetSelection()
        strSel = self.list_pathstosearchin.GetStringSelection()
        if sel == -1: return
        
        while True:
            dia = wx.TextEntryDialog(self, u"Enter a new path for '{}'".format(strSel), "Edit Path", strSel)
            if dia.ShowModal() == wx.ID_OK:
                if dia.GetValue().strip() == "" or not os.path.exists(dia.GetValue()):
                    wx.MessageDialog(self, "Unknown path!", "", wx.ICON_ERROR).ShowModal()
                else:
                    self.project.pathstosearchin[sel] = dia.GetValue()
                    self.project.loadAllhiddenmodules(self)
                    break

    def delPath(self, event):
        sel = self.list_pathstosearchin.GetSelection()
        if sel == -1: return
        del(self.project.pathstosearchin[sel])
        self.project.loadAllhiddenmodules(self)

    def event_search_outpath(self, event):
        dia = wx.DirDialog(self, "Select a dir to save in")
        if dia.ShowModal() == wx.ID_OK:
            self.input_outpath.SetValue(dia.GetPath())

    def event_search_temppath(self, event):
        dia = wx.DirDialog(self, "Select a dir to save in")
        if dia.ShowModal() == wx.ID_OK:
            self.input_outpath.SetValue(dia.GetPath())

    def start(self, event):
        self.project.loadFromFrame(self)
        c = builder.Connector(self.project)
        thread.start_new(self.loop, (c,))
        thread.start_new(builder.build, (c,))
        thread.start_new(builder.log, (c,))
    
    def loop(self, c):
        def success():
            wx.MessageDialog(self, "Building package successful!", "Successful!", wx.ICON_INFORMATION).ShowModal()
        def error(fm):
            wx.MessageDialog(self, u"Error while building package:\n\n{}".format(fm), "Error!", wx.ICON_ERROR).ShowModal()
        def log(l):
            self.list_log.SetItems(l)
            self.list_log.Select(len(l)-1)
        
        self.progress = True
        wx.CallAfter(self.Disable)
        while True:
            time.sleep(0.1)
            
            wx.CallAfter(log, c.log)
                
            if c.finished:
                wx.CallAfter(success)
                break
            elif c.error:
                wx.CallAfter(error, c.errormsg)
                break
        
        wx.CallAfter(self.Enable, True)
        self.progress = False
    
    def about(self, event):
        info = wx.AboutDialogInfo()
        
        info.SetName("PySaved")
        info.SetVersion("0.1")
        info.SetCopyright("(c) 2015 by Arne Hannappel")
        info.AddArtist("Adrian Gisder")
        info.SetWebSite("http://www.arnehannappel.de/index.php/programme/pysaved")
        info.SetDescription("PySaved is a simple GUI for PyInstaller, a program that converts Python (2.6-2.7) programs into stand-alone executables.")
        info.SetLicence(statics.gplv2)
        
        wx.AboutBox(info)

def start_frame():
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
