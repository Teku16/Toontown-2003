from ShowBaseGlobal import *
import DistributedObject, DirectNotifyGlobal

class DeleteManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DeleteManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        return None
        return

    def generate(self):
        self.accept('deleteItems', self.d_setInventory)
        return None
        return

    def disable(self):
        self.ignore('deleteItems')
        return None
        return

    def d_setInventory(self, newInventoryString):
        self.sendUpdate('setInventory', [newInventoryString])
        return None
        return