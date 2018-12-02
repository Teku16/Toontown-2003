import DistributedObject, DirectNotifyGlobal, Localizer

class DistributedTrophyMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrophyMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if toonbase.tcr.trophyManager != None:
            toonbase.tcr.trophyManager.delete()
        toonbase.tcr.trophyManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        toonbase.tcr.trophyManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        toonbase.tcr.trophyManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def d_requestTrophyScore(self):
        self.sendUpdate('requestTrophyScore', [])