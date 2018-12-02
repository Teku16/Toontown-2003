from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
from TaskManagerGlobal import *
import OnscreenText, StateData, ToontownDialog, FSM, State, DirectNotifyGlobal, Task, Localizer, GuiScreen

class WelcomeScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('WelcomeScreen')

    def __init__(self, tcr, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.fsm = FSM.FSM('WelcomeScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'display']),
         State.State('display', self.enterDisplay, self.exitDisplay, [])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        masterScale = 0.8
        textScale = 0.1 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 1.38 * masterScale
        buttonLineHeight = 0.17 * masterScale
        self.screen = loader.loadModel('phase_3/models/gui/login-background').find('**/welcome')
        self.screen.hide()
        self.screen.reparentTo(aspect2d)
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.welcomeLabel = DirectLabel(parent=self.screen, relief=None, pos=(0, 0, -0.06), text=Localizer.WelcomeScreenHeading, text_font=getMinnieFont(), text_scale=0.16, text_fg=Vec4(0.6, 0.1, 0.1, 1))
        self.sentence1Label = DirectLabel(parent=self.screen, relief=None, pos=(0, 0, -0.19), text=Localizer.WelcomeScreenSentence1, text_scale=0.09)
        self.toontownLabel = DirectLabel(parent=self.screen, relief=None, pos=(0, 0, -0.32), text=Localizer.WelcomeScreenToontown, text_font=getMinnieFont(), text_scale=0.09, text_fg=Vec4(0.8, 0.1, 0.1, 1))
        self.upsellLabel = DirectLabel(parent=self.screen, relief=None, pos=(0, 0, -0.44), scale=0.35, text=Localizer.WelcomeScreenSentence2, text_scale=0.17, text_fg=(0, 0, 0, 1), text_wordwrap=20)
        self.okButton = DirectButton(parent=self.screen, relief=None, pos=(0, 0, -0.62), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.WelcomeScreenOk, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleOkButton)
        guiButton.removeNode()
        return

    def unload(self):
        self.screen.removeNode()
        self.welcomeLabel.destroy()
        self.sentence1Label.destroy()
        self.toontownLabel.destroy()
        self.upsellLabel.destroy()
        self.okButton.destroy()
        del self.screen
        del self.fsm

    def enter(self):
        self.fsm.request('display')

    def exit(self):
        self.fsm.requestFinalState()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterDisplay(self):
        self.screen.show()

    def exitDisplay(self):
        self.screen.hide()

    def __handleOkButton(self):
        messenger.send(self.doneEvent, [{'mode': 'ok'}])

    def __handleQuitButton(self):
        messenger.send(self.doneEvent, [{'mode': 'quit'}])