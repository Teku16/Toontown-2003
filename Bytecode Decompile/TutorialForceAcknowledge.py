from ShowBaseGlobal import *
import ToontownDialog, Localizer

class TutorialForceAcknowledge:
    __module__ = __name__

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        return
        return

    def enter(self):
        toonbase.localToon.loop('neutral')
        self.doneStatus = {'mode': 'incomplete'}
        msg = Localizer.TutorialForceAcknowledgeMessage
        self.dialog = ToontownDialog.ToontownDialog(text=msg, command=self.handleOk, style=ToontownDialog.Acknowledge)
        return

    def exit(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        return
        return

    def handleOk(self, value):
        messenger.send(self.doneEvent, [self.doneStatus])
        return