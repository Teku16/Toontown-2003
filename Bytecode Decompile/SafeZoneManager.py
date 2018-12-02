from ShowBaseGlobal import *
import DistributedObject, DirectNotifyGlobal

class SafeZoneManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SafeZoneManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        return None
        return

    def generate(self):
        self.accept('enterSafeZone', self.d_enterSafeZone)
        self.accept('exitSafeZone', self.d_exitSafeZone)
        return None
        return

    def disable(self):
        self.ignoreAll()
        return None
        return

    def d_enterSafeZone(self):
        self.sendUpdate('enterSafeZone', [])
        return None
        return

    def d_exitSafeZone(self):
        self.sendUpdate('exitSafeZone', [])
        return None
        return