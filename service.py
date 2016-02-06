import threading
import xbmc
import xbmcgui

homeWindow = xbmcgui.Window(10000)

def log(msg, level = 1):
    xbmc.log('Underground Helper Service :: ' + msg, level=xbmc.LOGNOTICE)

class ContainerMonitor(threading.Thread):
    timeout = 0.5
    monitor = None

    currentContent = ''

    def __init__(self, *args):
        log('ContainerMonitor started')
        self.monitor = xbmc.Monitor()
        threading.Thread.__init__(self, *args)

    def run(self):
        while not self.monitor.abortRequested():
            if (self.monitor.waitForAbort(self.timeout)):
                break

            newContent = xbmc.getInfoLabel('Container.Content')
            if (self.currentContent != newContent):
                # log('content change ' + self.currentContent + ' to ' + newContent)
                self.currentContent = newContent
                homeWindow.setProperty('PreviousContent', newContent)

containerMonitor = ContainerMonitor()
containerMonitor.start()
