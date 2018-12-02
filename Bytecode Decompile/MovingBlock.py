from ShowBaseGlobal import *
from IntervalGlobal import *
import DirectObject, ToontownGlobals

class MovingBlock(DirectObject.DirectObject, NodePath):
    __module__ = __name__

    def __init__(self, index, model):
        self.token = ToontownGlobals.SPDynamic + index
        self.name = 'MovingBlock-%d' % index
        NodePath.__init__(self, hidden.attachNewNode(self.name))
        self.model = model.copyTo(self)
        self.model.find('**/floor').setName(self.name)
        toonbase.tcr.token2nodePath[self.token] = self
        self.accept('on-floor', self.__handleOnFloor)
        self.accept('off-floor', self.__handleOffFloor)
        return

    def delete(self):
        del toonbase.tcr.token2nodePath[self.token]
        self.model.removeNode()
        del self.model
        self.ignore('on-floor')
        self.ignore('off-floor')
        return

    def __handleOnFloor(self, collEntry):
        if collEntry.getIntoNode().getName() == self.name:
            print 'on floor %s' % self.name
            toonbase.localToon.b_setParent(self.token)
            base.drive.node().setPos(toonbase.localToon.getPos())
            base.drive.node().setHpr(toonbase.localToon.getHpr())
        return

    def __handleOffFloor(self, collEntry):
        if collEntry.getIntoNode().getName() == self.name:
            print 'off floor %s' % self.name
            toonbase.localToon.b_setParent(ToontownGlobals.SPRender)
            base.drive.node().setPos(toonbase.localToon.getPos())
            base.drive.node().setHpr(toonbase.localToon.getHpr())
        return