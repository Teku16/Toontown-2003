from PandaModules import *
from IntervalGlobal import *
from BattleBase import *
import ToontownGlobals, ToontownBattleGlobals, DistributedBattleBase, CollisionSphere, CollisionNode, DirectNotifyGlobal, MovieUtil, Suit, Actor, Emote, SuitBattleGlobals, whrandom

class DistributedBattle(DistributedBattleBase.DistributedBattleBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattle')
    camFOFov = ToontownBattleGlobals.BattleCamFaceOffFov
    camFOPos = ToontownBattleGlobals.BattleCamFaceOffPos

    def __init__(self, cr):
        townBattle = cr.playGame.hood.loader.townBattle
        DistributedBattleBase.DistributedBattleBase.__init__(self, cr, townBattle)
        self.__setupCollisions(self.uniqueBattleName('battle-collide'))

    def generate(self):
        DistributedBattleBase.DistributedBattleBase.generate(self)

    def disable(self):
        DistributedBattleBase.DistributedBattleBase.disable(self)

    def delete(self):
        DistributedBattleBase.DistributedBattleBase.delete(self)
        self.__removeCollisionData()

    def setPosition(self, x, y, z):
        self.notify.debug('setPosition() - %d %d %d' % (x, y, z))
        pos = Point3(x, y, -0.475)
        self.setPos(pos)

    def setInitialSuitPos(self, x, y, z):
        self.initialSuitPos = Point3(x, y, z)
        self.headsUp(self.initialSuitPos)

    def setMembers(self, suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, timestamp):
        oldtoons = DistributedBattleBase.DistributedBattleBase.setMembers(self, suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, timestamp)
        if len(self.toons) == 4 and len(oldtoons) < 4:
            self.notify.debug('setMembers() - battle is now full of toons')
            self.__closeBattleCollision()
        else:
            if len(self.toons) < 4 and len(oldtoons) == 4:
                self.__openBattleCollision()

    def __setupCollisions(self, name):
        self.cSphere = CollisionSphere.CollisionSphere(0.0, 0.0, 0.0, 9.0)
        self.cSphereNode = CollisionNode.CollisionNode(name)
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.reparentTo(hidden)
        self.cSphereNodePath.hide()
        self.cSphereBitMask = ToontownGlobals.WallBitmask
        self.cSphereNode.setCollideMask(self.cSphereBitMask)
        self.cSphere.setTangible(0)

    def __removeCollisionData(self):
        del self.cSphere
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        del self.cSphereNode
        self.cSphereBitMask = None
        return

    def __enableCollision(self):
        self.cSphereNodePath.reparentTo(self)
        if len(self.toons) < 4:
            self.accept('enter' + self.cSphereNode.getName(), self.__handleLocalToonCollision)

    def __handleLocalToonCollision(self, collEntry):
        self.notify.debug('localToonCollision')
        toonbase.tcr.playGame.getPlace().setState('WaitForBattle')
        toon = toonbase.localToon
        self.d_toonRequestJoin(toon.doId, toon.getPos(self))
        toonbase.localToon.preBattleHpr = toonbase.localToon.getHpr(render)
        self.localToonFsm.request('WaitForServer')

    def denyLocalToonJoin(self):
        self.notify.debug('denyLocalToonJoin()')
        toonbase.tcr.playGame.getPlace().setState('walk')
        self.localToonFsm.request('NoLocalToon')

    def __disableCollision(self):
        self.ignore('enter' + self.cSphereNode.getName())
        self.cSphereNodePath.reparentTo(hidden)

    def __openBattleCollision(self):
        self.cSphere.setTangible(0)
        if not self.hasLocalToon():
            self.__enableCollision()

    def __closeBattleCollision(self):
        self.cSphere.setTangible(1)
        self.ignore('enter' + self.cSphereNode.getName())

    def __faceOff(self, ts, name, callback):
        if len(self.suits) == 0:
            self.notify.warning('__faceOff(): no suits.')
            return
        if len(self.toons) == 0:
            self.notify.warning('__faceOff(): no toons.')
            return
        suit = self.suits[0]
        point = self.suitPoints[0][0]
        suitPos = point[0]
        suitHpr = VBase3(point[1], 0.0, 0.0)
        toon = self.toons[0]
        point = self.toonPoints[0][0]
        toonPos = point[0]
        toonHpr = VBase3(point[1], 0.0, 0.0)
        suit.setState('Battle')
        suitIvals = []
        toonIvals = []
        camIvals = []
        suitIvals.append(FunctionInterval(suit.loop, extraArgs=['neutral']))
        suitIvals.append(FunctionInterval(suit.headsUp, extraArgs=[toon.getPos()]))
        taunt = SuitBattleGlobals.getFaceoffTaunt(suit.getStyleName(), suit.doId)
        suitIvals.append(FunctionInterval(suit.setChatAbsolute, extraArgs=[taunt, CFSpeech | CFTimeout]))
        toonIvals.append(FunctionInterval(toon.loop, extraArgs=['neutral']))
        toonIvals.append(FunctionInterval(toon.headsUp, extraArgs=[suit.getPos()]))

        def setCamFov(fov):
            base.camLens.setFov(fov)

        camIvals.append(FunctionInterval(camera.wrtReparentTo, extraArgs=[suit]))
        camIvals.append(FunctionInterval(setCamFov, extraArgs=[self.camFOFov]))
        suitHeight = suit.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)
        MidTauntCamHeight = suitHeight * 0.66
        MidTauntCamHeightLim = suitHeight - 1.8
        if MidTauntCamHeight < MidTauntCamHeightLim:
            MidTauntCamHeight = MidTauntCamHeightLim
        TauntCamY = 16
        TauntCamX = whrandom.choice((-5, 5))
        TauntCamHeight = whrandom.choice((MidTauntCamHeight, 1, 11))
        camIvals.append(FunctionInterval(camera.setPos, extraArgs=[TauntCamX, TauntCamY, TauntCamHeight]))
        camIvals.append(FunctionInterval(camera.lookAt, extraArgs=[suit, suitOffsetPnt]))
        delay = FACEOFF_TAUNT_T
        camIvals.append(WaitInterval(delay))
        sFaceSpot = FunctionInterval(suit.headsUp, extraArgs=[self, suitPos])
        suitIvals.append((delay, sFaceSpot))
        suitIvals.append(FunctionInterval(suit.clearChat))
        tFaceSpot = FunctionInterval(toon.headsUp, extraArgs=[self, toonPos])
        toonIvals.append((delay, tFaceSpot))
        faceoffTime = self.calcFaceoffTime(self.getPos(), self.initialSuitPos)
        fromBattle = Vec3(self.getPos() - self.initialSuitPos)
        distance = fromBattle.length()
        if distance > MAX_EXPECTED_DISTANCE_FROM_BATTLE:
            try:
                zoneId = toonbase.tcr.playGame.getPlace().getZoneId()
                zoneStr = str(zoneId)
            except:
                zoneStr = 'Unknown'
            else:
                self.notify.warning('WARNING: Possible missing battle cell in zone ' + zoneStr + '!!')
                toonbase.tcr.timeManager.synchronize('Suit is %0.1f ft from battle cell.' % distance)
        suitIvals.append(FunctionInterval(suit.loop, extraArgs=['walk']))
        suitIvals.append(LerpPosInterval(suit, faceoffTime, suitPos, other=self))
        suitIvals.append(FunctionInterval(suit.loop, extraArgs=['neutral']))
        suitIvals.append(FunctionInterval(suit.setHpr, extraArgs=[self, suitHpr]))
        toonIvals.append(FunctionInterval(toon.loop, extraArgs=['run']))
        toonIvals.append(LerpPosInterval(toon, faceoffTime, toonPos, other=self))
        toonIvals.append(FunctionInterval(toon.loop, extraArgs=['neutral']))
        toonIvals.append(FunctionInterval(toon.setHpr, extraArgs=[self, toonHpr]))
        camIvals.append(FunctionInterval(setCamFov, extraArgs=[self.camFov]))
        camIvals.append(FunctionInterval(camera.wrtReparentTo, extraArgs=[self]))
        camIvals.append(FunctionInterval(camera.setPos, extraArgs=[self.camFOPos]))
        camIvals.append(FunctionInterval(camera.lookAt, extraArgs=[suit.getPos(self)]))
        camIvals.append(WaitInterval(faceoffTime))
        if toonbase.localToon == toon:
            soundTrack = Track((WaitInterval(delay), SoundInterval(toonbase.localToon.soundRun, loop=1, duration=faceoffTime, node=toonbase.localToon)))
        else:
            soundTrack = WaitInterval(faceoffTime + delay)
        suitTrack = Track(suitIvals)
        toonTrack = Track(toonIvals)
        camTrack = Track(camIvals)
        mtrack = MultiTrack([suitTrack, toonTrack, soundTrack])
        done = FunctionInterval(callback)
        track = Track([mtrack, done], name)
        track.start(ts)
        self.activeIntervals[name] = track
        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
            camTrack.start(ts)

    def enterFaceOff(self, ts):
        self.notify.debug('enterFaceOff()')
        self.delayDeleteToons()
        if len(self.toons) > 0 and toonbase.localToon == self.toons[0]:
            Emote.DisableAll(self.toons[0], 'dbattle, enterFaceOff')
        self.__faceOff(ts, self.faceOffName, self.__handleFaceOffDone)
        return None
        return

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        if len(self.toons) > 0 and toonbase.localToon == self.toons[0]:
            self.d_faceOffDone(toonbase.localToon.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if len(self.toons) > 0 and toonbase.localToon == self.toons[0]:
            Emote.ReleaseAll(self.toons[0], 'dbattle exitFaceOff')
        self.toonsKeep = None
        self.finishInterval(self.faceOffName)
        return None
        return

    def enterReward(self, ts):
        self.notify.debug('enterReward()')
        self.__disableCollision()
        self.delayDeleteToons()
        for toon in self.toons:
            Emote.DisableAll(toon, 'dbattle, enterReward')

        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
            if self.localToonActive() == 0:
                self.removeInactiveLocalToon(toonbase.localToon)
        for toon in self.toons:
            toon.startSmooth()

        self.accept('resumeAfterReward', self.handleResumeAfterReward)
        self.playReward(ts)
        return None
        return

    def playReward(self, ts):
        self.movie.playReward(ts, self.uniqueName('reward'), self.handleRewardDone)

    def handleRewardDone(self):
        self.notify.debug('Reward done')
        if self.hasLocalToon():
            self.d_rewardDone(toonbase.localToon.doId)
        self.movie.resetReward()
        messenger.send('resumeAfterReward')

    def handleResumeAfterReward(self):
        self.fsm.request('Resume')

    def exitReward(self):
        self.notify.debug('exitReward()')
        self.ignore('resumeAfterReward')
        self.toonsKeep = None
        self.movie.resetReward(finish=1)
        NametagGlobals.setMasterArrowsOn(1)
        for toon in self.toons:
            Emote.ReleaseAll(toon, 'dbattle exitReward')

        return None
        return

    def enterResume(self, ts=0):
        self.notify.debug('enterResume()')
        if self.hasLocalToon():
            self.removeLocalToon()
        return None
        return

    def exitResume(self):
        return None
        return

    def enterNoLocalToon(self):
        self.notify.debug('enterNoLocalToon()')
        self.__enableCollision()
        return None
        return

    def exitNoLocalToon(self):
        self.__disableCollision()
        return None
        return

    def enterWaitForServer(self):
        self.notify.debug('enterWaitForServer()')
        return None
        return

    def exitWaitForServer(self):
        return None
        return