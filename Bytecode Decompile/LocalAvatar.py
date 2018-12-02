from ShowBaseGlobal import *
from DirectGui import *
from PythonUtil import *
from IntervalGlobal import *
import Avatar, DistributedAvatar, Task, PositionExaminer, ToontownGlobals, ChatManager, math, string, whrandom, DirectNotifyGlobal, DistributedSmoothNode, DirectGuiGlobals, Toon, Localizer

class LocalAvatar(DistributedAvatar.DistributedAvatar, DistributedSmoothNode.DistributedSmoothNode):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalAvatar')
    wantMouse = base.config.GetBool('want-mouse', 0)
    sleepTimeout = base.config.GetInt('sleep-timeout', 120)
    __enableMarkerPlacement = base.config.GetBool('place-markers', 0)
    acceptingNewFriends = base.config.GetBool('accepting-new-friends', 1)

    def __init__(self, cr):
        try:
            self.LocalAvatar_initialized
        except:
            self.LocalAvatar_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
            self.initializeCollisions()
            self.initializeSmartCamera()
            self.animMultiplier = 1.0
            self.customMessages = []
            self.soundRun = base.loadSfx('phase_3.5/audio/sfx/AV_footstep_runloop.wav')
            self.soundWalk = base.loadSfx('phase_3.5/audio/sfx/AV_footstep_walkloop.wav')
            self.soundWhisper = base.loadSfx('phase_3.5/audio/sfx/GUI_whisper_3.mp3')
            self.positionExaminer = PositionExaminer.PositionExaminer()
            friendsGui = loader.loadModelOnce('phase_3.5/models/gui/friendslist_gui')
            friendsButtonNormal = friendsGui.find('**/FriendsBox_Closed')
            friendsButtonPressed = friendsGui.find('**/FriendsBox_Rollover')
            friendsButtonRollover = friendsGui.find('**/FriendsBox_Rollover')
            self.bFriendsList = DirectButton(image=(friendsButtonNormal, friendsButtonPressed, friendsButtonRollover), relief=None, pos=(1.192, 0, 0.875), scale=0.8, text=('', Localizer.FriendsListLabel, Localizer.FriendsListLabel), text_scale=0.09, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.18), text_font=ToontownGlobals.getInterfaceFont(), command=self.sendFriendsListEvent)
            self.bFriendsList.hide()
            self.friendsListButtonActive = 0
            self.friendsListButtonObscured = 0
            friendsGui.removeNode()
            self.chatMgr = ChatManager.ChatManager()
            self.commonChatFlags = 0
            self.garbleChat = 1
            self.isPageUp = 0
            self.isPageDown = 0
            self.sleepFlag = 0
            self.movingFlag = 0
            self.lastNeedH = None
            self.accept('friendOnline', self.__friendOnline)
            self.accept('friendOffline', self.__friendOffline)
            self.accept('clickedWhisper', self.__clickedWhisper)
            self.sleepCallback = None
            self.accept('wakeup', self.wakeUp)

        return None
        return

    def sendFriendsListEvent(self):
        messenger.send('wakeup')
        messenger.send('openFriendsList')

    def delete(self):
        try:
            self.LocalAvatar_deleted
        except:
            self.LocalAvatar_deleted = 1
            self.deleteCollisions()
            self.positionExaminer.delete()
            del self.positionExaminer
            self.bFriendsList.destroy()
            del self.bFriendsList
            self.chatMgr.delete()
            del self.chatMgr
            del self.soundRun
            del self.soundWalk
            del self.soundWhisper
            self.ignoreAll()
            DistributedAvatar.DistributedAvatar.delete(self)

        return

    def initializeCollisions(self):
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, 1.5)
        self.cSphereNode = CollisionNode('cSphereNode')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereBitMask = ToontownGlobals.WallBitmask
        self.cSphereNode.setFromCollideMask(self.cSphereBitMask)
        self.cSphereNode.setIntoCollideMask(BitMask32.allOff())
        base.mouse2cam.node().setVelocityNode(self.cSphereNode)
        self.cRay = CollisionRay(0.0, 0.0, 4.0, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode('cRayNode')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.pusher = CollisionHandlerPusher()
        self.pusher.setInPattern('enter%in')
        self.pusher.setOutPattern('exit%in')
        self.lifter = CollisionHandlerFloor()
        self.lifter.setInPattern('on-floor')
        self.lifter.setOutPattern('off-floor')
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        self.lifter.setMaxVelocity(16.0)
        self.cTrav = CollisionTraverser()
        base.cTrav = self.cTrav
        self.collisionsOn()
        self.pusher.addColliderDrive(self.cSphereNode, base.drive.node())
        self.lifter.addColliderDrive(self.cRayNode, base.drive.node())
        self.ccTrav = CollisionTraverser()
        self.ccLine = CollisionSegment(0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        self.ccLineNode = CollisionNode('ccLineNode')
        self.ccLineNode.addSolid(self.ccLine)
        self.ccLineNodePath = self.attachNewNode(self.ccLineNode)
        self.ccLineNodePath.hide()
        self.ccLineBitMask = ToontownGlobals.CameraBitmask
        self.ccLineNode.setFromCollideMask(self.ccLineBitMask)
        self.ccLineNode.setIntoCollideMask(BitMask32.allOff())
        self.camCollisionQueue = CollisionHandlerQueue()
        self.ccTrav.addCollider(self.ccLineNode, self.camCollisionQueue)
        self.camFloorRayNode = self.attachNewNode('camFloorRayNode')
        self.ccRay = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRayNode = CollisionNode('ccRayNode')
        self.ccRayNode.addSolid(self.ccRay)
        self.ccRayNodePath = self.camFloorRayNode.attachNewNode(self.ccRayNode)
        self.ccRayNodePath.hide()
        self.ccRayBitMask = ToontownGlobals.FloorBitmask
        self.ccRayNode.setFromCollideMask(self.ccRayBitMask)
        self.ccRayNode.setIntoCollideMask(BitMask32.allOff())
        self.ccTravFloor = CollisionTraverser()
        self.camFloorCollisionQueue = CollisionHandlerQueue()
        self.ccTravFloor.addCollider(self.ccRayNode, self.camFloorCollisionQueue)
        nearPlaneDist = base.camLens.getNear()
        hFov = base.camLens.getHfov()
        vFov = base.camLens.getVfov()
        hOff = nearPlaneDist * math.tan(deg2Rad(hFov / 2))
        vOff = nearPlaneDist * math.tan(deg2Rad(vFov / 2))
        camPnts = [
         Point3(hOff, nearPlaneDist, vOff), Point3(-hOff, nearPlaneDist, vOff), Point3(hOff, nearPlaneDist, -vOff), Point3(-hOff, nearPlaneDist, -vOff), Point3(0.0, 0.0, 0.0)]
        avgPnt = Point3(0.0, 0.0, 0.0)
        for camPnt in camPnts:
            avgPnt = avgPnt + camPnt

        avgPnt = avgPnt / len(camPnts)
        sphereRadius = 0.0
        for camPnt in camPnts:
            dist = Vec3(camPnt - avgPnt).length()
            if dist > sphereRadius:
                sphereRadius = dist

        sphereRadius *= 1.15
        self.ccSphere = CollisionSphere(avgPnt[0], avgPnt[1], avgPnt[2], sphereRadius)
        self.ccSphereNode = CollisionNode('ccSphereNode')
        self.ccSphereNode.addSolid(self.ccSphere)
        self.ccSphereNodePath = base.camera.attachNewNode(self.ccSphereNode)
        self.ccSphereNodePath.hide()
        self.ccSphereBitMask = ToontownGlobals.CameraBitmask
        self.ccSphereNode.setFromCollideMask(self.ccSphereBitMask)
        self.ccSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.camPusher = CollisionHandlerPusher()
        self.camPusher.addColliderNode(self.ccSphereNode, base.camera.node())
        self.ccPusherTrav = CollisionTraverser()
        self.ccSphere2 = self.ccSphere
        self.ccSphereNode2 = CollisionNode('ccSphereNode2')
        self.ccSphereNode2.addSolid(self.ccSphere2)
        self.ccSphereNodePath2 = base.camera.attachNewNode(self.ccSphereNode2)
        self.ccSphereNodePath2.hide()
        self.ccSphereBitMask2 = ToontownGlobals.CameraBitmask
        self.ccSphereNode2.setFromCollideMask(self.ccSphereBitMask2)
        self.ccSphereNode2.setIntoCollideMask(BitMask32(0))
        self.camPusher2 = CollisionHandlerPusher()
        self.ccPusherTrav.addCollider(self.ccSphereNode2, self.camPusher2)
        self.camPusher2.addColliderNode(self.ccSphereNode2, base.camera.node())
        return None
        return

    def deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        del self.cRay
        del self.cRayNode
        self.cRayNodePath.removeNode()
        del self.cRayNodePath
        del self.pusher
        self.ignore('entero157')
        del self.lifter
        del self.cTrav
        del self.ccTrav
        del self.ccLine
        del self.ccLineNode
        self.ccLineNodePath.removeNode()
        del self.ccLineNodePath
        del self.camCollisionQueue
        del self.ccRay
        del self.ccRayNode
        self.ccRayNodePath.removeNode()
        del self.ccRayNodePath
        del self.ccTravFloor
        del self.camFloorCollisionQueue
        del self.ccSphere
        del self.ccSphereNode
        self.ccSphereNodePath.removeNode()
        del self.ccSphereNodePath
        del self.camPusher
        del self.ccPusherTrav
        del self.ccSphere2
        del self.ccSphereNode2
        self.ccSphereNodePath2.removeNode()
        del self.ccSphereNodePath2
        del self.camPusher2

    def collisionsOff(self):
        self.cTrav.removeCollider(self.cSphereNode)
        self.cTrav.removeCollider(self.cRayNode)
        self.oneTimeCollide()
        return None
        return

    def collisionsOn(self):
        self.cTrav.addCollider(self.cSphereNode, self.pusher)
        self.cTrav.addCollider(self.cRayNode, self.lifter)
        return None
        return

    def oneTimeCollide(self):
        driveNode = base.drive.node()
        driveNode.setPos(self.getPos())
        tempCTrav = CollisionTraverser()
        tempCTrav.addCollider(self.cSphereNode, self.pusher)
        tempCTrav.addCollider(self.cRayNode, self.lifter)
        tempCTrav.traverse(render)
        self.setPos(driveNode.getPos())

    def attachCamera(self):
        pos = self.getPos()
        hpr = self.getHpr()
        base.enableMouse()
        camera.reparentTo(self)
        base.setMouseOnNode(self.node())
        if self.wantMouse:
            base.mouseInterfaceNode.setIgnoreMouse(0)
        else:
            base.mouseInterfaceNode.setIgnoreMouse(1)
        base.mouseInterfaceNode.setPos(pos)
        base.mouseInterfaceNode.setHpr(hpr)
        self.setWalkSpeedNormal()

    def setWalkSpeedNormal(self):
        base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSpeed)
        base.mouseInterfaceNode.setReverseSpeed(ToontownGlobals.ToonReverseSpeed)
        base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed)
        return

    def setWalkSpeedSlow(self):
        base.mouseInterfaceNode.setForwardSpeed(ToontownGlobals.ToonForwardSlowSpeed)
        base.mouseInterfaceNode.setReverseSpeed(ToontownGlobals.ToonReverseSlowSpeed)
        base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSlowSpeed)
        return

    def setWalkSpeed(self, fwd, rev, rotate):
        base.mouseInterfaceNode.setForwardSpeed(fwd)
        base.mouseInterfaceNode.setReverseSpeed(rev)
        base.mouseInterfaceNode.setRotateSpeed(rotate)
        return

    def detachCamera(self):
        base.disableMouse()

    def addTabHook(self):
        self.accept('tab', self.nextCameraPos, [1])
        self.accept('shift-tab', self.nextCameraPos, [0])
        self.accept('page_up', self.pageUp)
        self.accept('page_down', self.pageDown)
        self.accept('arrow_up', self.clearPageUpDown)
        self.accept('arrow_up-up', self.clearPageUpDown)
        self.accept('arrow_down', self.clearPageUpDown)
        self.accept('arrow_down-up', self.clearPageUpDown)

    def removeTabHook(self):
        self.ignore('tab')
        self.ignore('shift-tab')
        self.ignore('page_up')
        self.ignore('page_down')
        self.ignore('arrow_up')
        self.ignore('arrow_up-up')
        self.ignore('arrow_down')
        self.ignore('arrow_down-up')
        self.clearPageUpDown()

    def pageUp(self):
        if not self.isPageUp:
            self.isPageDown = 0
            self.isPageUp = 1
            self.lerpCameraFov(70, 0.6)
            self.setCameraPositionByIndex(self.cameraIndex)

    def pageDown(self):
        if not self.isPageDown:
            self.isPageUp = 0
            self.isPageDown = 1
            self.lerpCameraFov(70, 0.6)
            self.setCameraPositionByIndex(self.cameraIndex)

    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraFov(ToontownGlobals.DefaultCameraFov, 0.6)
            self.isPageDown = 0
            self.isPageUp = 0
            self.setCameraPositionByIndex(self.cameraIndex)

    def nextCameraPos(self, forward):
        self.__cameraHasBeenMoved = 1
        if forward:
            self.cameraIndex += 1
            if self.cameraIndex > len(self.cameraPositions) - 1:
                self.cameraIndex = 0
        else:
            self.cameraIndex -= 1
            if self.cameraIndex < 0:
                self.cameraIndex = len(self.cameraPositions) - 1
        self.setCameraPositionByIndex(self.cameraIndex)

    def initCameraPositions(self):
        camHeight = self.getClampedAvatarHeight()
        heightScaleFactor = camHeight * 0.3333333333
        defLookAt = Point3(0.0, 1.5, camHeight)
        qtXoffset = 3.0
        qtPosition = (
         Point3(qtXoffset - 1, -10.0, camHeight + 5.0), Point3(qtXoffset, 2.0, camHeight))
        self.cameraPositions = [
         (
          Point3(0.0, -9.0 * heightScaleFactor, camHeight), defLookAt, Point3(0.0, camHeight, camHeight * 4.0), Point3(0.0, camHeight, camHeight * -1.0), 0), (Point3(0.0, 0.5, camHeight), defLookAt, Point3(0.0, camHeight, camHeight * 1.33), Point3(0.0, camHeight, camHeight * 0.66), 1),
         (
          Point3(5.7 * heightScaleFactor, 7.65 * heightScaleFactor, camHeight + 2.0), Point3(0.0, 1.0, camHeight), Point3(0.0, 1.0, camHeight * 4.0), Point3(0.0, 1.0, camHeight * -1.0), 0), (Point3(0.0, -24.0 * heightScaleFactor, camHeight + 4.0), defLookAt, Point3(0.0, 1.5, camHeight * 4.0), Point3(0.0, 1.5, camHeight * -1.0), 0), (Point3(0.0, -12.0 * heightScaleFactor, camHeight + 4.0), defLookAt, Point3(0.0, 1.5, camHeight * 4.0), Point3(0.0, 1.5, camHeight * -1.0), 0)] + self.auxCameraPositions
        return None
        return

    def addCameraPosition(self, camPos=None):
        if camPos == None:
            lookAtNP = self.attachNewNode('lookAt')
            lookAtNP.setPos(base.cam, 0, 1, 0)
            lookAtPos = lookAtNP.getPos()
            camHeight = self.getClampedAvatarHeight()
            camPos = (base.cam.getPos(self), lookAtPos, Point3(0.0, 1.5, camHeight * 4.0), Point3(0.0, 1.5, camHeight * -1.0), 1)
            lookAtNP.removeNode()
        self.auxCameraPositions.append(camPos)
        self.cameraPositions.append(camPos)
        return

    def removeCameraPosition(self):
        if len(self.cameraPositions) > 1:
            camPos = self.cameraPositions[self.cameraIndex]
            if camPos in self.auxCameraPositions:
                self.auxCameraPositions.remove(camPos)
            if camPos in self.cameraPositions:
                self.cameraPositions.remove(camPos)
            self.nextCameraPos(1)

    def printCameraPositions(self):
        print '['
        for i in range(len(self.cameraPositions)):
            self.printCameraPosition(i)
            print ','

        print ']'

    def printCameraPosition(self, index):
        cp = self.cameraPositions[index]
        print '(Point3(%0.2f, %0.2f, %0.2f),' % (cp[0][0], cp[0][1], cp[0][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[1][0], cp[1][1], cp[1][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[2][0], cp[2][1], cp[2][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[3][0], cp[3][1], cp[3][2])
        print '%d,' % cp[4]
        print ')',

    def posCamera(self, lerp, time):
        if not lerp:
            self.positionCameraWithPusher(self.getCompromiseCameraPos(), self.getLookAtPoint())
        else:
            camPos = self.getCompromiseCameraPos()
            savePos = camera.getPos()
            saveHpr = camera.getHpr()
            self.positionCameraWithPusher(camPos, self.getLookAtPoint())
            x = camPos[0]
            y = camPos[1]
            z = camPos[2]
            destHpr = camera.getHpr()
            h = destHpr[0]
            p = destHpr[1]
            r = destHpr[2]
            camera.setPos(savePos)
            camera.setHpr(saveHpr)
            taskMgr.remove('posCamera')
            camera.lerpPosHpr(x, y, z, h, p, r, time, task='posCamera')

    def getClampedAvatarHeight(self):
        return max(self.getHeight(), 3.0)

    def getVisibilityPoint(self):
        return Point3(0.0, 0.0, self.getHeight())

    def setLookAtPoint(self, la):
        self.__curLookAt = Point3(la)

    def getLookAtPoint(self):
        return Point3(self.__curLookAt)

    def setIdealCameraPos(self, pos):
        self.__idealCameraPos = Point3(pos)
        self.updateSmartCameraCollisionLineSegment()

    def getIdealCameraPos(self):
        return Point3(self.__idealCameraPos)

    def setCameraPositionByIndex(self, index):
        camSettings = self.cameraPositions[index]
        self.setIdealCameraPos(camSettings[0])
        if self.isPageUp and self.isPageDown or not self.isPageUp and not self.isPageDown:
            self.__cameraHasBeenMoved = 1
            self.setLookAtPoint(camSettings[1])
        else:
            if self.isPageUp:
                self.__cameraHasBeenMoved = 1
                self.setLookAtPoint(camSettings[2])
            else:
                if self.isPageDown:
                    self.__cameraHasBeenMoved = 1
                    self.setLookAtPoint(camSettings[3])
                else:
                    self.notify.error('This case should be impossible.')
        self.__disableSmartCam = camSettings[4]
        if self.__disableSmartCam:
            self.cameraZOffset = 0.0

    def getCompromiseCameraPos(self):
        if self.__idealCameraObstructed == 0:
            compromisePos = self.getIdealCameraPos()
        else:
            visPnt = self.getVisibilityPoint()
            idealPos = self.getIdealCameraPos()
            distance = Vec3(idealPos - visPnt).length()
            ratio = self.closestObstructionDistance / distance
            compromisePos = idealPos * ratio + visPnt * (1 - ratio)
            liftMult = 1.0 - ratio * ratio
            compromisePos = Point3(compromisePos[0], compromisePos[1], compromisePos[2] + self.getHeight() * 0.4 * liftMult)
        compromisePos.setZ(compromisePos[2] + self.cameraZOffset)
        return compromisePos

    def updateSmartCameraCollisionLineSegment(self):
        pointB = self.getIdealCameraPos()
        pointA = self.getVisibilityPoint()
        pullbackDist = 1.5
        vectorAB = Vec3(pointB - pointA)
        lengthAB = vectorAB.length()
        if lengthAB > pullbackDist:
            pullbackVector = vectorAB * (pullbackDist / lengthAB)
            pointA = Point3(pointA + Point3(pullbackVector))
            lengthAB -= pullbackDist
        if lengthAB > 0.001:
            self.ccLine.setPointA(pointA)
            self.ccLine.setPointB(pointB)

    def initializeSmartCamera(self):
        self.__idealCameraObstructed = 0
        self.closestObstructionDistance = 0.0
        self.cameraIndex = 0
        self.auxCameraPositions = []
        self.cameraZOffset = 0.0
        self.__onLevelGround = 0
        self.__geom = render
        self.__disableSmartCam = 0

    def setOnLevelGround(self, flag):
        self.__onLevelGround = flag

    def setGeom(self, geom):
        self.__geom = geom

    def startUpdateSmartCamera(self):
        self.__floorDetected = 0
        self.__cameraHasBeenMoved = 0
        self.initCameraPositions()
        self.setCameraPositionByIndex(self.cameraIndex)
        self.posCamera(0, 0.0)
        self.__instantaneousCamPos = camera.getPos()
        self.cTrav.addCollider(self.ccSphereNode, self.camPusher)
        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)
        taskName = self.taskName('updateSmartCamera')
        taskMgr.remove(taskName)
        taskMgr.add(self.updateSmartCamera, taskName)

    def stopUpdateSmartCamera(self):
        self.cTrav.removeCollider(self.ccSphereNode)
        taskName = self.taskName('updateSmartCamera')
        taskMgr.remove(taskName)

    def updateSmartCamera(self, task):
        if not self.__cameraHasBeenMoved:
            if self.__lastPosWrtRender == camera.getPos(render):
                if self.__lastHprWrtRender == camera.getHpr(render):
                    return Task.cont
        self.__cameraHasBeenMoved = 0
        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)
        camWasObstructed = self.__idealCameraObstructed
        self.__idealCameraObstructed = 0
        if not self.__disableSmartCam:
            self.ccTrav.traverse(self.__geom)
            if self.camCollisionQueue.getNumEntries() > 0:
                self.camCollisionQueue.sortEntries()
                self.handleCameraObstruction(self.camCollisionQueue.getEntry(0), camWasObstructed)
            if not self.__onLevelGround:
                self.handleCameraFloorInteraction()
        self.nudgeCamera()
        return Task.cont

    def positionCameraWithPusher(self, pos, lookAt):
        camera.setPos(pos)
        self.ccPusherTrav.traverse(self.__geom)
        camera.lookAt(lookAt)

    def nudgeCamera(self):
        CLOSE_ENOUGH = 0.1
        curCamPos = self.__instantaneousCamPos
        curCamHpr = camera.getHpr()
        targetCamPos = self.getCompromiseCameraPos()
        targetCamLookAt = self.getLookAtPoint()
        posDone = 0
        if Vec3(curCamPos - targetCamPos).length() <= CLOSE_ENOUGH:
            camera.setPos(targetCamPos)
            posDone = 1
        camera.setPos(targetCamPos)
        camera.lookAt(targetCamLookAt)
        targetCamHpr = camera.getHpr()
        hprDone = 0
        if Vec3(curCamHpr - targetCamHpr).length() <= CLOSE_ENOUGH:
            hprDone = 1
        if posDone and hprDone:
            return
        lerpRatio = 0.15
        lerpRatio = 1 - pow(1 - lerpRatio, globalClock.getDt() * 30.0)
        self.__instantaneousCamPos = targetCamPos * lerpRatio + curCamPos * (1 - lerpRatio)
        newHpr = targetCamHpr * lerpRatio + curCamHpr * (1 - lerpRatio)
        camera.setPos(self.__instantaneousCamPos)
        camera.setHpr(newHpr)

    def popCameraToDest(self):
        newCamPos = self.getCompromiseCameraPos()
        newCamLookAt = self.getLookAtPoint()
        self.positionCameraWithPusher(newCamPos, newCamLookAt)
        self.__instantaneousCamPos = camera.getPos()

    def handleCameraObstruction(self, camObstrCollisionEntry, camWasObstructed):
        collisionPoint = camObstrCollisionEntry.getFromIntersectionPoint()
        collisionVec = Vec3(collisionPoint - self.ccLine.getPointA())
        distance = collisionVec.length()
        if not camWasObstructed or camWasObstructed and self.closestObstructionDistance > distance:
            popCameraUp = 1
        else:
            popCameraUp = 0
        self.__idealCameraObstructed = 1
        self.closestObstructionDistance = distance
        if popCameraUp:
            self.popCameraToDest()

    def handleCameraFloorInteraction(self):
        self.camFloorRayNode.setPos(camera.getPos())
        self.ccTravFloor.traverse(self.__geom)
        if self.camFloorCollisionQueue.getNumEntries() == 0:
            return
        self.camFloorCollisionQueue.sortEntries()
        camObstrCollisionEntry = self.camFloorCollisionQueue.getEntry(0)
        camHeightFromFloor = camObstrCollisionEntry.getFromIntersectionPoint()[2]
        heightOfFloorUnderCamera = camera.getPos()[2] - ToontownGlobals.FloorOffset + camHeightFromFloor
        camIdealHeightFromFloor = self.getIdealCameraPos()[2]
        camTargetHeight = heightOfFloorUnderCamera + camIdealHeightFromFloor
        self.cameraZOffset = camTargetHeight - camIdealHeightFromFloor
        if self.cameraZOffset < 0.0:
            self.cameraZOffset = self.cameraZOffset * 0.3333333333
            if self.cameraZOffset < -(self.getClampedAvatarHeight() * 0.5):
                if self.cameraZOffset < -self.getClampedAvatarHeight():
                    self.cameraZOffset = 0.0
                else:
                    self.cameraZOffset = -(self.getClampedAvatarHeight() * 0.5)
        if self.__floorDetected == 0:
            self.__floorDetected = 1
            self.popCameraToDest()

    def lerpCameraFov(self, fov, time):
        taskMgr.remove('cam-fov-lerp-play')
        oldFov = base.camLens.getHfov()
        if abs(fov - oldFov) > 0.1:

            def setCamFov(fov):
                base.camLens.setFov(fov)

            self.camLerpInterval = LerpFunctionInterval(setCamFov, fromData=oldFov, toData=fov, duration=time, name='cam-fov-lerp')
            self.camLerpInterval.play()

    def gotoNode(self, node):
        possiblePoints = (
         Point3(3, 6, 0), Point3(-3, 6, 0), Point3(6, 6, 0), Point3(-6, 6, 0), Point3(3, 9, 0), Point3(-3, 9, 0), Point3(6, 9, 0), Point3(-6, 9, 0), Point3(9, 9, 0), Point3(-9, 9, 0), Point3(6, 0, 0), Point3(-6, 0, 0), Point3(6, 3, 0), Point3(-6, 3, 0), Point3(9, 9, 0), Point3(-9, 9, 0), Point3(0, 12, 0), Point3(3, 12, 0), Point3(-3, 12, 0), Point3(6, 12, 0), Point3(-6, 12, 0), Point3(9, 12, 0), Point3(-9, 12, 0), Point3(0, -6, 0), Point3(-3, -6, 0), Point3(0, -9, 0), Point3(-6, -9, 0))
        for point in possiblePoints:
            pos = self.positionExaminer.consider(node, point)
            if pos:
                self.setPos(node, pos)
                self.lookAt(node)
                self.setHpr(self.getH() + whrandom.choice((-10, 10)), 0, 0)
                base.drive.node().setPos(self.getPos())
                base.drive.node().setHpr(self.getHpr())
                return

        self.setPos(node, 0, 0, 0)
        base.drive.node().setPos(self.getPos())
        base.drive.node().setHpr(self.getHpr())

    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages
        messenger.send('customMessagesChanged')

    def displayWhisper(self, fromId, chatString, whisperType):
        sender = None
        if fromId != 0:
            sender = toonbase.tcr.identifyAvatar(fromId)
        if whisperType == WhisperPopup.WTNormal or whisperType == WhisperPopup.WTQuickTalker:
            if sender == None:
                return
            chatString = sender.getName() + ': ' + chatString
        whisper = WhisperPopup(chatString, ToontownGlobals.getInterfaceFont(), whisperType)
        if sender != None:
            whisper.setClickable(sender.getName(), fromId)
        whisper.manage(toonbase.marginManager)
        base.playSfx(self.soundWhisper)
        return

    def setAnimMultiplier(self, value):
        self.animMultiplier = value

    def getAnimMultiplier(self):
        return self.animMultiplier

    def runSound(self):
        self.soundWalk.stop()
        base.playSfx(self.soundRun, looping=1)

    def walkSound(self):
        self.soundRun.stop()
        base.playSfx(self.soundWalk, looping=1)

    def stopSound(self):
        self.soundRun.stop()
        self.soundWalk.stop()

    def wakeUp(self):
        if self.sleepCallback != None:
            taskMgr.remove(self.uniqueName('sleepwatch'))
            self.startSleepWatch(self.sleepCallback)
        self.lastMoved = globalClock.getFrameTime()
        if self.sleepFlag:
            self.sleepFlag = 0
        return

    def gotoSleep(self):
        if not self.sleepFlag:
            self.b_setAnimState('Sleep', self.animMultiplier)
            self.sleepFlag = 1

    def forceGotoSleep(self):
        self.sleepFlag = 0
        self.gotoSleep()

    def startSleepWatch(self, callback):
        self.sleepCallback = callback
        taskMgr.doMethodLater(self.sleepTimeout, callback, self.uniqueName('sleepwatch'))

    def stopSleepWatch(self):
        taskMgr.remove(self.uniqueName('sleepwatch'))
        self.sleepCallback = None
        return

    def trackAnimToSpeed(self, task):
        speed = base.mouseInterfaceNode.getSpeed()
        rotSpeed = base.mouseInterfaceNode.getRotSpeed()
        if speed != 0.0 or rotSpeed != 0.0:
            if not self.movingFlag:
                self.movingFlag = 1
                self.stopLookAround()
        else:
            if self.movingFlag:
                self.movingFlag = 0
                self.startLookAround()
        if self.movingFlag or self.hp <= 0:
            self.wakeUp()
        else:
            if not self.sleepFlag:
                now = globalClock.getFrameTime()
                if now - self.lastMoved > self.sleepTimeout:
                    self.gotoSleep()
        state = None
        if self.sleepFlag:
            state = 'Sleep'
        else:
            if self.hp > 0:
                state = 'Happy'
            else:
                state = 'Sad'
        if state != self.lastState:
            self.lastState = state
            self.b_setAnimState(state, self.animMultiplier)
            if state == 'Sad':
                self.setWalkSpeedSlow()
            else:
                self.setWalkSpeedNormal()
        if self.cheesyEffect == ToontownGlobals.CEFlatProfile or self.cheesyEffect == ToontownGlobals.CEFlatPortrait:
            needH = None
            if rotSpeed > 0.0:
                needH = -10
            else:
                if rotSpeed < 0.0:
                    needH = 10
                else:
                    if speed != 0.0:
                        needH = 0
            if needH != None and self.lastNeedH != needH:
                node = self.getGeomNode().getChild(0)
                lerp = Sequence(LerpHprInterval(node, 0.5, Vec3(needH, 0, 0), blendType='easeInOut'), name='cheesy-lerp-hpr', autoPause=1)
                lerp.start()
                self.lastNeedH = needH
        else:
            self.lastNeedH = None
        action = self.setSpeed(speed, rotSpeed)
        if action != self.lastAction:
            self.lastAction = action
            if action == Toon.WALK_INDEX or action == Toon.REVERSE_INDEX:
                self.walkSound()
            else:
                if action == Toon.RUN_INDEX:
                    self.runSound()
                else:
                    self.stopSound()
        return Task.cont
        return

    def startTrackAnimToSpeed(self):
        taskName = self.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        task = Task.Task(self.trackAnimToSpeed)
        self.lastMoved = globalClock.getFrameTime()
        self.lastState = None
        self.lastAction = None
        self.trackAnimToSpeed(task)
        taskMgr.add(self.trackAnimToSpeed, taskName)
        return

    def stopTrackAnimToSpeed(self):
        taskName = self.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        self.stopSound()

    def startChat(self):
        self.chatMgr.start()
        self.accept('chatUpdate', self.b_setChat)
        self.accept('chatUpdateQT', self.b_setQT)
        self.accept('chatUpdateQTQuest', self.b_setQTQuest)
        self.accept('chatUpdateQTCustom', self.b_setQTCustom)
        self.accept('whisperUpdate', self.whisperTo)
        self.accept('whisperUpdateQT', self.whisperQTTo)
        self.accept('whisperUpdateQTQuest', self.whisperQTQuestTo)
        self.accept('whisperUpdateQTCustom', self.whisperQTCustomTo)
        self.accept(ToontownGlobals.ThinkPosHotkey, self.thinkPos)
        self.accept(ToontownGlobals.PrintCamPosHotkey, self.printCamPos)
        if self.__enableMarkerPlacement:
            self.accept(ToontownGlobals.PlaceMarkerHotkey, self.__placeMarker)
        return None
        return

    def stopChat(self):
        self.chatMgr.stop()
        self.ignore('chatUpdate')
        self.ignore('chatUpdateQT')
        self.ignore('chatUpdateQTQuest')
        self.ignore('chatUpdateQTCustom')
        self.ignore('whisperUpdate')
        self.ignore('whisperUpdateQT')
        self.ignore('whisperUpdateQTQuest')
        self.ignore('whisperUpdateQTCustom')
        self.ignore(ToontownGlobals.ThinkPosHotkey)
        if self.__enableMarkerPlacement:
            self.ignore(ToontownGlobals.PlaceMarkerHotkey)
        return None
        return

    def printCamPos(self):
        node = base.camera.getParent()
        pos = base.cam.getPos(node)
        hpr = base.cam.getHpr(node)
        print 'cam pos = ', `pos`, ', cam hpr = ', `hpr`

    def getAvPosStr(self):
        pos = self.getPos()
        hpr = self.getHpr()
        serverVersion = toonbase.tcr.getServerVersion()
        districtName = toonbase.tcr.getShardName(toonbase.localToon.defaultShard)
        if hasattr(toonbase.tcr.playGame.hood, 'loader') and hasattr(toonbase.tcr.playGame.hood.loader, 'place') and toonbase.tcr.playGame.getPlace() != None:
            zoneId = toonbase.tcr.playGame.getPlace().getZoneId()
        else:
            zoneId = '?'
        strPosCoordText = 'X: %.3f' % pos[0] + ', Y: %.3f' % pos[1] + '\nZ: %.3f' % pos[2] + ', H: %.3f' % hpr[0] + '\nZone: %s' % str(zoneId) + ', Ver: %s, ' % serverVersion + 'District: %s' % districtName
        return strPosCoordText
        return

    def thinkPos(self):
        pos = self.getPos()
        hpr = self.getHpr()
        serverVersion = toonbase.tcr.getServerVersion()
        districtName = toonbase.tcr.getShardName(toonbase.localToon.defaultShard)
        if hasattr(toonbase.tcr.playGame.hood, 'loader') and hasattr(toonbase.tcr.playGame.hood.loader, 'place') and toonbase.tcr.playGame.getPlace() != None:
            zoneId = toonbase.tcr.playGame.getPlace().getZoneId()
        else:
            zoneId = '?'
        strPos = 'X: %.3f' % pos[0] + '\nY: %.3f' % pos[1] + '\nZ: %.3f' % pos[2] + '\nH: %.3f' % hpr[0] + '\nZone: %s' % str(zoneId) + ',\nVer: %s, ' % serverVersion + '\nDistrict: %s' % districtName
        print 'Current position=', strPos.replace('\n', ', ')
        self.setChat(strPos, CFThought)
        return

    def __placeMarker(self):
        pos = self.getPos()
        hpr = self.getHpr()
        chest = loader.loadModelOnce('phase_4/models/props/coffin')
        chest.reparentTo(render)
        chest.setColor(1, 0, 0, 1)
        chest.setPosHpr(pos, hpr)
        chest.setScale(0.5)

    def stopPosHprBroadcast(self):
        taskName = self.taskName('sendPosHpr')
        taskMgr.remove(taskName)

    def startPosHprBroadcast(self):
        taskName = self.taskName('sendPosHpr')
        xyz = self.getPos()
        hpr = self.getHpr(0)
        self.__storeX = xyz[0]
        self.__storeY = xyz[1]
        self.__storeZ = xyz[2]
        self.__storeH = hpr[0]
        self.__storeP = hpr[1]
        self.__storeR = hpr[2]
        self.__storeStop = 0
        self.__epsilon = 0.01
        self.__broadcastFrequency = 0.2
        self.b_clearSmoothing()
        self.d_setSmPosHpr(self.__storeX, self.__storeY, self.__storeZ, self.__storeH, self.__storeP, self.__storeR)
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.__broadcastFrequency, self.posHprBroadcast, taskName)

    def posHprBroadcast(self, task):
        self.d_broadcastPosHpr()
        taskName = self.taskName('sendPosHpr')
        taskMgr.doMethodLater(self.__broadcastFrequency, self.posHprBroadcast, taskName)
        return Task.done

    def d_broadcastPosHpr(self):
        xyz = self.getPos()
        hpr = self.getHpr(0)
        if abs(self.__storeX - xyz[0]) > self.__epsilon:
            newX = xyz[0]
        else:
            newX = None
        if abs(self.__storeY - xyz[1]) > self.__epsilon:
            newY = xyz[1]
        else:
            newY = None
        if abs(self.__storeZ - xyz[2]) > self.__epsilon:
            newZ = xyz[2]
        else:
            newZ = None
        if abs(self.__storeH - hpr[0]) > self.__epsilon:
            newH = hpr[0]
        else:
            newH = None
        if abs(self.__storeP - hpr[1]) > self.__epsilon:
            newP = hpr[1]
        else:
            newP = None
        if abs(self.__storeR - hpr[2]) > self.__epsilon:
            newR = hpr[2]
        else:
            newR = None
        if not (newX or newY or newZ or newH or newP or newR):
            if not self.__storeStop:
                self.__storeStop = 1
                self.d_setSmStop()
        else:
            if newH and not (newX or newY or newZ or newP or newR):
                self.__storeStop = 0
                if newH:
                    self.__storeH = newH
                self.d_setSmH(self.__storeH)
            else:
                if (newX or newY) and not (newZ or newH or newP or newR):
                    self.__storeStop = 0
                    if newX:
                        self.__storeX = newX
                    if newY:
                        self.__storeY = newY
                    self.d_setSmXY(self.__storeX, self.__storeY)
                else:
                    if (newX or newY or newZ) and not (newH or newP or newR):
                        self.__storeStop = 0
                        if newX:
                            self.__storeX = newX
                        if newY:
                            self.__storeY = newY
                        if newZ:
                            self.__storeZ = newZ
                        self.d_setSmPos(self.__storeX, self.__storeY, self.__storeZ)
                    else:
                        if (newX or newY or newH) and not (newZ or newP or newR):
                            self.__storeStop = 0
                            if newX:
                                self.__storeX = newX
                            if newY:
                                self.__storeY = newY
                            if newH:
                                self.__storeH = newH
                            self.d_setSmXYH(self.__storeX, self.__storeY, self.__storeH)
                        else:
                            if (newX or newY or newZ or newH) and not (newP or newR):
                                self.__storeStop = 0
                                if newX:
                                    self.__storeX = newX
                                if newY:
                                    self.__storeY = newY
                                if newZ:
                                    self.__storeZ = newZ
                                if newH:
                                    self.__storeH = newH
                                self.d_setSmXYZH(self.__storeX, self.__storeY, self.__storeZ, self.__storeH)
                            else:
                                self.__storeStop = 0
                                if newX:
                                    self.__storeX = newX
                                if newY:
                                    self.__storeY = newY
                                if newZ:
                                    self.__storeZ = newZ
                                if newH:
                                    self.__storeH = newH
                                if newP:
                                    self.__storeP = newP
                                if newR:
                                    self.__storeR = newR
                                self.d_setSmPosHpr(self.__storeX, self.__storeY, self.__storeZ, self.__storeH, self.__storeP, self.__storeR)
        return

    def d_broadcastPositionNow(self):
        self.d_clearSmoothing()
        self.d_broadcastPosHpr()

    def setFriendsListButtonActive(self, active):
        self.friendsListButtonActive = active
        if active:
            self.accept(ToontownGlobals.FriendsListHotkey, self.sendFriendsListEvent)
        else:
            self.ignore(ToontownGlobals.FriendsListHotkey)
        self.__doFriendsListButton()

    def obscureFriendsListButton(self, increment):
        self.friendsListButtonObscured += increment
        self.__doFriendsListButton()

    def __doFriendsListButton(self):
        if self.friendsListButtonActive and self.friendsListButtonObscured <= 0:
            self.bFriendsList.show()
        else:
            self.bFriendsList.hide()

    def travCollisionsLOS(self, n=None):
        if n == None:
            n = self.__geom
        self.ccTrav.traverse(n)
        return

    def travCollisionsFloor(self, n=None):
        if n == None:
            n = self.__geom
        self.ccTravFloor.traverse(n)
        return

    def travCollisionsPusher(self, n=None):
        if n == None:
            n = self.__geom
        self.ccPusherTrav.traverse(n)
        return

    def __friendOnline(self, doId):
        if self.oldFriendsList != None:
            now = globalClock.getFrameTime()
            elapsed = now - self.timeFriendsListChanged
            if elapsed < 10.0 and self.oldFriendsList.count(doId) == 0:
                self.oldFriendsList.append(doId)
                return
        friend = toonbase.tcr.identifyFriend(doId)
        if friend != None:
            self.setSystemMessage(doId, Localizer.WhisperFriendComingOnline % friend.getName())
        return

    def __friendOffline(self, doId):
        friend = toonbase.tcr.identifyFriend(doId)
        if friend != None:
            self.setSystemMessage(0, Localizer.WhisperFriendLoggedOut % friend.getName())
        return

    def __clickedWhisper(self, doId):
        friend = toonbase.tcr.identifyFriend(doId)
        if friend != None:
            messenger.send('clickedNametag', [friend])
            self.chatMgr.whisperTo(friend.getName(), doId)
        return