from ShowBaseGlobal import *
from PandaObject import *
import DistributedObject, DirectNotifyGlobal, ZoneUtil

class TutorialManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        return

    def generate(self):
        messenger.send('tmGenerate')
        self.accept('requestTutorial', self.d_requestTutorial)
        self.accept('rejectTutorial', self.d_rejectTutorial)
        return

    def disable(self):
        self.ignoreAll()
        return

    def d_requestTutorial(self):
        self.sendUpdate('requestTutorial', [])
        return

    def d_rejectTutorial(self):
        self.sendUpdate('rejectTutorial', [])
        return

    def enterTutorial(self, branchZone, streetZone, shopZone, hqZone):
        toonbase.localToon.inTutorial = 1
        ZoneUtil.overrideOn(branch=branchZone, exteriorList=[streetZone], interiorList=[shopZone, hqZone])
        messenger.send('startTutorial', [shopZone])
        self.acceptOnce('stopTutorial', self.__handleStopTutorial)
        self.acceptOnce('toonArrivedTutorial', self.d_toonArrived)

    def __handleStopTutorial(self):
        toonbase.localToon.inTutorial = 0
        self.d_allDone()
        ZoneUtil.overrideOff()

    def d_allDone(self):
        self.sendUpdate('allDone', [])
        return

    def d_toonArrived(self):
        self.sendUpdate('toonArrived', [])
        return