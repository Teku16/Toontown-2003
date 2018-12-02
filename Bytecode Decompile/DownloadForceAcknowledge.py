from ShowBaseGlobal import *
import ToontownDialog, Localizer

class DownloadForceAcknowledge:
    __module__ = __name__

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        return

    def enter(self, phase):
        doneStatus = {}
        if not launcher:
            doneStatus['mode'] = 'complete'
            messenger.send(self.doneEvent, [doneStatus])
        if launcher.getPhaseComplete(phase):
            doneStatus['mode'] = 'complete'
            messenger.send(self.doneEvent, [doneStatus])
        try:
            toonbase.localToon.b_setAnimState('neutral', 1)
        except:
            pass
        else:
            doneStatus['mode'] = 'incomplete'
            self.doneStatus = doneStatus
            percentComplete = base.launcher.getPercentPhaseComplete(phase)
            phaseName = Localizer.LauncherPhaseNames[phase]
            msg = Localizer.DownloadForceAcknowledgeMsg % {'phase': phaseName, 'percent': percentComplete}
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