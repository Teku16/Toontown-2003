from ShowBaseGlobal import *
import Hood, DGTownLoader, DGSafeZoneLoader
from ToontownGlobals import *
import SkyUtil

class DGHood(Hood.Hood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore):
        Hood.Hood.__init__(self, parentFSM, doneEvent, dnaStore)
        self.id = DaisyGardens
        self.townLoaderClass = DGTownLoader.DGTownLoader
        self.safeZoneLoaderClass = DGSafeZoneLoader.DGSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_DG.dna'
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.titleColor = (0.8, 0.6, 1.0, 1.0)

    def load(self):
        Hood.Hood.load(self)
        self.parentFSM.getStateNamed('DGHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('DGHood').removeChild(self.fsm)
        Hood.Hood.unload(self)

    def enter(self, *args):
        Hood.Hood.enter(self, *args)

    def exit(self):
        Hood.Hood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)