from PandaModules import *
from IntervalGlobal import *
from ClockDelta import *
import StateData, DirectNotifyGlobal, CCharPaths, ToontownGlobals

class CharNeutralState(StateData.StateData):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CharNeutralState')

    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character

    def enter(self, startTrack=None, playRate=None):
        StateData.StateData.enter(self)
        self.notify.debug('Neutral ' + self.character.getName() + '...')
        self.__neutralTrack = Sequence(name=self.character.getName() + '-neutral')
        if startTrack:
            self.__neutralTrack.append(startTrack)
        if playRate:
            self.__neutralTrack.append(Func(self.character.setPlayRate, playRate, 'neutral'))
        self.__neutralTrack.append(Func(self.character.loop, 'neutral'))
        self.__neutralTrack.play()

    def exit(self):
        StateData.StateData.exit(self)
        self.__neutralTrack.stop()
        self.__neutralTrack.setFinalT()

    def __doneHandler(self):
        doneStatus = {}
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done


class CharWalkState(StateData.StateData):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CharWalkState')

    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character
        self.paths = CCharPaths.getPaths(character.getName())
        self.speed = character.walkSpeed()

    def enter(self, startTrack=None, playRate=None):
        StateData.StateData.enter(self)
        self.notify.debug('Walking ' + self.character.getName() + '... from ' + str(self.__walkInfo[0]) + ' to ' + str(self.__walkInfo[1]))
        posPoints = CCharPaths.getPointsFromTo(self.__walkInfo[0], self.__walkInfo[1], self.paths)
        self.__walkTrack = Sequence(name=self.character.getName() + '-walk')
        if startTrack:
            self.__walkTrack.append(startTrack)
        self.character.setPos(posPoints[0])
        raycast = CCharPaths.getRaycastFlag(self.__walkInfo[0], self.__walkInfo[1], self.paths)
        moveTrack = self.__makePathTrack(self.character, posPoints, self.speed, raycast)
        if playRate:
            self.__walkTrack.append(Func(self.character.setPlayRate, playRate, 'walk'))
        self.__walkTrack.append(Func(self.character.loop, 'walk'))
        self.__walkTrack.append(moveTrack)
        doneEventName = self.character.getName() + 'WalkDone'
        self.__walkTrack.append(Func(messenger.send, doneEventName))
        ts = globalClockDelta.localElapsedTime(self.__walkInfo[2])
        self.accept(doneEventName, self.__doneHandler)
        self.notify.debug('walkTrack.play(%s)' % ts)
        self.__walkTrack.play(ts)

    def __makePathTrack(self, nodePath, posPoints, velocity, raycast=0):
        track = Sequence()
        if raycast:
            track.append(Func(nodePath.enableRaycast, 1))
        startHpr = nodePath.getHpr()
        for pointIndex in range(len(posPoints) - 1):
            startPoint = posPoints[pointIndex]
            endPoint = posPoints[pointIndex + 1]
            track.append(Func(nodePath.setPos, startPoint))
            distance = Vec3(endPoint - startPoint).length()
            duration = distance / velocity
            curHpr = nodePath.getHpr()
            nodePath.headsUp(endPoint[0], endPoint[1], endPoint[2])
            destHpr = nodePath.getHpr()
            reducedCurH = reduceAngle(curHpr[0])
            reducedCurHpr = Vec3(reducedCurH, curHpr[1], curHpr[2])
            reducedDestH = reduceAngle(destHpr[0])
            shortestAngle = closestDestAngle(reducedCurH, reducedDestH)
            shortestHpr = Vec3(shortestAngle, destHpr[1], destHpr[2])
            turnTime = abs(shortestAngle) / 270.0
            nodePath.setHpr(shortestHpr)
            if duration - turnTime > 0.01:
                track.append(Parallel(Func(nodePath.loop, 'walk'), LerpHprInterval(nodePath, turnTime, shortestHpr, startHpr=reducedCurHpr, name='lerp' + nodePath.getName() + 'Hpr'), LerpPosInterval(nodePath, duration=duration - turnTime, pos=Point3(endPoint), startPos=Point3(startPoint))))

        nodePath.setHpr(startHpr)
        if raycast:
            track.append(Func(nodePath.enableRaycast, 0))
        return track

    def __doneHandler(self):
        doneStatus = {}
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done

    def exit(self):
        StateData.StateData.exit(self)
        self.ignore(self.character.getName() + 'WalkDone')
        self.__walkTrack.stop()
        self.__walkTrack.setFinalT()

    def setWalk(self, srcNode, destNode, timestamp):
        self.__walkInfo = (
         srcNode, destNode, timestamp)