from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
import OnscreenText, StateData, FSM, State, DirectNotifyGlobal, Localizer, GuiScreen, ToontownDialog

class NewPlayerScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('NewPlayerScreen')

    def __init__(self, tcr, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.allowNewAccounts = tcr.accountServerConstants.getBool('allowNewAccounts')
        self.fsm = FSM.FSM('NewPlayerScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'display']),
         State.State('display', self.enterDisplay, self.exitDisplay, [
          'off'])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        masterScale = 1.5
        textScale = 0.1 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 1.15 * masterScale
        buttonLineHeight = 0.14 * masterScale
        background = loader.loadModel('phase_3/models/gui/login-background')
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.frame = DirectFrame(parent=aspect2d, relief=None, image=background.find('**/first_time_install'))
        self.frame.hide()
        linePos = -0.3
        if self.allowNewAccounts:
            image_color = Vec4(1, 1, 1, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        else:
            g = 0.5
            image_color = Vec4(g, g, g, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_UP'))
        self.newAccountButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=imageSet, image_color=image_color, text=Localizer.NewPlayerScreenNewAccount, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleNewAccountButton)
        linePos -= buttonLineHeight
        self.loginButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.NewPlayerScreenLogin, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleLoginButton)
        linePos -= buttonLineHeight
        self.quitButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.NewPlayerScreenQuit, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleQuitButton)
        linePos -= buttonLineHeight
        self.dialogDoneEvent = 'newPlayerDialogAck'
        self.dialog = ToontownDialog.GlobalDialog(doneEvent=self.dialogDoneEvent, message='', style=ToontownDialog.Acknowledge)
        self.dialog.hide()
        background.removeNode()
        guiButton.removeNode()
        return

    def unload(self):
        self.dialog.cleanup()
        del self.dialog
        self.frame.destroy()
        del self.frame
        del self.fsm

    def enter(self):
        self.fsm.request('display')

    def exit(self):
        self.ignore(self.dialogDoneEvent)
        self.fsm.requestFinalState()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterDisplay(self):
        self.frame.show()

    def exitDisplay(self):
        self.frame.hide()

    def __handleNewAccountButton(self):
        if self.allowNewAccounts:
            messenger.send(self.doneEvent, [{'mode': 'newAccount'}])
            return
        self.dialog.setMessage(Localizer.LoginScreenNoNewAccounts)
        self.dialog.show()
        self.acceptOnce(self.dialogDoneEvent, self.__handleNoNewAccountsAck)

    def __handleLoginButton(self):
        messenger.send(self.doneEvent, [{'mode': 'login'}])

    def __handleQuitButton(self):
        messenger.send(self.doneEvent, [{'mode': 'quit'}])

    def __handleNoNewAccountsAck(self):
        self.dialog.hide()