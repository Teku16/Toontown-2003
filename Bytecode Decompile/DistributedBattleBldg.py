from PandaModules import *
from IntervalGlobal import *
from BattleBase import *
import DistributedBattleBase, DirectNotifyGlobal, MovieUtil, Suit, Actor, SuitBattleGlobals, AvatarDNA, State, Localizer, whrandom, Emote

class DistributedBattleBldg(DistributedBattleBase.DistributedBattleBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleBldg')
    camFOFov = 30.0
    camFOPos = Point3(0, -10, 4)

    def __init__(self, cr):
        townBattle = cr.playGame.getPlace().townBattle
        DistributedBattleBase.DistributedBattleBase.__init__(self, cr, townBattle)
        self.streetBattle = 0
        self.fsm.addState(State.State('BuildingReward', self.enterBuildingReward, self.exitBuildingReward, [
         'Resume']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('BuildingReward')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('BuildingReward')

    def generate(self):
        DistributedBattleBase.DistributedBattleBase.generate(self)

    def setBossBattle(self, value):
        self.bossBattle = value
        if self.bossBattle:
            self.battleMusic = base.loadMusic('phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
        else:
            self.battleMusic = base.loadMusic('phase_7/audio/bgm/encntr_general_bg_indoor.mid')
        base.playMusic(self.battleMusic, looping=1, volume=0.9)

    def disable(self):
        DistributedBattleBase.DistributedBattleBase.disable(self)
        self.battleMusic.stop()

    def delete(self):
        DistributedBattleBase.DistributedBattleBase.delete(self)
        del self.battleMusic

    def buildJoinPointList(self, avPos, destPos, toon=0):
        return []

    def setPosition(self, x, y, z):
        pos = Point3(x, y, z)
        self.setPos(pos)

    def setInitialSuitPos(self, x, y, z):
        pass

    def __faceOff(self, ts, name, callback):
        elevatorPos = self.toons[0].getPos()
        if len(self.suits) == 1:
            leaderIndex = 0
        if self.bossBattle == 1:
            leaderIndex = 1
        maxTypeNum = -1
        for suit in self.suits:
            suitTypeNum = AvatarDNA.getSuitType(suit.dna.name)
            if maxTypeNum < suitTypeNum:
                maxTypeNum = suitTypeNum
                leaderIndex = self.suits.index(suit)

        delay = FACEOFF_TAUNT_T
        suitTracks = []
        suitLeader = None
        for suit in self.suits:
            suit.setState('Battle')
            suitIsLeader = 0
            suitIvals = []
            suitIvals.append(FunctionInterval(suit.loop, extraArgs=['neutral']))
            suitIvals.append(FunctionInterval(suit.headsUp, extraArgs=[elevatorPos]))
            if self.suits.index(suit) == leaderIndex:
                suitLeader = suit
                suitIsLeader = 1
                if self.bossBattle == 1:
                    taunt = Localizer.BattleBldgBossTaunt
                else:
                    taunt = SuitBattleGlobals.getFaceoffTaunt(suit.getStyleName(), suit.doId)
                suitIvals.append(FunctionInterval(suit.setChatAbsolute, extraArgs=[taunt, CFSpeech | CFTimeout]))
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            suitIvals.append(WaitInterval(delay))
            if suitIsLeader == 1:
                suitIvals.append(FunctionInterval(suit.clearChat))
            suitIvals.append(self.createAdjustInterval(suit, destPos, destHpr))
            suitTracks.append(Track(suitIvals))

        suitTrack = Track([MultiTrack(suitTracks)])
        toonTracks = []
        for toon in self.toons:
            toonIvals = []
            destPos, destHpr = self.getActorPosHpr(toon, self.toons)
            toonIvals.append((delay,
             self.createAdjustInterval(toon, destPos, destHpr, toon=1, run=1)))
            toonTracks.append(Track(toonIvals))

        toonTrack = Track([MultiTrack(toonTracks)])
        camIvals = []

        def setCamFov(fov):
            base.camLens.setFov(fov)

        camIvals.append(FunctionInterval(camera.wrtReparentTo, extraArgs=[suitLeader]))
        camIvals.append(FunctionInterval(setCamFov, extraArgs=[self.camFOFov]))
        suitHeight = suitLeader.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)
        MidTauntCamHeight = suitHeight * 0.66
        MidTauntCamHeightLim = suitHeight - 1.8
        if MidTauntCamHeight < MidTauntCamHeightLim:
            MidTauntCamHeight = MidTauntCamHeightLim
        TauntCamY = 18
        TauntCamX = 0
        TauntCamHeight = whrandom.choice((MidTauntCamHeight, 1, 11))
        camIvals.append(FunctionInterval(camera.setPos, extraArgs=[TauntCamX, TauntCamY, TauntCamHeight]))
        camIvals.append(FunctionInterval(camera.lookAt, extraArgs=[suitLeader, suitOffsetPnt]))
        camIvals.append(WaitInterval(delay))
        camPos = Point3(0, -6, 4)
        camHpr = Vec3(0, 0, 0)
        camIvals.append(FunctionInterval(camera.reparentTo, extraArgs=[toonbase.localToon]))
        camIvals.append(FunctionInterval(setCamFov, extraArgs=[DefaultCameraFov]))
        camIvals.append(FunctionInterval(camera.setPosHpr, extraArgs=[camPos, camHpr]))
        camTrack = Track(camIvals)
        mtrack = MultiTrack([suitTrack, toonTrack, camTrack])
        done = FunctionInterval(callback)
        track = Track([mtrack, done], name)
        track.start(ts)
        self.activeIntervals[name] = track
        return

    def enterFaceOff(self, ts):
        if len(self.toons) > 0 and toonbase.localToon == self.toons[0]:
            Emote.DisableAll(self.toons[0], 'dbattlebldg, enterFaceOff')
        self.delayDeleteToons()
        self.__faceOff(ts, self.faceOffName, self.__handleFaceOffDone)
        return None
        return

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        self.d_faceOffDone(toonbase.localToon.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if len(self.toons) > 0 and toonbase.localToon == self.toons[0]:
            Emote.ReleaseAll(self.toons[0], 'dbattlebldg exitFaceOff')
        self.toonsKeep = None
        self.clearInterval(self.faceOffName)
        camera.wrtReparentTo(self)
        base.camLens.setFov(self.camFov)
        return None
        return

    def __playReward(self, ts, callback):
        toonTracks = Parallel()
        for toon in self.toons:
            toonTracks.append(Sequence(Func(toon.loop, 'victory'), Wait(FLOOR_REWARD_TIMEOUT), Func(toon.loop, 'neutral')))

        name = self.uniqueName('floorReward')
        track = Sequence(toonTracks, Func(callback), name=name)
        camera.setPos(0, 0, 1)
        camera.setHpr(180, 10, 0)
        self.activeIntervals[name] = track
        track.play(ts)

    def enterReward(self, ts):
        self.notify.debug('enterReward()')
        self.delayDeleteToons()
        self.__playReward(ts, self.__handleFloorRewardDone)
        return None
        return

    def __handleFloorRewardDone(self):
        return None
        return

    def exitReward(self):
        self.notify.debug('exitReward()')
        self.clearInterval(self.uniqueName('floorReward'))
        self.toonsKeep = None
        NametagGlobals.setMasterArrowsOn(1)
        for toon in self.toons:
            toon.startSmooth()

        return None
        return

    def enterBuildingReward(self, ts):
        self.delayDeleteToons()
        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
        self.movie.playReward(ts, self.uniqueName('building-reward'), self.__handleBuildingRewardDone)
        return None
        return

    def __handleBuildingRewardDone(self):
        if self.hasLocalToon():
            self.d_rewardDone(toonbase.localToon.doId)
        self.movie.resetReward()
        self.fsm.request('Resume')

    def exitBuildingReward(self):
        self.toonsKeep = None
        self.movie.resetReward(finish=1)
        NametagGlobals.setMasterArrowsOn(1)
        return None
        return

    def enterResume(self, ts=0):
        if self.hasLocalToon():
            self.removeLocalToon()
        return None
        return

    def exitResume(self):
        return None
        return