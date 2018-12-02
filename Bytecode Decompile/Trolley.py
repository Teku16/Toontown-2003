from ShowBaseGlobal import *
from ToonBaseGlobal import *
from DirectGui import *
from IntervalGlobal import *
import PandaObject, FSM, State, StateData, ToontownDialog, ToontownGlobals, Localizer

class Trolley(PandaObject.PandaObject, StateData.StateData):
    __module__ = __name__

    def __init__(self, safeZone, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.fsm = FSM.FSM('Trolley', [
         State.State('start', self.enterStart, self.exitStart, [
          'requestBoard', 'trolleyHFA', 'trolleyTFA']),
         State.State('trolleyHFA', self.enterTrolleyHFA, self.exitTrolleyHFA, [
          'final']),
         State.State('trolleyTFA', self.enterTrolleyTFA, self.exitTrolleyTFA, [
          'final']),
         State.State('requestBoard', self.enterRequestBoard, self.exitRequestBoard, [
          'boarding']),
         State.State('boarding', self.enterBoarding, self.exitBoarding, [
          'boarded']),
         State.State('boarded', self.enterBoarded, self.exitBoarded, [
          'requestExit', 'trolleyLeaving', 'final']),
         State.State('requestExit', self.enterRequestExit, self.exitRequestExit, [
          'exiting', 'trolleyLeaving']),
         State.State('trolleyLeaving', self.enterTrolleyLeaving, self.exitTrolleyLeaving, [
          'final']),
         State.State('exiting', self.enterExiting, self.exitExiting, [
          'final']),
         State.State('final', self.enterFinal, self.exitFinal, [
          'start'])], 'start', 'final')
        self.parentFSM = parentFSM
        return None
        return

    def load(self):
        self.parentFSM.getStateNamed('trolley').addChild(self.fsm)
        self.buttonModels = loader.loadModelOnce('phase_3.5/models/gui/inventory_gui')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        return

    def unload(self):
        self.parentFSM.getStateNamed('trolley').removeChild(self.fsm)
        del self.fsm
        del self.parentFSM
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        return

    def enter(self):
        self.fsm.enterInitialState()
        if toonbase.localToon.hp > 0:
            messenger.send('enterTrolleyOK')
            self.fsm.request('requestBoard')
        else:
            self.fsm.request('trolleyHFA')
        return None
        return

    def exit(self):
        self.ignoreAll()
        return None
        return

    def enterStart(self):
        return None
        return

    def exitStart(self):
        return None
        return

    def enterTrolleyHFA(self):
        self.noTrolleyBox = ToontownDialog.GlobalDialog(message=Localizer.TrolleyHFAMessage, doneEvent='noTrolleyAck', style=ToontownDialog.Acknowledge)
        self.noTrolleyBox.show()
        toonbase.localToon.b_setAnimState('neutral', 1)
        self.accept('noTrolleyAck', self.__handleNoTrolleyAck)
        return

    def exitTrolleyHFA(self):
        self.ignore('noTrolleyAck')
        self.noTrolleyBox.cleanup()
        del self.noTrolleyBox
        return

    def enterTrolleyTFA(self):
        self.noTrolleyBox = ToontownDialog.GlobalDialog(message=Localizer.TrolleyTFAMessage, doneEvent='noTrolleyAck', style=ToontownDialog.Acknowledge)
        self.noTrolleyBox.show()
        toonbase.localToon.b_setAnimState('neutral', 1)
        self.accept('noTrolleyAck', self.__handleNoTrolleyAck)
        return

    def exitTrolleyTFA(self):
        self.ignore('noTrolleyAck')
        self.noTrolleyBox.cleanup()
        del self.noTrolleyBox
        return

    def __handleNoTrolleyAck(self):
        ntbDoneStatus = self.noTrolleyBox.doneStatus
        if ntbDoneStatus == 'ok':
            doneStatus = {}
            doneStatus['mode'] = 'reject'
            messenger.send(self.doneEvent, [doneStatus])
        else:
            self.notify.error('Unrecognized doneStatus: ' + str(ntbDoneStatus))
        return

    def enterRequestBoard(self):
        return None
        return

    def handleRejectBoard(self):
        doneStatus = {}
        doneStatus['mode'] = 'reject'
        messenger.send(self.doneEvent, [doneStatus])

    def exitRequestBoard(self):
        return None
        return

    def enterBoarding(self, nodePath):
        camera.wrtReparentTo(nodePath)
        self.cameraBoardTrack = LerpPosHprInterval(camera, 1.5, Point3(-35, 0, 8), Point3(-90, 0, 0))
        self.cameraBoardTrack.start()
        return None
        return

    def exitBoarding(self):
        self.ignore('boardedTrolley')
        return None
        return

    def enterBoarded(self):
        self.enableExitButton()
        return None
        return

    def exitBoarded(self):
        self.cameraBoardTrack.finish()
        self.disableExitButton()
        return None
        return

    def enableExitButton(self):
        self.exitButton = DirectButton(relief=None, text=Localizer.TrolleyHopOff, text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton), image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0, 0, 0.8), scale=0.15, command=lambda self=self: self.fsm.request('requestExit'))
        return
        return

    def disableExitButton(self):
        self.exitButton.destroy()
        return

    def enterRequestExit(self):
        messenger.send('trolleyExitButton')
        return None
        return

    def exitRequestExit(self):
        return None
        return

    def enterTrolleyLeaving(self):
        messenger.send('trolleyLeaving')
        camera.lerpPosHprXYZHPR(0, 18.55, 3.75, -180, 0, 0, 3, blendType='easeInOut', task='leavingCamera')
        self.acceptOnce('playMinigame', self.handlePlayMinigame)
        return None
        return

    def handlePlayMinigame(self, zoneId, minigameId):
        toonbase.localToon.b_setParent(ToontownGlobals.SPHidden)
        doneStatus = {}
        doneStatus['mode'] = 'minigame'
        doneStatus['zoneId'] = zoneId
        doneStatus['minigameId'] = minigameId
        messenger.send(self.doneEvent, [doneStatus])

    def exitTrolleyLeaving(self):
        self.ignore('playMinigame')
        taskMgr.remove('leavingCamera')
        return None
        return

    def enterExiting(self):
        return None
        return

    def handleOffTrolley(self):
        doneStatus = {}
        doneStatus['mode'] = 'exit'
        messenger.send(self.doneEvent, [doneStatus])
        return None
        return

    def exitExiting(self):
        return None
        return

    def enterFinal(self):
        return None
        return

    def exitFinal(self):
        return None
        return