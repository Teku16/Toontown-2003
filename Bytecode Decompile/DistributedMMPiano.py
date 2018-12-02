from ShowBaseGlobal import *
from PandaObject import *
from ClockDelta import *
from IntervalGlobal import *
import DistributedObject, NodePath, ToontownGlobals
ChangeDirectionDebounce = 1.0
ChangeDirectionTime = 1.0

class DistributedMMPiano(DistributedObject.DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.spinStartTime = 0.0
        self.rpm = 0.0
        self.degreesPerSecond = self.rpm / 60.0 * 360.0
        self.offset = 0.0
        self.oldOffset = 0.0
        self.lerpStart = 0.0
        self.lerpFinish = 1.0
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.lastChangeDirection = 0.0
        return

    def generate(self):
        self.accept('on-floor', self.__handleOnFloor)
        self.accept('off-floor', self.__handleOffFloor)
        self.accept('entero7', self.__handleChangeDirectionButton)
        self.speedUpSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.mp3')
        self.changeDirectionSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_cymbal.mp3')
        self.__setupSpin()
        DistributedObject.DistributedObject.generate(self)

    def __setupSpin(self):
        taskMgr.add(self.__updateSpin, self.taskName('pianoSpinTask'))

    def __stopSpin(self):
        taskMgr.remove(self.taskName('pianoSpinTask'))

    def __updateSpin(self, task):
        piano = toonbase.tcr.token2nodePath[ToontownGlobals.SPMinniesPiano]
        now = globalClock.getFrameTime()
        if now > self.lerpFinish:
            offset = self.offset
        else:
            if now > self.lerpStart:
                t = (now - self.lerpStart) / (self.lerpFinish - self.lerpStart)
                offset = self.oldOffset + t * (self.offset - self.oldOffset)
            else:
                offset = self.oldOffset
        heading = self.degreesPerSecond * (now - self.spinStartTime) + offset
        piano.setHprScale(heading % 360.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        return Task.cont

    def disable(self):
        self.ignore('on-floor')
        self.ignore('off-floor')
        self.ignore('entero7')
        self.ignore('entericon_center_collisions')
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.__stopSpin()
        DistributedObject.DistributedObject.disable(self)
        return

    def setSpeed(self, rpm, offset, timestamp):
        timestamp = globalClockDelta.networkToLocalTime(timestamp)
        degreesPerSecond = rpm / 60.0 * 360.0
        now = globalClock.getFrameTime()
        oldHeading = self.degreesPerSecond * (now - self.spinStartTime) + self.offset
        oldHeading = oldHeading % 360.0
        oldOffset = oldHeading - degreesPerSecond * (now - timestamp)
        self.rpm = rpm
        self.degreesPerSecond = degreesPerSecond
        self.offset = offset
        self.spinStartTime = timestamp
        while oldOffset - offset < -180.0:
            oldOffset += 360.0

        while oldOffset - offset > 180.0:
            oldOffset -= 360.0

        self.oldOffset = oldOffset
        self.lerpStart = now
        self.lerpFinish = timestamp + ChangeDirectionTime

    def playSpeedUp(self, avId):
        if avId != toonbase.localToon.doId:
            base.playSfx(self.speedUpSound)

    def playChangeDirection(self, avId):
        if avId != toonbase.localToon.doId:
            base.playSfx(self.changeDirectionSound)

    def __handleOnFloor(self, collEntry):
        if collEntry.getIntoNode().getName() == 'large_round_keyboard_collisions':
            self.cr.playGame.getPlace().activityFsm.request('OnPiano')
            self.sendUpdate('requestSpeedUp', [])
            base.playSfx(self.speedUpSound)

    def __handleOffFloor(self, collEntry):
        if collEntry.getIntoNode().getName() == 'large_round_keyboard_collisions':
            self.cr.playGame.getPlace().activityFsm.request('off')

    def __handleSpeedUpButton(self, collEntry):
        self.sendUpdate('requestSpeedUp', [])
        base.playSfx(self.speedUpSound)

    def __handleChangeDirectionButton(self, collEntry):
        now = globalClock.getFrameTime()
        if now - self.lastChangeDirection < ChangeDirectionDebounce:
            return
        self.lastChangeDirection = now
        self.sendUpdate('requestChangeDirection', [])
        base.playSfx(self.changeDirectionSound)