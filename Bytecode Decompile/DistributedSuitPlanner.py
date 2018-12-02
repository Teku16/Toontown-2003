from ShowBaseGlobal import *
import DistributedObject, SuitPlannerBase

class DistributedSuitPlanner(DistributedObject.DistributedObject, SuitPlannerBase.SuitPlannerBase):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        SuitPlannerBase.SuitPlannerBase.__init__(self)
        self.suitList = []
        self.buildingList = [0, 0, 0, 0]
        return None
        return

    def generate(self):
        self.notify.info('DistributedSuitPlanner %d: generating' % self.getDoId())
        DistributedObject.DistributedObject.generate(self)
        toonbase.tcr.currSuitPlanner = self

    def disable(self):
        self.notify.info('DistributedSuitPlanner %d: disabling' % self.getDoId())
        DistributedObject.DistributedObject.disable(self)
        toonbase.tcr.currSuitPlanner = None
        return

    def d_suitListQuery(self):
        self.sendUpdate('suitListQuery')

    def suitListResponse(self, suitList):
        self.suitList = suitList
        messenger.send('suitListResponse')

    def d_buildingListQuery(self):
        self.sendUpdate('buildingListQuery')

    def buildingListResponse(self, buildingList):
        self.buildingList = buildingList
        messenger.send('buildingListResponse')