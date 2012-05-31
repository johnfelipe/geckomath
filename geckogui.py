#!/usr/bin/env python-32
# geckogui.py

'''This is the main application script for Geckomath.

This script provides the GUI for geckomath.py, allowing the user to set
configuration values and run the program.
'''

# stdlib modules
import argparse
import ConfigParser
import logging
import os

# 3rd party modules
import wx
from wx.lib.mixins.inspection import InspectionMixin

# geckomath modules
from geckomodules import *
import geckomath

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
WILDCARD = "PDF (*.pdf)|*.pdf|"  "All files (*.*)|*.*"


class ConfigFrame(wx.Frame):
    '''The main application frame for Geckomath.

    The contents of the frame are created by iterating over all of the
    modules in the `geckomodules` directory, giving each a configuration pane,
    and then adding a button to run geckomath.
    '''
    def __init__(self, parent, id, version, to_file):
        wx.Frame.__init__(self, parent, id, 'Geckomath v.{}'.format(version),
                          wx.DefaultPosition, ((774 - 284), 553))

        self.to_file = to_file
        self.build_menu()

        self.scroll = wx.ScrolledWindow(self, -1)
        panel = wx.Panel(self.scroll, -1)
        sizer = wx.GridBagSizer(4, 4)

        panel.header_font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.BOLD)

        wx.EVT_PAINT(self, self.OnPaint)

        self.prob_panels = dict()

        self.problem_output = OutputPanel(panel, 'Problems')
        sizer.Add(self.problem_output, (0, 0), flag=wx.EXPAND)
        self.solution_output = OutputPanel(panel, 'Solutions')
        sizer.Add(self.solution_output, (1, 0), flag=wx.EXPAND)

        sizer_index = 2
        probtypes = Problems.PROBTYPES
        probtypes.sort(key=lambda x: x.secname)
        for probtype in Problems.PROBTYPES:
            logging.debug('adding problem type {}'.format(probtype.__name__))
            prob_panel = ProbPanel(panel, probtype.secname)
            self.prob_panels[probtype.__name__] = prob_panel
            sizer.Add(prob_panel, (sizer_index, 0))
            sizer_index += 1

        if self.to_file:
            label = 'Write to file'
        else:
            label = 'Generate PDFs'

        save_button = wx.Button(panel, id=-1, label=label)
        save_button.Bind(wx.EVT_BUTTON, self.write_to_file)
        sizer.Add(save_button, (sizer_index, 0), flag=wx.EXPAND)

        panel.SetSizerAndFit(sizer)

        self.Centre()

        width, height = panel.GetSize()
        self.unit = 1
        self.scroll.SetScrollbars(self.unit, self.unit,
                                  width / self.unit,
                                  height / self.unit)

        self.Show(True)

    def build_menu(self):
        'Build a menu that is cross-platform compatible'
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()

#        item = file_menu.Append(wx.ID_ANY, text = "&Open")
#        self.Bind(wx.EVT_MENU, self.OnOpen, item)
#
#        item = file_menu.Append(wx.ID_PREFERENCES, text = "&Preferences")
#        self.Bind(wx.EVT_MENU, self.OnPrefs, item)
#
        item = file_menu.Append(wx.ID_EXIT, text="&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        menu_bar.Append(file_menu, "&File")

        help_menu = wx.Menu()

        item = help_menu.Append(wx.ID_HELP, "Test &Help",
                                "Help for this simple test")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        ## this gets put in the App menu on OS X
        item = help_menu.Append(wx.ID_ABOUT, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def OnQuit(self, event):
        self.Destroy()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to test\n"
                                     "the use of menus on Mac, etc.\n",
                                "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                                "Test Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, event):
        dlg = wx.MessageDialog(self, "This would be an open Dialog\n"
                                     "If there was anything to open\n",
                                "Open File", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self, "This would be an preferences Dialog\n"
                                     "If there were any preferences to set.\n",
                                "Preferences", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPaint(self, event=None):
        pdc = wx.PaintDC(self)
        pdc.Clear()

    def write_to_file(self, event):
        '''Build a config object, pass it to geckomath.main().'''
        logging.debug("Writing to file")
        config = ConfigParser.ConfigParser()

        config.add_section('output')
        config.set('output', 'problems', self.problem_output.path)
        config.set('output', 'solutions', self.solution_output.path)

        for section, params in self.prob_panels.items():
            config.add_section(section)
            config.set(section, 'nprobs', str(params.counter.GetValue()))
            depth = str(bool(params.depth.GetSelection()))
            logging.debug('{section} Depth: {depth}'.format(section=section,
                                                            depth=depth))
            config.set(section, 'solutions', depth)

        config.add_section('LaTeX')
        config.set('LaTeX', 'preamble',
            r'''\documentclass[11pt,notitlepage,letterpaper,oneside]{article}
                \usepackage{amsmath}
                \newcommand{\abs}[1]{\left\lvert{#1}\right\rvert}
                \begin{document}''')
        config.set('LaTeX', 'postamble',
            r'\end{document}')

        if self.to_file:
            logging.debug('writing to geckomath.ini')
            with open('geckomath.ini', 'wb') as configfile:
                config.write(configfile)

        else:
            logging.debug('calling geckomath.main')
            geckomath.main(config)


class OutputPanel(wx.Panel):
    '''Configure the output file locations.'''
    def __init__(self, parent, name):
        wx.Panel.__init__(self, parent, -1)
        self.currentDirectory = os.getcwd()
        self.filename = '.'.join([name.lower(), 'pdf'])
        self.path = os.path.join(self.currentDirectory, self.filename)

        sizer = wx.GridBagSizer(vgap=4, hgap=4)
        ctrl_sizer = wx.GridBagSizer(vgap=4, hgap=4)

        title = wx.StaticText(self, -1, name)
        title.SetFont(parent.header_font)
        sizer.Add(title, (0, 0), flag=wx.EXPAND)

        label = wx.StaticText(self, -1, 'output file name')
        ctrl_sizer.Add(label, (0, 0), flag=wx.EXPAND)

        self.display = wx.TextCtrl(self, -1, self.filename,
                                   size=(400, 25))
        ctrl_sizer.Add(self.display, (1, 0), flag=wx.EXPAND)

        openFileDlgBtn = wx.Button(self, label="Browse")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)

        ctrl_sizer.Add(openFileDlgBtn, (1, 1), flag=wx.RIGHT)
        sizer.Add(ctrl_sizer, (1, 0), flag=wx.EXPAND)

        self.SetSizerAndFit(sizer)

    def onOpenFile(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=WILDCARD,
            style=wx.SAVE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.filename = dlg.GetFilename()
            if not self.path.endswith('.pdf'):
                self.path = '.'.join([self.path, 'pdf'])
                self.filename = '.'.join([self.filename, 'pdf'])
            self.display.SetValue(self.path)
        dlg.Destroy()


class ProbPanel(wx.Panel):
    '''The configuration panel for a particular problem type.'''
    def __init__(self, parent, name):
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.GridBagSizer(4, 4)
        ctrl_sizer = wx.GridBagSizer(4, 4)

        ptype = wx.StaticText(self, -1, name)
        ptype.SetFont(parent.header_font)
        sizer.Add(ptype, (0, 0), flag=wx.EXPAND)

        counter_lbl = wx.StaticText(self, -1, 'Number of problems')
        ctrl_sizer.Add(counter_lbl, (0, 0), flag=wx.EXPAND)

        self.counter = wx.SpinCtrl(self, -1)
        self.counter.SetValue(5)
        ctrl_sizer.Add(self.counter, (0, 1), flag=wx.EXPAND)

        depth_lbl = wx.StaticText(self, -1, 'Depth of solutions')
        ctrl_sizer.Add(depth_lbl, (0, 2), flag=wx.EXPAND)

        self.depth = wx.Choice(self, -1,
                               choices=['Just answers', 'Full solutions'])
        self.depth.SetSelection(1)
        ctrl_sizer.Add(self.depth, (0, 3), flag=wx.EXPAND)

        sizer.Add(ctrl_sizer, (1, 0), flag=wx.EXPAND)

        self.SetSizerAndFit(sizer)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store_true', dest='to_file')
    args = parser.parse_args()

    class MyApp(wx.App, InspectionMixin):
        'The main app loop.'
        def OnInit(self):
            self.Init()
            frame = ConfigFrame(None, -1, 0.1, args.to_file)
            frame.Show()
            self.SetTopWindow(frame)
            return True

    app = MyApp(0)
    app.MainLoop()
