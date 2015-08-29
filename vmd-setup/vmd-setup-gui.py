#! /usr/bin/python

# VMD Setup GUI written by Synge Todo

import sys
import os
import shutil
import subprocess
import wx

import config

class Frame(wx.Frame):
    def __init__(self, prefix, scriptdir):
        self.prefix = prefix
        self.scriptdir = scriptdir
        self.process_download = None
        self.process_compile = None
        self.process_kill = False
        self.on_dialog = False

        wx.Frame.__init__(self, None, -1, "VMD Setup", size = (420,500))
        self.panel = wx.Panel(self, -1)

        layout = wx.BoxSizer(wx.VERTICAL)

        self.radio_download = wx.RadioButton(self.panel, -1, "Download a binary archive from official website")
        self.radio_download.Bind(wx.EVT_RADIOBUTTON, self.OnChooseRadioDownload)
        self.radio_download.SetValue(True)
        layout.Add(self.radio_download, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        grid_1 = wx.FlexGridSizer(2, 3)
        self.text_username = wx.TextCtrl(self.panel, -1, size = (285, -1))
        self.text_username.Bind(wx.EVT_TEXT, self.OnTextUsername)
        self.text_password = wx.TextCtrl(self.panel, -1) # style = wx.TE_PASSWORD
        self.text_password.Bind(wx.EVT_TEXT, self.OnTextPassword)
        grid_1.Add(wx.StaticText(self.panel, -1, '     '), 0)
        grid_1.Add(wx.StaticText(self.panel, -1, "Username:"), 0, wx.RIGHT, 4)
        grid_1.Add(self.text_username, 1, wx.EXPAND, 4)
        grid_1.Add(wx.StaticText(self.panel, -1, '     '), 0)
        grid_1.Add(wx.StaticText(self.panel, -1, "Password:"), 0, wx.RIGHT | wx.TOP, 4)
        grid_1.Add(self.text_password, 1, wx.EXPAND | wx.TOP, 4)
        layout.Add(grid_1, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.radio_local = wx.RadioButton(self.panel, -1, "Use a binary archive on local storage")
        self.radio_local.Bind(wx.EVT_RADIOBUTTON, self.OnChooseRadioLocal)
        layout.Add(self.radio_local, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        grid_2 = wx.FlexGridSizer(2, 3)
        self.text_file = wx.TextCtrl(self.panel, -1, size = (325, -1), style = wx.TE_READONLY)
        self.button_choose = wx.Button(self.panel, -1, "Choose")
        self.button_choose.Bind(wx.EVT_BUTTON, self.OnChoose)
        grid_2.Add(wx.StaticText(self.panel, -1, '     '), 0)
        grid_2.Add(wx.StaticText(self.panel, -1, "File:"), 0, wx.RIGHT | wx.TOP, 4)
        grid_2.Add(self.text_file, 1, wx.EXPAND | wx.TOP, 4)
        grid_2.Add(wx.StaticText(self.panel, -1, ''), 0)
        grid_2.Add(wx.StaticText(self.panel, -1, ''), 0)
        grid_2.Add(self.button_choose, 0, wx.TOP, 4)
        layout.Add(grid_2, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        box_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_help = wx.Button(self.panel, -1, "Help", size=(70,30))
        self.button_help.Bind(wx.EVT_BUTTON, self.OnHelp)
        self.button_cancel = wx.Button(self.panel, -1, "Cancel", size=(70,30))
        self.button_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.button_install = wx.Button(self.panel, -1, "Install", size=(70,30))
        self.button_install.Bind(wx.EVT_BUTTON, self.OnInstall)
        self.button_start = wx.Button(self.panel, -1, "Start VMD", size=(90,30))
        self.button_start.Bind(wx.EVT_BUTTON, self.OnStart)
        box_1.Add(self.button_help, 0, wx.LEFT | wx.BOTTOM, 5)
        box_1.Add(self.button_cancel, 0, wx.LEFT | wx.BOTTOM, 5)
        box_1.Add(self.button_install, 0, wx.LEFT | wx.BOTTOM, 5)
        box_1.Add(self.button_start, 0, wx.LEFT | wx.BOTTOM, 5)
        layout.Add(box_1, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 10)

        self.text_log = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(50,10))
        layout.Add(self.text_log, 1, wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
                                    
        self.panel.SetSizer(layout)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind (wx.EVT_IDLE, self.OnIdle)
        self.UpdateState()

    def OnCancel(self, event):
        if (self.process_download):
            self.on_dialog = True
            dialog = wx.MessageDialog(None, 'Downloading is now proceeding.  Stop download?', 'VMD Setup', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            if dialog.ShowModal() == wx.ID_YES:
                self.process_kill = True
            dialog.Destroy()
            self.on_dialog = False
        elif (self.process_compile):
            self.on_dialog = True
            dialog = wx.MessageDialog(None, 'Compilation is now proceeding.  Stop compilation?', 'VMD Setup', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            if dialog.ShowModal() == wx.ID_YES:
                self.process_kill = True
            dialog.Destroy()
            self.on_dialog = False
        else:
            self.Destroy()
        self.UpdateState()

    def OnChoose(self, event):
        self.OpenFileDialog()
        self.UpdateState()

    def OnChooseRadioDownload(self, event):
        self.UpdateState()

    def OnChooseRadioLocal(self, event):
        if (not self.text_file.GetValue()):
            self.OpenFileDialog()
        self.UpdateState()

    def OnClose(self, event):
        if (self.process_download or self.process_compile):
            self.OnCancel(event)
        if (not (self.process_download or self.process_compile)):
            self.Destroy()
        self.UpdateState()

    def OnHelp(self, event):
        wx.BeginBusyCursor() 
        import webbrowser
        webbrowser.open('file://' + scriptdir + '/help.html') 
        wx.EndBusyCursor() 
        
    def OnIdle(self, event):
        if (self.on_dialog): return
        if (self.process_download):
            ret = self.process_download.poll()
            if (ret == None):
                if (self.process_kill):
                    self.process_kill = False
                    self.process_download.kill()
                    self.process_download = None
                    self.text_log.AppendText('Killed.')
                    self.UpdateState()
                else:
                    line = self.process_download.stdout.readline()
                    self.text_log.AppendText(line)
            else:
                self.process_download = None
                if (ret != 0):
                    dialog = wx.MessageDialog(None, 'Password incorrect or username already taken.', 'Error', wx.OK | wx.ICON_ERROR)
                    dialog.ShowModal()
                    dialog.Destroy()
                else:
                    self.StartCompile(os.path.join(self.prefix, 'source', config.tarball))
                self.UpdateState()
        elif (self.process_compile):
            ret = self.process_compile.poll()
            if (ret == None):
                if (self.process_kill):
                    self.process_kill = False
                    self.process_compile.kill()
                    self.process_compile = None
                    self.text_log.AppendText('Killed.')
                    self.UpdateState()
                else:
                    line = self.process_compile.stdout.readline()
                    self.text_log.AppendText(line)
            else:
                self.process_compile = None
                if (ret != 0):
                    dialog = wx.MessageDialog(None, 'Error occured during compilation', 'Error', wx.OK | wx.ICON_ERROR)
                    dialog.ShowModal()
                    dialog.Destroy()
                else:
                    dialog = wx.MessageBox('Installation completed', 'VMD Setup')
                    # self.Destroy()
                self.UpdateState()

    def OnInstall(self, event):
        if (self.radio_download.GetValue()):
            target = os.path.join(self.prefix, 'source')
            tarfile = os.path.join(target, config.tarball)
            username = self.text_username.GetValue()
            password = self.text_password.GetValue()
            if (os.path.exists(tarfile)):
                dialog = wx.MessageDialog(None, tarfile + ' already exists.  Remove it and continue download?', 'VMD Setup', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
                if dialog.ShowModal() == wx.ID_OK:
                    dialog.Destroy()
                    os.remove(tarfile)
                else:
                    dialog.Destroy()
                    self.text_file.SetValue(tarfile)
                    self.radio_local.SetValue(True)
                    self.UpdateState()
                    return
            self.StartDownload(username, password, target)
        else:
            file = self.text_file.GetValue()
            if (file):
                self.StartCompile(file)
            else:
                dialog = wx.MessageDialog(None, 'Please specify a binary archive', 'Error',
                                          wx.OK | wx.ICON_ERROR)
                dialog.ShowModal()
                dialog.Destroy()
        self.UpdateState()

    def OnStart(self, event):
        vmd = os.path.join(self.prefix, 'bin', 'vmd')
        if (os.path.exists(vmd)):
            cmd = ['/usr/bin/gnome-terminal', '-e', vmd]
            subprocess.Popen(cmd)
            self.Destroy()

    def OnTextUsername(self, event):
        self.UpdateState()

    def OnTextPassword(self, event):
        self.UpdateState()

    def OpenFileDialog(self):
        wildCard = "tar.gz file (*.tar.gz)|*.tar.gz|All files (*.*)|*.*"
        if (self.text_file.GetValue()):
            path = os.path.dirname(self.text_file.GetValue())
        else:
            path = os.environ['HOME']
        dialog = wx.FileDialog(self, "Choose a binary archive", path, '', wildCard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.text_file.SetValue(dialog.GetPath())
            self.radio_local.SetValue(True)
        dialog.Destroy()

    def StartCompile(self, file):
        vmddir = os.path.join(self.prefix, 'libexec', 'vmd')
        if (os.path.exists(vmddir)):
            dialog = wx.MessageDialog(None, vmddir + ' already exists.  Clean up and install VMD anyway?', 'VMD Setup', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            if dialog.ShowModal() == wx.ID_OK:
                shutil.rmtree(vmddir)
                dialog.Destroy()
            else:
                dialog.Destroy()
                return            
        cmd = ['/bin/sh', os.path.join(self.scriptdir, 'compile.sh'), file, self.prefix]
        self.process_compile = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT,
                                                stdin=subprocess.PIPE)
        self.text_log.AppendText('Start compilation of VMD\n')

    def StartDownload(self, username, password, target):
        cmd = ['python', os.path.join(self.scriptdir, 'download.py'), username, password, target]
        self.process_download = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT,
                                                 stdin=subprocess.PIPE)
        self.text_log.AppendText('Start download of VMD\n')
        
    def UpdateState(self):
        if (self.process_download or self.process_compile):
            self.radio_download.Disable()
            self.radio_local.Disable()
            self.text_username.Disable()
            self.text_password.Disable()
            self.text_file.Disable()
            self.button_choose.Disable()
            self.button_help.Disable()
            self.button_install.Disable()
            self.button_start.Disable()
        else:
            self.radio_download.Enable()
            self.radio_local.Enable()
            self.button_choose.Enable()
            self.button_help.Enable()
            if (self.radio_download.GetValue()):
                self.text_username.Enable()
                self.text_password.Enable()
                self.text_file.Disable()
                if (self.text_username.GetValue() and self.text_password.GetValue()):
                    self.button_install.Enable()
                else:
                    self.button_install.Disable()
            else:
                self.text_username.Disable()
                self.text_password.Disable()
                self.text_file.Enable()
                if (self.text_file.GetValue()):
                    self.button_install.Enable()
                else:
                    self.button_install.Disable()
            if (os.path.exists(os.path.join(self.prefix, 'bin', 'vmd'))):
                self.button_start.Enable()
            else:
                self.button_start.Disable()

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Usage:", sys.argv[0], "prefix"
        sys.exit(127)
    scriptdir = os.path.dirname(sys.argv[0])
    prefix = sys.argv[1]
    app = wx.App()
    frame = Frame(prefix, scriptdir)
    frame.Show()
    app.MainLoop()
    app.Destroy()
