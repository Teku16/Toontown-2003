from PandaObject import *
from ShowBaseGlobal import *
import Playground, whrandom, State, Actor, ToontownGlobals

class MMPlayground(Playground.Playground):
    __module__ = __name__

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.activityFsm = FSM.FSM('Activity', [
         State.State('off', self.enterOff, self.exitOff, [
          'OnPiano']),
         State.State('OnPiano', self.enterOnPiano, self.exitOnPiano, [
          'off'])], 'off', 'off')
        self.activityFsm.enterInitialState()

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        del self.activityFsm
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)

    def handleBookClose(self):
        Playground.Playground.handleBookClose(self)

    def teleportInDone(self):
        Playground.Playground.teleportInDone(self)

    def enterOff(self):
        return None
        return

    def exitOff(self):
        return None
        return

    def enterOnPiano(self):
        toonbase.localToon.b_setParent(ToontownGlobals.SPMinniesPiano)
        base.drive.node().setPos(toonbase.localToon.getPos())
        base.drive.node().setHpr(toonbase.localToon.getHpr())

    def exitOnPiano(self):
        toonbase.localToon.b_setParent(ToontownGlobals.SPRender)
        base.drive.node().setPos(toonbase.localToon.getPos())
        base.drive.node().setHpr(toonbase.localToon.getHpr())