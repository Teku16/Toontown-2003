from ShowBaseGlobal import *
from PandaObject import *
from ClockDelta import *
import DistributedObject, CollisionSphere, CollisionNode, ToontownGlobals
SPIN_RATE = 1.25

class DistributedDGFlower(DistributedObject.DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.bigFlower = loader.loadModel('phase_8/models/props/DG_flower-mod.bam')
        self.bigFlower.setPos(1.39, 92.91, 2.0)
        self.bigFlower.setScale(2.5)
        self.bigFlower.reparentTo(render)
        self.flowerCollSphere = CollisionSphere.CollisionSphere(0, 0, 0, 4.5)
        self.flowerCollSphereNode = CollisionNode.CollisionNode('bigFlowerCollide')
        self.flowerCollSphereNode.addSolid(self.flowerCollSphere)
        self.flowerCollSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.bigFlower.attachNewNode(self.flowerCollSphereNode)
        self.flowerTrigSphere = CollisionSphere.CollisionSphere(0, 0, 0, 6.0)
        self.flowerTrigSphere.setTangible(0)
        self.flowerTrigSphereNode = CollisionNode.CollisionNode('bigFlowerTrigger')
        self.flowerTrigSphereNode.addSolid(self.flowerTrigSphere)
        self.flowerTrigSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.bigFlower.attachNewNode(self.flowerTrigSphereNode)
        taskMgr.add(self.__flowerSpin, self.taskName('DG-flowerSpin'))
        self.accept('enterbigFlowerTrigger', self.__flowerEnter)
        self.accept('exitbigFlowerTrigger', self.__flowerExit)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        taskMgr.remove(self.taskName('DG-flowerRaise'))
        taskMgr.remove(self.taskName('DG-flowerSpin'))
        self.ignore('enterbigFlowerTrigger')
        self.ignore('exitbigFlowerTrigger')

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.bigFlower.removeNode()
        del self.bigFlower
        del self.flowerCollSphere
        del self.flowerCollSphereNode

    def __flowerSpin(self, task):
        self.bigFlower.setH(self.bigFlower.getH() + SPIN_RATE)
        return Task.cont

    def __flowerEnter(self, collisionEntry):
        self.sendUpdate('avatarEnter', [])

    def __flowerExit(self, collisionEntry):
        self.sendUpdate('avatarExit', [])

    def setHeight(self, newHeight):
        pos = self.bigFlower.getPos()
        self.bigFlower.lerpPos(pos[0], pos[1], newHeight, 0.5, task=self.taskName('DG-flowerRaise'))