from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
from TaskManagerGlobal import *
from SecretFriendsInfoPanel import *
from PrivacyPolicyPanel import *
import OnscreenText, StateData, ToontownDialog, FSM, State, DirectNotifyGlobal, Task, Localizer, TTAccount, GuiScreen, InputCheck

class ParentPasswordScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ParentPasswordScreen')
    ActiveEntryColor = Vec4(1, 1, 1, 1)
    InactiveEntryColor = Vec4(0.8, 0.8, 0.8, 1)

    def __init__(self, tcr, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.loginInterface = self.tcr.loginInterface

    def load(self):
        self.notify.debug('load')
        masterScale = 0.8
        textScale = 0.08 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 1.3 * masterScale
        buttonLineHeight = 0.16 * masterScale
        background = loader.loadModel('phase_3/models/gui/login-background')
        nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.frame = DirectFrame(parent=aspect2d, relief=FLAT, image=background.find('**/background_only'))
        self.frame.hide()
        self.titleLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.8), text=Localizer.ParentPasswordScreenTitle, text_font=getMinnieFont(), text_scale=0.14, text_fg=(1, 0.5, 0.1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.instructionsLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.8, 0, 0.6), text=Localizer.ParentPasswordScreenInstructions, text_scale=0.06, text_align=TextNode.ALeft, text_wordwrap=26, text_fg=(1, 1, 0.6, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.secretFriendsInfoButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, -0.34), scale=buttonScale * 0.8, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.ParentPasswordScreenSecretFriendsMoreInfo, text_scale=0.06, text_pos=(0, -0.02), image_scale=1.1, command=self.showSecretFriendsDetails)
        linePos = -0.54
        self.passwordLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.1, 0, linePos), text=Localizer.ParentPasswordScreenPassword, text_scale=textScale, text_align=TextNode.ARight, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.passwordEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.015, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1, obscured=1)
        linePos -= lineHeight
        self.passwordConfirmLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.1, 0, linePos), text=Localizer.ParentPasswordScreenConfirmPassword, text_scale=textScale, text_align=TextNode.ARight, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.passwordConfirmEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.015, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1, obscured=1, command=self.__handleConfirmCreatePassword)
        linePos -= lineHeight
        self.submitButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.ParentPasswordScreenSubmit, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.4, 1.1, 1.1), command=self.__handleSubmit)
        linePos -= buttonLineHeight
        self.privacyPolicyButton = DirectButton(parent=self.frame, relief=None, pos=(1.1, 0, -0.94), scale=1.1, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 0.8, 0.8), text=Localizer.ParentPasswordScreenPrivacyPolicy, text_pos=(0, -0.012), text_scale=0.054, command=self.showPrivacyPolicy)
        self.dialogDoneEvent = 'parentPasswordDialogAck'
        self.dialog = ToontownDialog.GlobalDialog(dialogName='parentPasswordDialog', doneEvent=self.dialogDoneEvent, message='', text_wordwrap=15, style=ToontownDialog.Acknowledge, sortOrder=NO_FADE_SORT_INDEX + 100)
        self.dialog.hide()
        guiButton.removeNode()
        background.removeNode()
        nameBalloon.removeNode()
        return

    def unload(self):
        self.notify.debug('unload')
        self.dialog.cleanup()
        del self.dialog
        self.frame.destroy()
        del self.tcr

    def enter(self):
        if hasattr(self.tcr, 'justPaid'):
            self.justPaid = 1
            del self.tcr.justPaid
        else:
            self.justPaid = 0
        self.password = ''
        self.passwordEntry.set('')
        self.passwordConfirmEntry.set('')
        self.focusList = [
         self.passwordEntry, self.passwordConfirmEntry]
        self.startFocusMgmt(overrides={self.passwordConfirmEntry: GuiScreen.GuiScreen.ENTERPRESS_REMOVE_FOCUS})
        self.frame.show()

    def exit(self):
        self.ignore(self.dialogDoneEvent)
        self.stopFocusMgmt()
        self.frame.hide()

    def __handleConfirmCreatePassword(self, password):
        if password != '':
            if self.passwordEntry.get() == '':
                self.setFocus(self.passwordEntry)
            else:
                self.__handleSubmit()
        else:
            self.setFocus(self.passwordConfirmEntry)

    def __handleSubmit(self):
        self.removeFocus()
        self.password = self.passwordEntry.get()
        passwordConfirm = self.passwordConfirmEntry.get()
        minPwdLength = self.tcr.accountServerConstants.getInt('minPwLength')
        if len(self.password) < minPwdLength:
            self.dialog.setMessage(Localizer.ParentPasswordScreenPasswordTooShort % minPwdLength)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
        if self.password != passwordConfirm:
            self.dialog.setMessage(Localizer.ParentPasswordScreenPasswordMismatch)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
        try:
            self.loginInterface.setParentPassword(self.tcr.userName, self.tcr.password, self.password)
        except TTAccount.TTAccountException, e:
            self.notify.info(str(e))
            if self.justPaid:
                err = Localizer.ParentPasswordScreenConnectionProblemJustPaid
            else:
                err = Localizer.ParentPasswordScreenConnectionProblemJustLoggedIn
            self.dialog.setMessage(err)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleConnectionProblemAck)
        else:
            messenger.send(self.doneEvent, [{'mode': 'success'}])

    def __handlePasswordAck(self):
        self.dialog.hide()
        self.setFocus(self.passwordEntry)
        self.password = ''
        self.passwordEntry.set('')
        self.passwordConfirmEntry.set('')

    def __handleConnectionProblemAck(self):
        self.dialog.hide()
        messenger.send(self.doneEvent, [{'mode': 'failure'}])

    def showSecretFriendsDetails(self):
        self.removeFocus()
        secretFriendsInfoDone = 'secretFriendsInfoDone'
        self.secretFriendsInfo = SecretFriendsInfoPanel(secretFriendsInfoDone)

        def hideSecretFriendsDetails(self=self):
            self.secretFriendsInfo.hide()
            self.secretFriendsInfo.cleanup()
            del self.secretFriendsInfo
            self.restoreFocus()

        self.acceptOnce(secretFriendsInfoDone, hideSecretFriendsDetails)
        self.secretFriendsInfo.show()

    def showPrivacyPolicy(self):
        self.removeFocus()
        ppDoneEvent = 'privacyPolicyDone'
        self.privacyPolicyDialog = PrivacyPolicyPanel(ppDoneEvent)
        self.privacyPolicyDialog.show()

        def hidePrivacyPolicy(self=self):
            self.privacyPolicyDialog.hide()
            self.privacyPolicyDialog.cleanup()
            del self.privacyPolicyDialog
            self.restoreFocus()

        self.acceptOnce(ppDoneEvent, hidePrivacyPolicy)