from ShowBaseGlobal import *
from IntervalGlobal import *
import Avatar, AvatarDNA, DistributedChar, DirectNotifyGlobal, FSM, State, ToontownGlobals, CCharChatter, CCharPaths, string, copy

class DistributedCCharBase(DistributedChar.DistributedChar):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCCharBase')

    def __init__(self, cr, name, dnaName):
        try:
            self.DistributedCCharBase_initialized
        except:
            self.DistributedCCharBase_initialized = 1
            DistributedChar.DistributedChar.__init__(self, cr)
            dna = AvatarDNA.AvatarDNA()
            dna.newChar(dnaName)
            self.setDNA(dna)
            self.setName(name)
            self.__initCollisions()

    def __initCollisions(self):
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, 8.0)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode(self.getName() + 'BlatherSphere')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.acceptOnce('enter' + self.cSphereNode.getName(), self.__handleCollisionSphereEnter)
        self.cRay = CollisionRay(0.0, 0.0, 10.0, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode(self.getName() + 'cRay')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        self.lifter.setMaxVelocity(0.0)
        self.lifter.addColliderNode(self.cRayNode, self.node())
        self.cTrav = toonbase.localToon.cTrav

    def __deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None
        self.cTrav = None
        return

    def disable(self):
        self.stopBlink()
        self.ignoreAll()
        self.chatTrack.stop()
        del self.chatTrack
        DistributedChar.DistributedChar.disable(self)
        self.stopEarTask()

    def delete(self):
        try:
            self.DistributedCCharBase_deleted
        except:
            self.DistributedCCharBase_deleted = 1
            self.__deleteCollisions()
            DistributedChar.DistributedChar.delete(self)

    def generate(self):
        DistributedChar.DistributedChar.generate(self)
        self.setPos(CCharPaths.getNodePos(CCharPaths.startNode, CCharPaths.getPaths(self.getName())))
        self.setHpr(0, 0, 0)
        self.setParent(ToontownGlobals.SPRender)
        self.startBlink()
        self.startEarTask()
        self.chatTrack = Sequence()
        self.acceptOnce('enter' + self.cSphereNode.getName(), self.__handleCollisionSphereEnter)
        self.accept('exitSafeZone', self.__handleExitSafeZone)

    def __handleExitSafeZone(self):
        self.__handleCollisionSphereExit(None)
        return

    def __handleCollisionSphereEnter(self, collEntry):
        self.notify.debug('Entering collision sphere...')
        self.sendUpdate('avatarEnter', [])
        self.accept('chatUpdate', self.__handleChatUpdate)
        self.accept('chatUpdateQT', self.__handleChatUpdateQT)
        self.accept('chatUpdateQTQuest', self.__handleChatUpdateQTQuest)
        self.acceptOnce('exit' + self.cSphereNode.getName(), self.__handleCollisionSphereExit)

    def __handleCollisionSphereExit(self, collEntry):
        self.notify.debug('Exiting collision sphere...')
        self.sendUpdate('avatarExit', [])
        self.ignore('chatUpdate')
        self.ignore('chatUpdateQT')
        self.ignore('chatUpdateQTQuest')
        self.acceptOnce('enter' + self.cSphereNode.getName(), self.__handleCollisionSphereEnter)

    def __handleChatUpdate(self, msg, chatFlags):
        self.sendUpdate('setNearbyAvatarChat', [msg])

    def __handleChatUpdateQT(self, qtList):
        self.sendUpdate('setNearbyAvatarQT', [qtList])

    def __handleChatUpdateQTQuest(self, qtList):
        self.sendUpdate('setNearbyAvatarQTQuest', [qtList])

    def makeTurnToHeadingTrack(self, heading):
        curHpr = self.getHpr()
        destHpr = self.getHpr()
        destHpr.setX(heading)
        if destHpr[0] - curHpr[0] > 180.0:
            destHpr.setX(destHpr[0] - 360)
        else:
            if destHpr[0] - curHpr[0] < -180.0:
                destHpr.setX(destHpr[0] + 360)
        turnSpeed = 180.0
        time = abs(destHpr[0] - curHpr[0]) / turnSpeed
        turnTracks = Parallel()
        if time > 0.2:
            turnTracks.append(Sequence(Func(self.loop, 'walk'), Wait(time), Func(self.loop, 'neutral')))
        turnTracks.append(LerpHprInterval(self, time, destHpr, name='lerp' + self.getName() + 'Hpr'))
        return turnTracks

    def setChat(self, category, msg, avId):
        if self.cr.doId2do.has_key(avId):
            avatar = self.cr.doId2do[avId]
            str = CCharChatter.getChatter(self.getName())[category][msg]
            if '%' in str:
                str = copy.deepcopy(str)
                avName = avatar.getName()
                str = string.replace(str, '%', avName)
            track = Sequence()
            if category != CCharChatter.GOODBYE:
                curHpr = self.getHpr()
                self.headsUp(avatar)
                destHpr = self.getHpr()
                self.setHpr(curHpr)
                track.append(self.makeTurnToHeadingTrack(destHpr[0]))
            if self.getName() == 'Donald':
                chatFlags = CFThought | CFTimeout
            else:
                chatFlags = CFSpeech | CFTimeout
            track.append(Func(self.setChatAbsolute, str, chatFlags))
            self.chatTrack.stop()
            self.chatTrack = track
            self.chatTrack.play()

    def setWalk(self, srcNode, destNode, timestamp):
        pass

    def walkSpeed(self):
        return 0.1

    def enableRaycast(self, enable=1):
        if not self.cTrav or not hasattr(self, 'cRayNode') or not self.cRayNode:
            self.notify.debug('raycast info not found for ' + self.getName())
            return None
        self.cTrav.removeCollider(self.cRayNode)
        if enable:
            if self.notify.getDebug():
                self.notify.debug('enabling raycast for ' + self.getName())
            self.cTrav.addCollider(self.cRayNode, self.lifter)
        else:
            if self.notify.getDebug():
                self.notify.debug('disabling raycast for ' + self.getName())
        return None
        return