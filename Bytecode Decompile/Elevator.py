from ShowBaseGlobal import *
from ToonBaseGlobal import *
from DirectGui import *
from IntervalGlobal import *
import PandaObject, FSM, State, StateData, DownloadForceAcknowledge, Localizer

class Elevator(PandaObject.PandaObject, StateData.StateData):
    __module__ = __name__

    def __init__(self, elevatorState, doneEvent, distElevator):
        StateData.StateData.__init__(self, doneEvent)
        self.fsm = FSM.FSM('Elevator', [
         State.State('start', self.enterStart, self.exitStart, [
          'elevatorDFA']),
         State.State('elevatorDFA', self.enterElevatorDFA, self.exitElevatorDFA, [
          'requestBoard', 'final']),
         State.State('requestBoard', self.enterRequestBoard, self.exitRequestBoard, [
          'boarding']),
         State.State('boarding', self.enterBoarding, self.exitBoarding, [
          'boarded']),
         State.State('boarded', self.enterBoarded, self.exitBoarded, [
          'requestExit', 'elevatorClosing', 'final']),
         State.State('requestExit', self.enterRequestExit, self.exitRequestExit, [
          'exiting', 'elevatorClosing']),
         State.State('elevatorClosing', self.enterElevatorClosing, self.exitElevatorClosing, [
          'final']),
         State.State('exiting', self.enterExiting, self.exitExiting, [
          'final']),
         State.State('final', self.enterFinal, self.exitFinal, [
          'start'])], 'start', 'final')
        self.dfaDoneEvent = 'elevatorDfaDoneEvent'
        self.elevatorState = elevatorState
        self.distElevator = distElevator
        return None
        return

    def load(self):
        self.elevatorState.addChild(self.fsm)
        self.buttonModels = loader.loadModelOnce('phase_3.5/models/gui/inventory_gui')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        return

    def unload(self):
        self.elevatorState.removeChild(self.fsm)
        del self.fsm
        del self.elevatorState
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        return

    def enter(self):
        self.fsm.enterInitialState()
        self.fsm.request('elevatorDFA')
        return None
        return

    def exit(self):
        self.ignoreAll()
        return None
        return

    def signalDone(self, doneStatus):
        messenger.send(self.doneEvent, [doneStatus])

    def enterStart(self):
        return None
        return

    def exitStart(self):
        return None
        return

    def enterElevatorDFA(self):
        self.acceptOnce(self.dfaDoneEvent, self.enterDFACallback)
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(self.dfaDoneEvent)
        self.dfa.enter(7)
        return

    def enterDFACallback(self, DFAdoneStatus):
        self.dfa.exit()
        del self.dfa
        if DFAdoneStatus['mode'] == 'complete':
            self.fsm.request('requestBoard')
        else:
            if DFAdoneStatus['mode'] == 'incomplete':
                elevatorDoneStatus = {}
                elevatorDoneStatus['where'] = 'reject'
                messenger.send(self.doneEvent, [elevatorDoneStatus])
            else:
                self.notify.error('Unrecognized doneStatus: ' + str(DFAdoneStatus))
        return

    def exitElevatorDFA(self):
        self.ignore(self.dfaDoneEvent)
        return

    def enterRequestBoard(self):
        messenger.send(self.distElevator.uniqueName('enterElevatorOK'))
        return None
        return

    def exitRequestBoard(self):
        return None
        return

    def enterBoarding(self, nodePath):
        camera.wrtReparentTo(nodePath)
        self.cameraBoardTrack = Track([
         LerpPosHprInterval(camera, 1.5, Point3(0, -16, 5.5), Point3(0, 0, 0))])
        self.cameraBoardTrack.play()
        return None
        return

    def exitBoarding(self):
        self.ignore('boardedElevator')
        return None
        return

    def enterBoarded(self):
        self.enableExitButton()
        return None
        return

    def exitBoarded(self):
        self.cameraBoardTrack.stop()
        self.disableExitButton()
        return None
        return

    def enableExitButton(self):
        self.exitButton = DirectButton(relief=None, text=Localizer.ElevatorHopOff, text_fg=(0.9, 0.9, 0.9, 1), text_pos=(0, -0.23), text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton), image_color=(0.5, 0.5, 0.5, 1), image_scale=(20, 1, 11), pos=(0, 0, 0.8), scale=0.15, command=lambda self=self: self.fsm.request('requestExit'))
        return
        return

    def disableExitButton(self):
        self.exitButton.destroy()
        return

    def enterRequestExit(self):
        messenger.send('elevatorExitButton')
        return None
        return

    def exitRequestExit(self):
        return None
        return

    def enterElevatorClosing(self):
        return None
        return

    def exitElevatorClosing(self):
        return None
        return

    def enterExiting(self):
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