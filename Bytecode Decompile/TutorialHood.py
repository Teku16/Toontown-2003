from ShowBaseGlobal import *
import Hood, TutorialTownLoader
from ToontownGlobals import *
import SkyUtil

class TutorialHood(Hood.Hood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore):
        Hood.Hood.__init__(self, parentFSM, doneEvent, dnaStore)
        self.id = Tutorial
        self.townLoaderClass = TutorialTownLoader.TutorialTownLoader
        self.safeZoneLoaderClass = None
        self.storageDNAFile = None
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)
        return

    def load(self):
        Hood.Hood.load(self)
        self.parentFSM.getStateNamed('TutorialHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('TutorialHood').removeChild(self.fsm)
        Hood.Hood.unload(self)

    def enter(self, *args):
        Hood.Hood.enter(self, *args)

    def exit(self):
        Hood.Hood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)