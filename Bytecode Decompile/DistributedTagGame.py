from ShowBaseGlobal import *
from ToonBaseGlobal import *
from DistributedMinigame import *
from IntervalGlobal import *
import FSM, State, Walk, ToontownTimer, OnscreenText, MinigameAvatarScorePanel, DistributedSmoothNode, whrandom, Toon, ToontownGlobals, Localizer, TagGameGlobals, Trajectory

class DistributedTagGame(DistributedMinigame):
    __module__ = __name__
    DURATION = TagGameGlobals.DURATION
    IT_SPEED_INCREASE = 1.3
    IT_ROT_INCREASE = 1.3

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.gameFSM = FSM.FSM('DistributedTagGame', [
         State.State('off', self.enterOff, self.exitOff, [
          'play']),
         State.State('play', self.enterPlay, self.exitPlay, [
          'cleanup']),
         State.State('cleanup', self.enterCleanup, self.exitCleanup, [
          'off'])], 'off', 'off')
        self.addChildGameFSM(self.gameFSM)
        self.walkStateData = Walk.Walk('walkDone')
        self.scorePanels = []
        self.initialPositions = (
         (
          0, 10, 0, 180, 0, 0), (10, 0, 0, 90, 0, 0), (0, -10, 0, 0, 0, 0), (-10, 0, 0, -90, 0, 0))
        toonbase.localToon.isIt = 0
        self.modelCount = 4

    def getTitle(self):
        return Localizer.TagGameTitle

    def getInstructions(self):
        return Localizer.TagGameInstructions

    def getMaxDuration(self):
        return self.DURATION

    def load(self):
        self.notify.debug('load')
        DistributedMinigame.load(self)
        self.itText = OnscreenText.OnscreenText('itText', fg=(0.95, 0.95, 0.65, 1), scale=0.14, font=ToontownGlobals.getSignFont(), pos=(0.0, -0.8), wordwrap=15, mayChange=1)
        self.itText.hide()
        self.sky = loader.loadModel('phase_3.5/models/props/TT_sky')
        self.ground = loader.loadModel('phase_4/models/minigames/tag_arena')
        self.music = base.loadMusic('phase_4/audio/bgm/MG_toontag.mid')
        self.tagSfx = base.loadSfx('phase_4/audio/sfx/MG_Tag_C.mp3')
        self.itPointer = loader.loadModel('phase_4/models/minigames/bboard-pointer')
        self.tracks = []
        self.IT = None
        return

    def unload(self):
        self.notify.debug('unload')
        DistributedMinigame.unload(self)
        self.ignoreAll()
        del self.tracks
        del self.IT
        self.sky.removeNode()
        del self.sky
        self.itPointer.removeNode()
        del self.itPointer
        self.ground.removeNode()
        del self.ground
        del self.music
        del self.tagSfx
        self.itText.cleanup()
        del self.itText
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug('onstage')
        DistributedMinigame.onstage(self)
        self.ground.reparentTo(render)
        self.sky.reparentTo(render)
        myPos = self.avIdList.index(self.localAvId)
        toonbase.localToon.setPosHpr(*self.initialPositions[myPos])
        toonbase.localToon.reparentTo(render)
        toonbase.localToon.loop('neutral')
        camera.reparentTo(render)
        camera.setPosHpr(0, -24, 16, 0, -30, 0)
        base.camLens.setFar(450.0)
        base.transitions.irisIn(0.4)
        NametagGlobals.setMasterArrowsOn(1)
        DistributedSmoothNode.activateSmoothing(1, 1)
        self.IT = None
        return

    def offstage(self):
        self.notify.debug('offstage')
        DistributedSmoothNode.activateSmoothing(1, 0)
        NametagGlobals.setMasterArrowsOn(0)
        DistributedMinigame.offstage(self)
        self.sky.reparentTo(hidden)
        self.ground.reparentTo(hidden)
        base.camLens.setFar(ToontownGlobals.DefaultCameraFar)
        self.itText.hide()

    def setGameReady(self):
        self.notify.debug('setGameReady')
        if DistributedMinigame.setGameReady(self):
            return
        for avId in self.avIdList:
            self.acceptTagEvent(avId)

        myPos = self.avIdList.index(self.localAvId)
        for i in range(self.numPlayers):
            avId = self.avIdList[i]
            avatar = self.getAvatar(avId)
            if avatar:
                avatar.startSmooth()

        toonbase.localToon.setPosHpr(*self.initialPositions[myPos])
        toonbase.localToon.d_clearSmoothing()
        toonbase.localToon.d_setSmPosHpr(*self.initialPositions[myPos])
        toonbase.localToon.b_setAnimState('neutral', 1)
        toonbase.localToon.b_setParent(ToontownGlobals.SPRender)

    def setGameStart(self, timestamp):
        self.notify.debug('setGameStart')
        DistributedMinigame.setGameStart(self, timestamp)
        self.gameFSM.request('play')

    def enterOff(self):
        self.notify.debug('enterOff')

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug('enterPlay')
        for i in range(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId, avName)
            scorePanel.setPos(1.12, 0.0, 0.28 * i - 0.34)
            self.scorePanels.append(scorePanel)

        toonbase.setCellsAvailable(toonbase.rightCells, 0)
        self.walkStateData.enter()
        self.walkStateData.fsm.request('walking')
        if toonbase.localToon.isIt:
            base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSpeed * self.IT_SPEED_INCREASE)
            base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed * self.IT_ROT_INCREASE)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(self.DURATION)
        self.timer.countdown(self.DURATION, self.timerExpired)
        base.playMusic(self.music, looping=1, volume=0.9)
        toonbase.localToon.setIdealCameraPos(Point3(0, -24, 8))

    def exitPlay(self):
        for task in self.tracks:
            task.stop()

        self.tracks = []
        for avId in self.avIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.getGeomNode().clearMat()
                toon.scale = 1.0
                toon.rescaleToon()

        self.walkStateData.exit()
        self.music.stop()
        self.timer.destroy()
        del self.timer
        for panel in self.scorePanels:
            panel.cleanup()

        self.scorePanels = []
        toonbase.setCellsAvailable(toonbase.rightCells, 1)
        base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSpeed)
        base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed)
        self.itPointer.reparentTo(hidden)
        toonbase.localToon.cameraIndex = 0
        toonbase.localToon.setCameraPositionByIndex(0)

    def timerExpired(self):
        self.notify.debug('local timer expired')
        self.gameOver()

    def enterCleanup(self):
        self.notify.debug('enterCleanup')
        self.gameFSM.request('off')

    def exitCleanup(self):
        pass

    def setIt(self, avId):
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.debug('Ignoring setIt after done playing')
            return
        self.itText.show()
        self.notify.debug(str(avId) + ' is now it')
        if avId == self.localAvId:
            self.itText.setText(Localizer.TagGameYouAreIt)
            toonbase.localToon.isIt = 1
            base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSpeed * self.IT_SPEED_INCREASE)
            base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed * self.IT_ROT_INCREASE)
        else:
            self.itText.setText(Localizer.TagGameSomeoneElseIsIt % self.getAvatarName(avId))
            toonbase.localToon.isIt = 0
            base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSpeed)
            base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed)
        avatar = self.getAvatar(avId)
        if avatar:
            self.itPointer.reparentTo(avatar)
            self.itPointer.setZ(avatar.getHeight())
        base.playSfx(self.tagSfx)
        toon = self.getAvatar(avId)
        duration = 0.6
        spinTrack = LerpHprInterval(toon.getGeomNode(), duration, Point3(0, 0, 0), startHpr=Point3(-5.0 * 360.0, 0, 0), blendType='easeOut')
        growTrack = Parallel()
        gs = 2.5
        for hi in range(toon.headParts.getNumPaths()):
            head = toon.headParts[hi]
            growTrack.append(LerpScaleInterval(head, duration, Point3(gs, gs, gs)))

        def bounceFunc(t, trajectory, node=toon.getGeomNode()):
            node.setZ(trajectory.calcZ(t))

        def bounceCleanupFunc(node=toon.getGeomNode(), z=toon.getGeomNode().getZ()):
            node.setZ(z)

        bounceTrack = Sequence()
        startZ = toon.getGeomNode().getZ()
        tLen = 0
        zVel = 30
        decay = 0.6
        while tLen < duration:
            trajectory = Trajectory.Trajectory(0, Point3(0, 0, startZ), Point3(0, 0, zVel), gravMult=5.0)
            dur = trajectory.calcTimeOfImpactOnPlane(startZ)
            if dur <= 0:
                break
            bounceTrack.append(LerpFunctionInterval(bounceFunc, fromData=0.0, toData=dur, duration=dur, extraArgs=[trajectory]))
            tLen += dur
            zVel *= decay

        bounceTrack.append(Func(bounceCleanupFunc))
        tagTrack = Sequence(Func(toon.animFSM.request, 'off'), Parallel(spinTrack, growTrack, bounceTrack), Func(toon.animFSM.request, 'Happy'))
        self.tracks.append(tagTrack)
        tagTrack.start()
        if self.IT:
            it = self.getAvatar(self.IT)
            shrinkTrack = Parallel()
            for hi in range(it.headParts.getNumPaths()):
                head = it.headParts[hi]
                scale = Toon.toonHeadScales[it.style.getAnimal()]
                shrinkTrack.append(LerpScaleInterval(head, duration, scale))

            self.tracks.append(shrinkTrack)
            shrinkTrack.start()
        self.IT = avId

    def acceptTagEvent(self, avId):
        self.accept('enterdistAvatarCollNode-' + str(avId), self.sendTagIfIt, [
         avId])

    def sendTagIfIt(self, avId, collisionEntry):
        if toonbase.localToon.isIt:
            self.notify.debug('Tagging ' + str(avId))
            self.sendUpdate('tag', [avId])
        else:
            self.notify.debug('Bumped ' + str(avId))

    def setTreasureScore(self, scores):
        self.notify.debug('setTreasureScore: %s' % scores)
        for i in range(len(self.scorePanels)):
            self.scorePanels[i].setScore(scores[i])