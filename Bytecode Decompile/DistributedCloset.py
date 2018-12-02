from DirectGui import *
from ToontownGlobals import *
from ToonBaseGlobal import *
from ShowBaseGlobal import *
from IntervalGlobal import *
from ClockDelta import *
import ToontownGlobals, PandaObject, AvatarDNA, StateData, ClosetGUI, ClosetGlobals, DistributedObject, Localizer, CollisionSphere, CollisionNode

class DistributedCloset(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedCloset')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.notify.debug('__init__')
        self.av = None
        self.closetGUI = None
        self.closetNode = None
        self.closetSphere = None
        self.closetSphereNode = None
        self.closetSphereNodePath = None
        self.topList = []
        self.botList = []
        self.oldTopList = []
        self.oldBotList = []
        self.oldStyle = None
        self.button = None
        self.topTrashButton = None
        self.bottomTrashButton = None
        self.isLocalToon = None
        self.popupInfo = None
        self.isOwner = 0
        self.ownerId = 0
        self.customerId = 0
        self.purchaseDoneEvent = ''
        self.swapEvent = ''
        self.locked = 0
        self.gender = None
        self.topDeleted = 0
        self.bottomDeleted = 0
        self.closetTrack = None
        self.avMoveTrack = None
        self.fsm = FSM.FSM('Closet', [
         State.State('off', self.enterOff, self.exitOff, [
          'ready', 'open', 'closed']),
         State.State('ready', self.enterReady, self.exitReady, [
          'open', 'closed']),
         State.State('closed', self.enterClosed, self.exitClosed, [
          'open', 'off']),
         State.State('open', self.enterOpen, self.exitOpen, [
          'closed', 'off'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.load()
        return

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        self.fsm.request('ready')
        self.setupCollisionSphere()

    def load(self):
        self.closetNode = render.find('**/closet_origin')
        self.closetModel = self.closetNode.getParent()
        lNode = self.closetModel.find('**/door_rotate_L')
        lDoor = self.closetModel.find('**/closetdoor_L')
        lDoor.wrtReparentTo(lNode)
        self.leftDoor = lNode
        rNode = self.closetModel.find('**/door_rotate_R')
        rDoor = self.closetModel.find('**/closetdoor_R')
        rDoor.wrtReparentTo(rNode)
        self.rightDoor = rNode

    def setupCollisionSphere(self):
        if self.ownerId:
            self.closetSphere = CollisionSphere.CollisionSphere(0, 0, 0, 1.8)
            self.closetSphere.setTangible(0)
            self.closetSphereNode = CollisionNode.CollisionNode(self.uniqueName('closetSphere'))
            self.closetSphereNode.setIntoCollideMask(WallBitmask)
            self.closetSphereNode.addSolid(self.closetSphere)
            self.closetSphereNodePath = self.closetNode.attachNewNode(self.closetSphereNode)
            self.closetSphereNodePath.reparentTo(self.closetNode)

    def disable(self):
        self.notify.debug('disable')
        self.ignore(self.uniqueName('enterclosetSphere'))
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupChangeClothesGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        taskMgr.remove(self.uniqueName('lerpToon'))
        if self.closetGUI:
            self.closetGUI.resetClothes(self.oldStyle)
            self.resetCloset()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.notify.debug('delete')
        DistributedObject.DistributedObject.delete(self)
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.av:
            del self.av
        del self.gender
        del self.closetSphere
        del self.closetSphereNode
        del self.closetSphereNodePath
        del self.closetModel
        del self.closetNode
        del self.closetGUI
        return

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterReady(self):
        if self.ownerId:
            self.accept(self.uniqueName('enterclosetSphere'), self.handleEnterSphere)

    def exitReady(self):
        pass

    def enterOpen(self):
        if self.ownerId:
            self.ignore(self.uniqueName('enterclosetSphere'))
            self.__openDoors()
            if self.customerId == toonbase.localToon.doId:
                camera.wrtReparentTo(self.closetNode)
                camera.lerpPosHpr(-7.58, -6.02, 6.9, 286.3, 336.8, 0, 1, other=self.closetNode, blendType='easeOut', task=self.uniqueName('lerpCamera'))
                camera.setPosHpr(self.closetNode, -7.58, -6.02, 6.9, 286.3, 336.8, 0)
            if self.av:
                if self.avMoveTrack:
                    self.avMoveTrack.stop()
                self.av.stopSmooth()
                self.avMoveTrack = Sequence(Parallel(Func(self.av.play, 'walk'), LerpPosHprInterval(node=self.av, other=self.closetNode, duration=1.0, pos=Vec3(1.67, -3.29, 0.025), hpr=Vec3(112, 0, 0), blendType='easeOut')), Func(self.av.loop, 'neutral'), Func(self.av.startSmooth))
                self.avMoveTrack.play()

    def exitOpen(self):
        if self.ownerId:
            self.__closeDoors()

    def enterClosed(self):
        if self.ownerId:
            self.accept(self.uniqueName('enterclosetSphere'), self.handleEnterSphere)

    def exitClosed(self):
        pass

    def handleEnterSphere(self, collEntry):
        self.notify.debug('Entering Closet Sphere....%s' % self.uniqueName('enterclosetSphere'))
        self.ignore(self.uniqueName('enterclosetSphere'))
        if not self.locked:
            self.sendUpdate('enterAvatar', [])

    def setState(self, mode, avId, ownerId, gender, topList, botList):
        self.notify.debug('setState, mode=%s, avId=%s, ownerId=%d' % (mode, avId, ownerId))
        self.isOwner = avId == ownerId
        self.ownerGender = gender
        if mode == ClosetGlobals.CLOSED:
            self.fsm.request('closed')
            return
        else:
            if mode == ClosetGlobals.OPEN:
                self.customerId = avId
                self.av = self.cr.doId2do.get(self.customerId, None)
                if self.av:
                    if toonbase.localToon.getDoId() == self.customerId:
                        self.cr.playGame.getPlace().detectedClosetCollision()
                        self.gender = self.av.style.gender
                        self.topList = topList
                        self.botList = botList
                        self.oldTopList = self.topList[0:]
                        self.oldBotList = self.botList[0:]
                        if not self.isOwner:
                            self.__popupNotOwnerPanel()
                        else:
                            taskMgr.doMethodLater(0.5, self.popupChangeClothesGUI, self.uniqueName('popupChangeClothesGUI'))
                    self.fsm.request('open')
        return

    def __revertGender(self):
        if self.gender:
            self.av.style.gender = self.gender
            self.av.loop('neutral')

    def popupChangeClothesGUI(self, task):
        self.notify.debug('popupChangeClothesGUI')
        self.purchaseDoneEvent = self.uniqueName('purchaseDone')
        self.swapEvent = self.uniqueName('swap')
        self.cancelEvent = self.uniqueName('cancel')
        self.accept(self.purchaseDoneEvent, self.__proceedToCheckout)
        self.accept(self.swapEvent, self.__handleSwap)
        self.accept(self.cancelEvent, self.__handleCancel)
        self.deleteEvent = self.uniqueName('delete')
        if self.isOwner:
            self.accept(self.deleteEvent, self.__handleDelete)
        self.closetGUI = ClosetGUI.ClosetGUI(self.isOwner, self.purchaseDoneEvent, self.cancelEvent, self.swapEvent, self.deleteEvent, self.topList, self.botList)
        self.closetGUI.load()
        if self.gender != self.ownerGender:
            self.closetGUI.setGender(self.ownerGender)
        self.closetGUI.enter(toonbase.localToon)
        self.closetGUI.showButtons()
        if toonbase.localToon.getHeight() > 3.5:
            self.closetGUI.topLButton.setZ(0.1)
            self.closetGUI.topRButton.setZ(0.1)
            self.closetGUI.bottomLButton.setZ(-0.3)
            self.closetGUI.bottomRButton.setZ(-0.3)
        else:
            self.closetGUI.topLButton.setZ(0)
            self.closetGUI.topRButton.setZ(0)
            self.closetGUI.bottomLButton.setZ(-0.4)
            self.closetGUI.bottomRButton.setZ(-0.4)
        style = self.av.getStyle()
        self.oldStyle = AvatarDNA.AvatarDNA()
        self.oldStyle.makeFromNetString(style.makeNetString())
        return Task.done

    def resetCloset(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupChangeClothesGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        taskMgr.remove(self.uniqueName('lerpToon'))
        if self.closetGUI:
            self.closetGUI.hideButtons()
            self.closetGUI.exit()
            self.closetGUI.unload()
            self.closetGUI = None
            del self.av
        self.av = toonbase.localToon
        style = self.av.getStyle()
        self.oldStyle = AvatarDNA.AvatarDNA()
        self.oldStyle.makeFromNetString(style.makeNetString())
        self.topDeleted = 0
        self.bottomDeleted = 0
        return Task.done
        return

    def __handleButton(self):
        messenger.send('next')

    def __handleCancel(self):
        self.d_setDNA(self.oldStyle.makeNetString(), 1)
        self.closetGUI.resetClothes(self.oldStyle)

    def __handleSwap(self):
        self.d_setDNA(self.av.getStyle().makeNetString(), 0)

    def __handleDelete(self, t_or_b):
        if t_or_b == ClosetGlobals.SHIRT:
            itemList = self.closetGUI.tops
            trashIndex = self.closetGUI.topChoice
            swapFunc = self.closetGUI.swapTop
            removeFunc = self.closetGUI.removeTop
            self.topDeleted = self.topDeleted | 1

            def setItemChoice(i):
                self.closetGUI.topChoice = i

        else:
            itemList = self.closetGUI.bottoms
            trashIndex = self.closetGUI.bottomChoice
            swapFunc = self.closetGUI.swapBottom
            removeFunc = self.closetGUI.removeBottom
            self.bottomDeleted = self.bottomDeleted | 1

            def setItemChoice(i):
                self.closetGUI.bottomChoice = i

        if len(itemList) > 1:
            trashDNA = AvatarDNA.AvatarDNA()
            trashItem = self.av.getStyle().makeNetString()
            trashDNA.makeFromNetString(trashItem)
            if trashIndex == 0:
                swapFunc(1)
            else:
                swapFunc(-1)
            removeFunc(trashIndex)
            self.sendUpdate('removeItem', [trashItem, t_or_b])
            swapFunc(0)
            self.closetGUI.updateTrashButtons()
        else:
            self.notify.warning("cant delete this item(type = %s), since we don't have a replacement" % t_or_b)

    def resetItemLists(self):
        self.topList = self.oldTopList[0:]
        self.botList = self.oldBotList[0:]
        self.closetGUI.tops = self.topList
        self.closetGUI.bottoms = self.botList
        self.topDeleted = 0
        self.bottomDeleted = 0

    def __proceedToCheckout(self):
        if self.topDeleted or self.bottomDeleted:
            self.__popupAreYouSurePanel()
        else:
            self.__handlePurchaseDone()

    def __handlePurchaseDone(self, timeout=0):
        if timeout == 1:
            self.d_setDNA(self.oldStyle.makeNetString(), 1)
        else:
            which = 0
            if self.closetGUI.topChoice != 0 or self.topDeleted:
                which = which | 1
            if self.closetGUI.bottomChoice != 0 or self.bottomDeleted:
                which = which | 2
            self.d_setDNA(self.av.getStyle().makeNetString(), 2, which)

    def d_setDNA(self, dnaString, finished, whichItems=3):
        self.sendUpdate('setDNA', [dnaString, finished, whichItems])

    def setMovie(self, mode, avId, timestamp):
        self.isLocalToon = avId == toonbase.localToon.doId
        if mode == ClosetGlobals.CLOSET_MOVIE_CLEAR:
            return
        if mode == ClosetGlobals.CLOSET_MOVIE_COMPLETE:
            self.__revertGender()
            self.resetCloset()
            self.freeAvatar()
            return
        if mode == ClosetGlobals.CLOSET_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            taskMgr.remove(self.uniqueName('lerpToon'))
            if self.isLocalToon:
                self.ignore(self.purchaseDoneEvent)
                self.ignore(self.swapEvent)
                if self.closetGUI:
                    self.closetGUI.resetClothes(self.oldStyle)
                    self.__handlePurchaseDone(timeout=1)
                    self.resetCloset()
                self.__popupTimeoutPanel()
                self.freeAvatar()

    def freeAvatar(self):
        if self.isLocalToon:
            toonbase.localToon.posCamera(0, 0)
            toonbase.tcr.playGame.getPlace().setState('walk')
            toonbase.localToon.startLookAround()
        self.fsm.request('off')

    def setOwnerId(self, avId):
        self.ownerId = avId

    def __popupTimeoutPanel(self):
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.popupInfo = DirectFrame(parent=hidden, relief=None, state='normal', text=Localizer.ClosetTimeoutMessage, frameSize=(-1, 1, -1, 1), geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.88, 1, 0.45), geom_pos=(0, 0, -0.08), text_scale=0.08)
        DirectButton(self.popupInfo, image=okButtonImage, relief=None, text=Localizer.ClosetPopupOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.16), command=self.__handleTimeoutMessageOK)
        buttons.removeNode()
        self.popupInfo.reparentTo(aspect2d)
        return

    def __handleTimeoutMessageOK(self):
        self.popupInfo.reparentTo(hidden)

    def __popupNotOwnerPanel(self):
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.popupInfo = DirectFrame(parent=hidden, relief=None, state='normal', text=Localizer.ClosetNotOwnerMessage, frameSize=(-1, 1, -1, 1), text_wordwrap=10, geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.88, 1, 0.55), geom_pos=(0, 0, -0.08), text_scale=0.08, text_pos=(0, 0.06))
        DirectButton(self.popupInfo, image=okButtonImage, relief=None, text=Localizer.ClosetPopupOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.21), command=self.__handleNotOwnerMessageOK)
        buttons.removeNode()
        self.popupInfo.reparentTo(aspect2d)
        return

    def __handleNotOwnerMessageOK(self):
        self.popupInfo.reparentTo(hidden)
        taskMgr.doMethodLater(0.1, self.popupChangeClothesGUI, self.uniqueName('popupChangeClothesGUI'))

    def __popupAreYouSurePanel(self):
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelButtonImage = (
         buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
        self.popupInfo = DirectFrame(parent=hidden, relief=None, state='normal', text=Localizer.ClosetAreYouSureMessage, frameSize=(-1, 1, -1, 1), text_wordwrap=10, geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.88, 1, 0.55), geom_pos=(0, 0, -0.08), text_scale=0.08, text_pos=(0, 0.08))
        DirectButton(self.popupInfo, image=okButtonImage, relief=None, text=Localizer.ClosetYes, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.1, 0.0, -0.21), command=self.__handleYesImSure)
        DirectButton(self.popupInfo, image=cancelButtonImage, relief=None, text=Localizer.ClosetNo, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.1, 0.0, -0.21), command=self.__handleNotSure)
        buttons.removeNode()
        self.popupInfo.reparentTo(aspect2d)
        return

    def __handleYesImSure(self):
        self.popupInfo.reparentTo(hidden)
        self.__handlePurchaseDone()

    def __handleNotSure(self):
        self.popupInfo.reparentTo(hidden)

    def __openDoors(self):
        if self.closetTrack:
            self.closetTrack.stop()
        leftHpr = Vec3(-110, 0, 0)
        rightHpr = Vec3(110, 0, 0)
        self.closetTrack = Parallel(LerpHprInterval(self.rightDoor, 0.5, rightHpr, other=self.closetNode), LerpHprInterval(self.leftDoor, 0.5, leftHpr, other=self.closetNode))
        self.closetTrack.play()

    def __closeDoors(self):
        if self.closetTrack:
            self.closetTrack.stop()
        leftHpr = Vec3(0, 0, 0)
        rightHpr = Vec3(0, 0, 0)
        self.closetOpenTrack = Parallel(LerpHprInterval(self.rightDoor, 0.5, rightHpr, other=self.closetNode), LerpHprInterval(self.leftDoor, 0.5, leftHpr, other=self.closetNode))
        self.closetOpenTrack.play()