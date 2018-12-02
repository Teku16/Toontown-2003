from PandaObject import *
from DirectNotifyGlobal import *
ESNew = 1
ESDeleted = 2
ESDisabling = 3
ESDisabled = 4
ESGenerating = 5
ESGenerated = 6

class DistributedObject(PandaObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObject')
    neverDisable = 0

    def __init__(self, cr):
        try:
            self.DistributedObject_initialized
        except:
            self.DistributedObject_initialized = 1
            self.cr = cr
            self.setCacheable(0)
            self.delayDeleteCount = 0
            self.deleteImminent = 0
            self.activeState = ESNew

        return None
        return

    def setNeverDisable(self, bool):
        self.neverDisable = bool
        return None
        return

    def getNeverDisable(self):
        return self.neverDisable

    def setCacheable(self, bool):
        self.cacheable = bool
        return None
        return

    def getCacheable(self):
        return self.cacheable

    def deleteOrDelay(self):
        if self.delayDeleteCount > 0:
            self.deleteImminent = 1
        else:
            self.disableAnnounceAndDelete()
        return None
        return

    def delayDelete(self, flag):
        if flag == 1:
            self.delayDeleteCount += 1
        else:
            if flag == 0:
                self.delayDeleteCount -= 1
            else:
                self.notify.error('Invalid flag passed to delayDelete: ' + str(flag))
        if self.delayDeleteCount < 0:
            self.notify.error('Somebody decremented delayDelete for doId %s without incrementing' % self.doId)
        else:
            if self.delayDeleteCount == 0:
                self.notify.debug('delayDeleteCount for doId %s now 0' % self.doId)
                if self.deleteImminent:
                    self.notify.debug('delayDeleteCount for doId %s -- deleteImminent' % self.doId)
                    self.disableAnnounceAndDelete()
            else:
                self.notify.debug('delayDeleteCount for doId %s now %s' % (self.doId, self.delayDeleteCount))
        return self.delayDeleteCount

    def disableAnnounceAndDelete(self):
        self.disableAndAnnounce()
        self.delete()
        return None
        return

    def disableAndAnnounce(self):
        if self.activeState != ESDisabled:
            self.activeState = ESDisabling
            messenger.send(self.uniqueName('disable'))
            self.disable()
        return None
        return

    def announceGenerate(self):
        self.activeState = ESGenerated
        messenger.send(self.uniqueName('generate'), [self])

    def disable(self):
        self.activeState = ESDisabled

    def isDisabled(self):
        return self.activeState < ESGenerating

    def delete(self):
        try:
            self.DistributedObject_deleted
        except:
            self.DistributedObject_deleted = 1
            del self.cr
            return

    def generate(self):
        self.activeState = ESGenerating

    def generateInit(self):
        self.activeState = ESGenerating

    def getDoId(self):
        return self.doId

    def updateRequiredFields(self, cdc, di):
        for i in cdc.broadcastRequiredCDU:
            i.updateField(cdc, self, di)

    def updateAllRequiredFields(self, cdc, di):
        for i in cdc.allRequiredCDU:
            i.updateField(cdc, self, di)

    def updateRequiredOtherFields(self, cdc, di):
        for i in cdc.broadcastRequiredCDU:
            i.updateField(cdc, self, di)

        numberOfOtherFields = di.getArg(STUint16)
        for i in range(numberOfOtherFields):
            cdc.updateField(self, di)

        return None
        return

    def sendUpdate(self, fieldName, args=[], sendToId=None):
        self.cr.sendUpdate(self, fieldName, args, sendToId)

    def taskName(self, taskString):
        return taskString + '-' + str(self.getDoId())

    def uniqueName(self, idString):
        return idString + '-' + str(self.getDoId())

    def isLocal(self):
        return 0