from ToonBaseGlobal import *
from IntervalGlobal import *
from OrthoDrive import *

class OrthoWalk:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('OrthoWalk')
    BROADCAST_POS_TASK = 'OrthoWalkBroadcastPos'

    def __init__(self, orthoDrive, collisions=1, broadcast=1, broadcastPeriod=0.1):
        self.orthoDrive = orthoDrive
        self.collisions = collisions
        self.broadcast = broadcast
        self.broadcastPeriod = broadcastPeriod
        self.priority = self.orthoDrive.priority + 1
        self.lt = toonbase.localToon

    def destroy(self):
        self.orthoDrive.destroy()
        del self.orthoDrive

    def start(self):
        self.notify.debug('start')
        self.orthoDrive.start()
        if self.collisions:
            self.__initCollisions()
        if self.broadcast:
            self.__initBroadcast()

    def stop(self):
        self.notify.debug('stop')
        self.__shutdownCollisions()
        self.__shutdownBroadcast()
        self.orthoDrive.stop()

    def __initCollisions(self):
        self.notify.debug('initCollisions')
        lt = toonbase.localToon
        lt.collisionsOn()
        lt.pusher.clearColliders()
        lt.pusher.addColliderNode(lt.cSphereNode, lt.node())
        self.__collisionsOn = 1

    def __shutdownCollisions(self):
        if not hasattr(self, '_OrthoWalk__collisionsOn'):
            return
        del self.__collisionsOn
        self.notify.debug('shutdownCollisions')
        lt = toonbase.localToon
        lt.collisionsOff()
        lt.pusher.clearColliders()
        lt.pusher.addColliderDrive(lt.cSphereNode, base.drive.node())

    def __initBroadcast(self):
        self.notify.debug('initBroadcast')
        self.__timeSinceLastPosBroadcast = 0.0
        self.__lastPosBroadcast = self.lt.getPos()
        self.__lastHprBroadcast = self.lt.getHpr()
        self.__storeStop = 0
        lt = self.lt
        lt.d_clearSmoothing()
        lt.d_setSmPosHpr(lt.getX(), lt.getY(), lt.getZ(), lt.getH(), lt.getP(), lt.getR())
        taskMgr.add(self.__doBroadcast, self.BROADCAST_POS_TASK, priority=self.priority)

    def __shutdownBroadcast(self):
        self.notify.debug('shutdownBroadcast')
        taskMgr.remove(self.BROADCAST_POS_TASK)

    def __doBroadcast(self, task):
        dt = globalClock.getDt()
        self.__timeSinceLastPosBroadcast += dt
        if self.__timeSinceLastPosBroadcast >= self.broadcastPeriod:
            self.__timeSinceLastPosBroadcast = 0
            pos = self.lt.getPos()
            hpr = self.lt.getHpr()
            if self.orthoDrive.setHeading and (pos[0] != self.__lastPosBroadcast[0] or pos[1] != self.__lastPosBroadcast[1] or hpr[0] != self.__lastHprBroadcast[0]):
                self.lt.d_setSmXYH(pos[0], pos[1], hpr[0])
                self.__lastPosBroadcast = pos
                self.__lastHprBroadcast = hpr
                self.__storeStop = 0
            else:
                if pos[0] != self.__lastPosBroadcast[0] or pos[1] != self.__lastPosBroadcast[1]:
                    self.lt.d_setSmXY(pos[0], pos[1])
                    self.__lastPosBroadcast = pos
                    self.__storeStop = 0
                else:
                    if not self.__storeStop:
                        self.__storeStop = 1
                        self.lt.d_setSmStop()
        return Task.cont