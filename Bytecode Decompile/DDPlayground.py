from PandaObject import *
from ShowBaseGlobal import *
import Playground, whrandom, State, Actor, ToontownGlobals, DirectNotifyGlobal, Place

class DDPlayground(Playground.Playground):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DDPlayground')

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.cameraSubmerged = -1
        self.toonSubmerged = -1
        self.activityFsm = FSM.FSM('Activity', [
         State.State('off', self.enterOff, self.exitOff, [
          'OnBoat']),
         State.State('OnBoat', self.enterOnBoat, self.exitOnBoat, [
          'off'])], 'off', 'off')
        self.activityFsm.enterInitialState()

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        del self.activityFsm
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        self.nextSeagullTime = 0
        taskMgr.add(self.__seagulls, 'dd-seagulls')
        self.loader.hood.setWhiteFog()
        donald = self.loader.donald
        donald.loop('wheel')
        donald.setZ(3.95)
        donald.setY(-1.0)
        donald.reparentTo(toonbase.tcr.token2nodePath[ToontownGlobals.SPDonaldsBoat])
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('dd-check-toon-underwater')
        taskMgr.remove('dd-check-cam-underwater')
        taskMgr.remove('dd-seagulls')
        self.loader.hood.setNoFog()
        donald = self.loader.donald
        donald.stop()
        donald.reparentTo(hidden)

    def enterStart(self):
        self.cameraSubmerged = 0
        self.toonSubmerged = 0
        taskMgr.add(self.__checkToonUnderwater, 'dd-check-toon-underwater')
        taskMgr.add(self.__checkCameraUnderwater, 'dd-check-cam-underwater')

    def enterDoorOut(self):
        taskMgr.remove('dd-check-toon-underwater')

    def exitDoorOut(self):
        pass

    def enterDoorIn(self, requestStatus):
        Playground.Playground.enterDoorIn(self, requestStatus)
        taskMgr.add(self.__checkToonUnderwater, 'dd-check-toon-underwater')

    def __checkCameraUnderwater(self, task):
        self.notify.debug('__checkCameraUnderwater')
        if camera.getZ(render) < 1.0:
            self.__submergeCamera()
        else:
            self.__emergeCamera()
        return Task.cont

    def __checkToonUnderwater(self, task):
        self.notify.debug('__checkToonUnderwater')
        if toonbase.localToon.getZ() < -2.3314585:
            self.__submergeToon()
        else:
            self.__emergeToon()
        return Task.cont

    def __submergeCamera(self):
        if self.cameraSubmerged == 1:
            return
        self.loader.hood.setUnderwaterFog()
        base.playSfx(self.loader.underwaterSound, looping=1, volume=0.8)
        self.loader.seagullSound.stop()
        taskMgr.remove('dd-seagulls')
        self.cameraSubmerged = 1
        self.walkStateData.setSwimSoundAudible(1)

    def __emergeCamera(self):
        if self.cameraSubmerged == 0:
            return
        self.loader.hood.setWhiteFog()
        self.loader.underwaterSound.stop()
        self.nextSeagullTime = whrandom.random() * 8.0
        taskMgr.add(self.__seagulls, 'dd-seagulls')
        self.cameraSubmerged = 0
        self.walkStateData.setSwimSoundAudible(0)

    def __submergeToon(self):
        self.notify.debug('__submergeToon')
        if self.toonSubmerged == 1:
            return
        base.playSfx(self.loader.submergeSound)
        self.walkStateData.fsm.request('swimming', [self.loader.swimSound])
        pos = toonbase.localToon.getPos(render)
        toonbase.localToon.d_playSplashEffect(pos[0], pos[1], 1.675)
        self.toonSubmerged = 1

    def __emergeToon(self):
        self.notify.debug('__emergeToon')
        if self.toonSubmerged == 0:
            return
        self.walkStateData.fsm.request('walking')
        self.toonSubmerged = 0

    def __seagulls(self, task):
        if task.time < self.nextSeagullTime:
            return Task.cont
        base.playSfx(self.loader.seagullSound)
        self.nextSeagullTime = task.time + whrandom.random() * 4.0 + 8.0
        return Task.cont

    def handleBookClose(self):
        Playground.Playground.handleBookClose(self)
        if self.toonSubmerged == 1:
            self.walkStateData.fsm.request('swimming', [self.loader.swimSound])

    def enterTeleportIn(self, requestStatus):
        self.toonSubmerged = -1
        taskMgr.remove('dd-check-toon-underwater')
        Playground.Playground.enterTeleportIn(self, requestStatus)

    def teleportInDone(self):
        self.notify.debug('teleportInDone')
        self.toonSubmerged = -1
        taskMgr.add(self.__checkToonUnderwater, 'dd-check-toon-underwater')
        Playground.Playground.teleportInDone(self)

    def enterOff(self):
        return None
        return

    def exitOff(self):
        return None
        return

    def enterOnBoat(self):
        boat = toonbase.tcr.token2nodePath[ToontownGlobals.SPDonaldsBoat]
        toonbase.localToon.b_setParent(ToontownGlobals.SPDonaldsBoat)
        base.drive.node().setPos(toonbase.localToon.getPos())
        base.drive.node().setHpr(toonbase.localToon.getHpr())
        base.playSfx(self.loader.waterSound, looping=1)

    def exitOnBoat(self):
        toonbase.localToon.b_setParent(ToontownGlobals.SPRender)
        base.drive.node().setPos(toonbase.localToon.getPos())
        base.drive.node().setHpr(toonbase.localToon.getHpr())
        self.loader.waterSound.stop()