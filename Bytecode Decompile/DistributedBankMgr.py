import DistributedObject, DirectNotifyGlobal, Localizer

class DistributedBankMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBankMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if toonbase.tcr.bankManager != None:
            toonbase.tcr.bankManager.delete()
        toonbase.tcr.bankManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        toonbase.tcr.bankManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        toonbase.tcr.bankManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def d_transferMoney(self, amount):
        self.sendUpdate('transferMoney', [amount])