import threading
import xbmc
import xbmcgui

homeWindow = xbmcgui.Window(10000)

def log(msg, level = 1):
    xbmc.log('Underground Helper Service :: ' + msg, level=xbmc.LOGNOTICE)

class ContainerMonitor(threading.Thread):
    timeout = 0.05
    monitor = None

    changed = True

    previousContent = ''
    content = ''
    previousFolderPath = ''
    folderPath = ''

    def __init__(self, *args):
        log('ContainerMonitor started')
        self.monitor = xbmc.Monitor()
        threading.Thread.__init__(self, *args)

    def run(self):
        while not self.monitor.abortRequested():
            if (self.monitor.waitForAbort(self.timeout)):
                break

            if (self.changed == False):
                self.changed = True
                homeWindow.setProperty('Changed', 'True')

            newFolderPath = xbmc.getInfoLabel('Container.FolderPath')
            if (self.folderPath != newFolderPath):
                self.previousFolderPath = self.folderPath
                self.folderPath = newFolderPath
                homeWindow.setProperty('PreviousFolderPath', self.previousFolderPath)
                homeWindow.setProperty('FolderPath', self.folderPath)

                self.changed = False
                homeWindow.setProperty('Changed', 'False')

                if (len(self.folderPath) < len(self.previousFolderPath)):
                    homeWindow.setProperty('ChangedBackwards', 'True')
                else:
                    homeWindow.setProperty('ChangedBackwards', 'False')

            newContent = xbmc.getInfoLabel('Container.Content')
            if (self.content != newContent):
                self.previousContent = self.content
                self.content = newContent
                homeWindow.setProperty('PreviousContent', self.previousContent)
                homeWindow.setProperty('Content', self.content)

containerMonitor = ContainerMonitor()
containerMonitor.start()
