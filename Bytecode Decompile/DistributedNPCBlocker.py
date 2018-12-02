from ShowBaseGlobal import *
from DistributedNPCToonBase import *
from DirectGui import *
from PandaModules import *
import NPCToons, Localizer, DistributedObject, QuestParser

class DistributedNPCBlocker(DistributedNPCToonBase):
    __module__ = __name__

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.cSphereNodePath.setScale(4.0, 1.0, 1.0)
        self.isLocalToon = 1
        self.movie = None
        return

    def announceGenerate(self):
        self.setAnimState('neutral', 0.9, None, None)
        posh = NPCToons.BlockerPositions[self.name]
        self.setPos(posh[0])
        self.setH(posh[1])
        DistributedObject.DistributedObject.announceGenerate(self)
        return

    def disable(self):
        if self.movie:
            self.movie.cleanup()
            del self.movie
            if self.isLocalToon == 1:
                toonbase.localToon.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        toonbase.tcr.playGame.getPlace().fsm.request('quest', [self])
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')

    def resetBlocker(self):
        self.cSphereNode.setCollideMask(BitMask32())
        if self.movie:
            self.movie.cleanup()
            self.movie = None
        if self.isLocalToon == 1:
            toonbase.localToon.posCamera(0, 0)
            self.freeAvatar()
            self.isLocalToon = 0
        self.startLookAround()
        self.clearMat()
        return

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.npcId = npcId
        self.isLocalToon = avId == toonbase.localToon.doId
        if mode == NPCToons.BLOCKER_MOVIE_CLEAR:
            return
        else:
            if mode == NPCToons.BLOCKER_MOVIE_START:
                self.movie = QuestParser.NPCMoviePlayer('tutorial_blocker', toonbase.localToon, self)
                self.movie.play()
            else:
                if mode == NPCToons.BLOCKER_MOVIE_TIMEOUT:
                    return
        return

    def finishMovie(self, av, isLocalToon, elapsedTime):
        self.resetBlocker()