from ShowBaseGlobal import *
from ToonBaseGlobal import *
from ToontownGlobals import *
from DirectGui import *
from ClockDelta import *
import Place, DirectNotifyGlobal, FSM, State, Localizer, random, PythonUtil, Place, SkyUtil, HouseGlobals

class Estate(Place.Place):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('Estate')

    def __init__(self, loader, avId, zoneId, parentFSMState, doneEvent):
        Place.Place.__init__(self, None, doneEvent)
        self.id = MyEstate
        self.avId = avId
        self.zoneId = zoneId
        self.loader = loader
        self.cameraSubmerged = -1
        self.toonSubmerged = -1
        self.fsm = FSM.FSM('Estate', [
         State.State('init', self.enterInit, self.exitInit, [
          'final', 'teleportIn', 'doorIn', 'walk']),
         State.State('walk', self.enterWalk, self.exitWalk, [
          'final', 'stickerBook', 'options', 'quest', 'fishing', 'DFA', 'doorOut']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, [
          'walk', 'DFA']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, [
          'walk']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, [
          'teleportIn', 'final']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, [
          'walk']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, [
          'final', 'walk']),
         State.State('final', self.enterFinal, self.exitFinal, [
          'teleportIn']),
         State.State('quest', self.enterQuest, self.exitQuest, [
          'walk']),
         State.State('fishing', self.enterFishing, self.exitFishing, [
          'walk']),
         State.State('DFA', self.enterDFA, self.exitDFA, [
          'DFAReject', 'teleportOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, [
          'walk'])], 'init', 'final')
        self.fsm.enterInitialState()
        self.doneEvent = doneEvent
        self.parentFSMState = parentFSMState
        return

    def delete(self):
        self.unload()

    def load(self):
        Place.Place.load(self)
        self.fog = Fog('EstateFog')
        taskMgr.add(self.__checkCameraUnderwater, 'estate-check-cam-underwater')
        self.parentFSMState.addChild(self.fsm)

    def unload(self):
        self.ignoreAll()
        self.parentFSMState.removeChild(self.fsm)
        del self.fsm
        taskMgr.remove('estate-check-toon-underwater')
        taskMgr.remove('estate-check-cam-underwater')
        self.fog = None
        if self.loader:
            self.loader.stopSky()
        Place.Place.unload(self)
        return

    def enter(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        self.loader.startSky()
        self.loader.sky.setFogOff()
        self.__setFaintFog()
        for i in self.loader.nodeList:
            self.loader.enterAnimatedProps(i)

        self.loader.geom.reparentTo(render)
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        self.fsm.request(requestStatus['how'], [requestStatus])

    def exit(self):
        toonbase.localToon.stopChat()
        self.loader.geom.reparentTo(hidden)
        for i in self.loader.nodeList:
            self.loader.exitAnimatedProps(i)

        self.loader.stopSky()
        render.setFogOff()

    def __setZoneId(self, zoneId):
        self.zoneId = zoneId

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def enterTeleportIn(self, requestStatus):
        try:
            houseDo = toonbase.tcr.doId2do.get(toonbase.localToon.houseId)
            house = houseDo.house
            pos = house.getPos(render)
            toonbase.localToon.reparentTo(hidden)
            toonbase.localToon.setPosHpr(house, 17, 3, 0, 125, 0, 0)
        except:
            x, y, z, h, p, r = HouseGlobals.defaultEntryPoint
            toonbase.localToon.reparentTo(hidden)
            toonbase.localToon.setPosHpr(render, x, y, z, h, p, r)

        self.toonSubmerged = -1
        taskMgr.remove('estate-check-toon-underwater')
        Place.Place.enterTeleportIn(self, requestStatus)

    def teleportInDone(self):
        self.notify.debug('teleportInDone')
        self.toonSubmerged = -1
        taskMgr.add(self.__checkToonUnderwater, 'estate-check-toon-underwater')
        Place.Place.teleportInDone(self)

    def enterTeleportOut(self, requestStatus):
        Place.Place.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        avId = requestStatus['avId']
        shardId = requestStatus['shardId']
        if hoodId == ToontownGlobals.MyEstate and zoneId == self.getZoneId() and shardId == None:
            self.fsm.request('teleportIn', [requestStatus])
        else:
            if hoodId == ToontownGlobals.MyEstate and shardId == None:
                self.doneStatus = requestStatus
                self.getEstateZoneAndGoHome(requestStatus)
            else:
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent, [self.doneStatus])
        return

    def handleBookClose(self):
        Place.Place.handleBookClose(self)
        if self.toonSubmerged == 1:
            self.walkStateData.fsm.request('swimming', [self.loader.swimSound])

    def goHomeFailed(self, task):
        self.notifyUserGoHomeFailed()
        self.ignore('setLocalEstateZone')
        self.doneStatus['avId'] = -1
        self.doneStatus['zoneId'] = self.getZoneId()
        self.fsm.request('teleportIn', [self.doneStatus])
        return Task.done

    def exitTeleportOut(self):
        Place.Place.exitTeleportOut(self)

    def exitDoorIn(self):
        self.toonSubmerged = -1
        taskMgr.add(self.__checkToonUnderwater, 'estate-check-toon-underwater')
        Place.Place.exitDoorIn(self)

    def getZoneId(self):
        if self.zoneId:
            return self.zoneId
        else:
            self.notify.warning('no zone id available')

    def __checkCameraUnderwater(self, task):
        if camera.getZ(render) < -1.2:
            self.__submergeCamera()
        else:
            self.__emergeCamera()
        return Task.cont

    def __checkToonUnderwater(self, task):
        if toonbase.localToon.getZ() < -4.0:
            self.__submergeToon()
        else:
            self.__emergeToon()
        return Task.cont

    def __submergeCamera(self):
        if self.cameraSubmerged == 1:
            return
        self.__setUnderwaterFog()
        base.playSfx(self.loader.underwaterSound, looping=1, volume=0.8)
        self.cameraSubmerged = 1
        self.walkStateData.setSwimSoundAudible(1)

    def __emergeCamera(self):
        if self.cameraSubmerged == 0:
            return
        self.loader.underwaterSound.stop()
        self.loader.sky.setFogOff()
        self.__setFaintFog()
        self.cameraSubmerged = 0
        self.walkStateData.setSwimSoundAudible(0)

    def forceUnderWater(self):
        self.toonSubmerged = 0
        self.__submergeToon()

    def __submergeToon(self):
        if self.toonSubmerged == 1:
            return
        base.playSfx(self.loader.submergeSound)
        self.walkStateData.fsm.request('swimming', [self.loader.swimSound])
        pos = toonbase.localToon.getPos(render)
        toonbase.localToon.d_playSplashEffect(pos[0], pos[1], -2.3)
        self.toonSubmerged = 1

    def __emergeToon(self):
        if self.toonSubmerged == 0:
            return
        self.walkStateData.fsm.request('walking')
        self.toonSubmerged = 0

    def __setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.0, 0.0, 0.6, 1.0))
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            self.loader.sky.setFog(self.fog)

    def __setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
            self.fog.setLinearRange(0.0, 400.0)
            render.setFog(self.fog)
            self.loader.sky.setFog(self.fog)

    def __setFaintFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
            self.fog.setLinearRange(0.0, 700.0)
            render.setFog(self.fog)