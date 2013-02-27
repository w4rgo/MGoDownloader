import wx
import threading
import os
import time
import subprocess
# Define notification event for thread completion
EVT_BEGIN_ID = wx.NewId()
EVT_START_ID = wx.NewId()
EVT_FINISHED_ID = wx.NewId()
EVT_END_ID = wx.NewId()

def EVT_BEGIN(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_BEGIN_ID, func)

def EVT_START(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_START_ID, func)
    
def EVT_FINISHED(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_FINISHED_ID, func)
    
def EVT_END(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_END_ID, func)

class EventBegin(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BEGIN_ID)
class EventStart(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, song):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_START_ID)
        self.song = song
class EventFinished(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, song):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_FINISHED_ID)
        self.song = song
class EventEnd(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_END_ID)
        
class ThreadDownload(threading.Thread):
    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.args = args
        self.func=func
    def run(self):
        apply(self.func,self.args)
        
    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
        
def downloadAsync(work,folder,goear):
    if goear.selectedSongs==[]:
        return
    selected=work
    
    print "TRABAJO: " , work
    
    #deshabilitar botones y selected list
    #self.enableSelecting(False)

    #os.chdir(os.curdir + "/"+ folder)
    wx.PostEvent(goear,EventBegin())
    for song in selected:
        #self.notifyStartSong(str(song.num),song.name)
        #
        #self.notifyFinishedSong(str(song.num))     
        wx.PostEvent(goear,EventStart(song))
        song.downloadSong(folder)
        time.sleep(1)
        wx.PostEvent(goear,EventFinished(song))
        
    #self.enableSelecting(True)
    #if goear.selectedSongs==[]:
    #    wx.PostEvent(goear,EventEnd())

    return

##def downloadAsyncProcess(work,folder,goear):
##    if goear.selectedSongs==[]:
##        return
##    folder= folder.replace(" ","-")
##    selected=work
##    
##    print "TRABAJO: " , work
##    
##    #deshabilitar botones y selected list
##    #self.enableSelecting(False)
##    if not os.path.exists(folder):
##        os.makedirs(folder)
##    os.chdir(os.curdir + "/"+ folder)
##    
##    wx.PostEvent(goear,EventBegin())
##    for song in selected:
##        #self.notifyStartSong(str(song.num),song.name)
##        #
##        #self.notifyFinishedSong(str(song.num))     
##        wx.PostEvent(goear,EventStart(song))
##        song.downloadSong(folder)
##        wx.PostEvent(goear,EventFinished(song))
##        
##    #self.enableSelecting(True)
##    if goear.selectedSongs==[]:
##        wx.PostEvent(goear,EventEnd())
##
##    return

class InstanceMethod(object):
    def __init__(self,method):
        self.method = method
        self.methodName = method.func_name
    def __getstate__(self):
        return (self.method, self.methodName)
    def __setstate__(self,state):
        self.methods = getattr(obj,name)