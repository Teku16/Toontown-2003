from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
from TaskManagerGlobal import *
from DateOfBirthEntry import *
import OnscreenText, StateData, ToontownDialog, FSM, State, DirectNotifyGlobal, Task, Localizer, TTAccount, GuiScreen, calendar, InputCheck

class CreateAccountScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateAccountScreen')
    ActiveEntryColor = Vec4(1, 1, 1, 1)
    InactiveEntryColor = Vec4(0.8, 0.8, 0.8, 1)
    labelFg = (
     1, 1, 1, 1)
    labelFgActive = (1, 1, 0, 1)
    getEmailUnder13 = 1

    def __init__(self, tcr, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.loginInterface = self.tcr.loginInterface
        self.fsm = FSM.FSM('CreateAccountScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'create']),
         State.State('create', self.enterCreate, self.exitCreate, [
          'waitForLoginResponse', 'getEmail', 'create']),
         State.State('getEmail', self.enterGetEmail, self.exitGetEmail, [
          'waitForLoginResponse', 'getEmail']),
         State.State('waitForLoginResponse', self.enterWaitForLoginResponse, self.exitWaitForLoginResponse, [
          'create'])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        self.notify.debug('load')
        masterScale = 0.8
        textScale = 0.1 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 1.3 * masterScale
        buttonLineHeight = 0.16 * masterScale
        background = loader.loadModel('phase_3/models/gui/login-background')
        nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.frame = DirectFrame(parent=aspect2d, relief=FLAT, image=background.find('**/create_account'))
        self.frame.hide()
        self.EMAIL_WIDTH = self.ENTRY_WIDTH
        linePos = 0.5
        linePos -= lineHeight
        self.freeTrialLengthLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.3), scale=1.09, text=Localizer.CreateAccountScreenFreeTrialLength % self.tcr.accountServerConstants.getString('freeTrialPeriodInDays'), text_scale=textScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.freeLabel = DirectLabel(parent=self.freeTrialLengthLabel, relief=None, pos=(0.02, 0, 0), text=Localizer.CreateAccountScreenFree, text_font=getMinnieFont(), text_scale=textScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        linePos -= lineHeight
        self.instructionsLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, linePos), text='', text_scale=textScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.instructionsLabel.hide()
        linePos -= lineHeight
        self.nameLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.CreateAccountScreenUserName, text_scale=textScale, text_align=TextNode.ARight, text_fg=self.labelFg, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.nameEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.125, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1)
        self.nameEntry.label = self.nameLabel
        linePos -= lineHeight
        self.passwordLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.CreateAccountScreenPassword, text_scale=textScale, text_align=TextNode.ARight, text_fg=self.labelFg, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.passwordEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.125, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1, obscured=1)
        self.passwordEntry.label = self.passwordLabel
        linePos -= lineHeight
        self.passwordConfirmLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.CreateAccountScreenConfirmPassword, text_scale=textScale, text_align=TextNode.ARight, text_fg=self.labelFg, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.passwordConfirmEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.125, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1, obscured=1)
        self.passwordConfirmEntry.label = self.passwordConfirmLabel
        linePos -= lineHeight
        self.dobLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.DateOfBirthEntryDefaultLabel, text_scale=textScale, text_align=TextNode.ARight, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.dobEntry = DateOfBirthEntry(parent=self.frame, pos=(-0.02, 0, linePos), scale=textScale, defaultAge=0, curYear=self.tcr.dateObject.getYear())
        self.dobEntry.label = self.dobLabel
        linePos -= lineHeight
        self.submitButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.CreateAccountScreenSubmit, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleSubmit)
        linePos -= buttonLineHeight
        self.cancelButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.3, 1.1, 1.1), image0_color=Vec4(1, 0.1, 0.1, 1), image1_color=Vec4(1, 0.1, 0.1, 1), image2_color=Vec4(1, 1, 1, 1), text=Localizer.CreateAccountScreenCancel, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleCancel)
        linePos -= buttonLineHeight
        self.dialogDoneEvent = 'createAccountDialogAck'
        self.dialog = ToontownDialog.GlobalDialog(dialogName='createAccountDialog', doneEvent=self.dialogDoneEvent, message='', style=ToontownDialog.Acknowledge, sortOrder=NO_FADE_SORT_INDEX + 100)
        self.dialog.hide()
        self.emailPanel = DirectFrame(relief=None, pos=(0, 0.1, 0), image=getDefaultDialogGeom(), image_color=GlobalDialogColor, image_scale=(1.55, 1.0, 1.0), sortOrder=NO_FADE_SORT_INDEX)
        lineHeight *= 0.7
        linePos = 0.4
        self.emailLabel = DirectLabel(parent=self.emailPanel, relief=None, pos=(0, 0, linePos), text=Localizer.CreateAccountScreenEmailInstructions, text_scale=0.06, text_align=TextNode.ACenter)
        self.emailLabelUnder13 = DirectLabel(parent=self.emailPanel, relief=None, pos=(0, 0, linePos - lineHeight * 0.8), text=Localizer.CreateAccountScreenEmailInstructionsUnder13, text_scale=0.06, text_align=TextNode.ACenter, text_wordwrap=25)
        linePos -= lineHeight * 2.95
        self.emailEntry = DirectEntry(parent=self.emailPanel, relief=SUNKEN, scale=0.06, pos=(-0.61, 0, linePos), borderWidth=(0.1, 0.1), numLines=1, cursorKeys=1, frameSize=(-0.2, self.EMAIL_WIDTH, -0.4, 1.1), width=self.EMAIL_WIDTH, frameColor=(0.8, 0.8, 0.5, 1))
        linePos -= lineHeight
        self.emailConfirmLabel = DirectLabel(parent=self.emailPanel, relief=None, pos=(0, 0, linePos), text=Localizer.CreateAccountScreenEmailConfirm, text_scale=0.06, text_align=TextNode.ACenter)
        linePos -= lineHeight
        self.emailConfirmEntry = DirectEntry(parent=self.emailPanel, relief=SUNKEN, scale=0.06, pos=(-0.61, 0, linePos), borderWidth=(0.1, 0.1), numLines=1, cursorKeys=1, frameSize=(-0.2, self.EMAIL_WIDTH, -0.4, 1.1), width=self.EMAIL_WIDTH, frameColor=(0.8, 0.8, 0.5, 1), command=self.__handleEmailConfirmEntry)
        linePos -= lineHeight
        self.emailOkButton = DirectButton(parent=self.emailPanel, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.CreateAccountScreenEmailPanelSubmit, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleEmailSubmit)
        linePos -= lineHeight
        self.emailCancelButton = DirectButton(parent=self.emailPanel, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.3, 1.1, 1.1), image0_color=Vec4(1, 0.1, 0.1, 1), image1_color=Vec4(1, 0.1, 0.1, 1), image2_color=Vec4(1, 1, 1, 1), text=Localizer.CreateAccountScreenEmailPanelCancel, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleEmailCancel)
        self.emailPanel.hide()
        guiButton.removeNode()
        background.removeNode()
        nameBalloon.removeNode()
        return

    def unload(self):
        self.notify.debug('unload')
        self.dialog.cleanup()
        del self.dialog
        self.emailPanel.destroy()
        del self.emailPanel
        self.frame.destroy()
        del self.fsm
        del self.loginInterface
        del self.tcr

    def enter(self):
        self.__firstTime = 1
        self.__validatedEmail = 0
        self.frame.show()
        self.fsm.request('create')

    def exit(self):
        self.ignore(self.dialogDoneEvent)
        self.fsm.requestFinalState()
        self.frame.hide()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterCreate(self):
        self.password = ''
        self.passwordEntry.set('')
        self.passwordConfirmEntry.set('')
        if self.__firstTime:
            self.userName = ''
            self.nameEntry.set(self.userName)
            self.dobEntry.setMonthHandler(self.__handleDob)
            self.dobEntry.setYearHandler(self.__handleDob)
            self.dobEntry.setDayHandler(self.__handleDob)
            self.email = ''
        self.__firstTime = 0
        self.focusList = [
         self.nameEntry, self.passwordEntry, self.passwordConfirmEntry, self.dobEntry]
        self.startFocusMgmt(overrides={self.dobEntry: self.__handleDobEnterPress}, globalFocusHandler=self.__handleFocusChange)

    def exitCreate(self):
        self.stopFocusMgmt()

    def enterGetEmail(self):
        self.under13 = self.age < 13
        if self.under13 and not self.getEmailUnder13 or self.tcr.getCreditCardUpFront():
            self.email = ''
            self.fsm.request('waitForLoginResponse')
            return
        self.emailLabel.hide()
        self.emailLabelUnder13.hide()
        if self.under13:
            self.emailLabelUnder13.show()
        else:
            self.emailLabel.show()
        self.focusList = [self.emailEntry, self.emailConfirmEntry]
        self.startFocusMgmt(overrides={self.emailConfirmEntry: GuiScreen.GuiScreen.ENTERPRESS_REMOVE_FOCUS})
        self.emailEntry.enterText(self.email)
        if self.__validatedEmail:
            self.emailConfirmEntry.enterText(self.email)
            self.setFocus(self.emailConfirmEntry)
        else:
            self.emailConfirmEntry.enterText('')
        base.transitions.fadeScreen(0.5)
        self.emailPanel.show()

    def __handleEmailConfirmEntry(self, emailConfirm):
        if emailConfirm:
            self.__handleEmailSubmit()
        else:
            self.setFocus(self.emailConfirmEntry)

    def __handleEmailSubmit(self):
        self.email = self.emailEntry.get()

        def showErrorMsg(msg, self=self):
            self.dialog.setMessage(msg)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleInvalidEmailAck)
            self.emailPanel.hide()

        if self.emailEntry.get() == '' and self.emailConfirmEntry.get() == '':
            self.fsm.request('getEmail')
        else:
            if not InputCheck.isValidEmailAddr(self.email):
                showErrorMsg(Localizer.CreateAccountScreenInvalidEmail)
            else:
                if self.email != self.emailConfirmEntry.get():
                    showErrorMsg(Localizer.CreateAccountScreenEmailMismatch)
                else:
                    self.__validatedEmail = 1
                    self.fsm.request('waitForLoginResponse')

    def __handleInvalidEmailAck(self):
        self.dialog.hide()
        self.fsm.request('getEmail')

    def __handleEmailCancel(self):
        messenger.send(self.doneEvent, [{'mode': 'cancel'}])

    def exitGetEmail(self):
        if self.under13 and not self.getEmailUnder13:
            return
        base.transitions.noTransitions()
        self.stopFocusMgmt()
        self.emailPanel.hide()

    def __handleFocusChange(self, focusItem):
        for item in self.focusList:
            item.label.component('text0').setFg(self.labelFg)

        if focusItem is not None:
            focusItem.label.component('text0').setFg(self.labelFgActive)
        if focusItem is not None:
            msgs = [
             Localizer.CreateAccountScreenInstructionsUsername, Localizer.CreateAccountScreenInstructionsPassword, Localizer.CreateAccountScreenInstructionsConfirmPassword, Localizer.CreateAccountScreenInstructionsDob]
            index = self.getFocusIndex()
            self.instructionsLabel['text'] = msgs[index]
        return

    def __handleDob(self, value):
        self.setFocus(self.dobEntry)

    def __handleDobEnterPress(self):
        self.removeFocus()
        self.playFocusChangeSound()
        self.__handleSubmit()

    def __handleSubmit(self):
        self.removeFocus()
        self.userName = self.nameEntry.get()
        self.password = self.passwordEntry.get()
        passwordConfirm = self.passwordConfirmEntry.get()
        self.dobMonth = self.dobEntry.getMonth()
        self.dobYear = self.dobEntry.getYear()
        self.dobDay = self.dobEntry.getDay()
        minNameLength = self.tcr.accountServerConstants.getInt('minNameLength')
        minPwdLength = self.tcr.accountServerConstants.getInt('minPwLength')
        if self.userName == '':
            self.dialog.setMessage(Localizer.CreateAccountScreenNoAccountName)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleUsernameAck)
        else:
            if len(self.userName) < minNameLength:
                self.dialog.setMessage(Localizer.CreateAccountScreenAccountNameTooShort % minNameLength)
                self.dialog.show()
                self.acceptOnce(self.dialogDoneEvent, self.__handleUsernameAck)
            else:
                if len(self.password) < minPwdLength:
                    self.dialog.setMessage(Localizer.CreateAccountScreenPasswordTooShort % minPwdLength)
                    self.dialog.show()
                    self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
                else:
                    if self.password != passwordConfirm:
                        self.dialog.setMessage(Localizer.CreateAccountScreenPasswordMismatch)
                        self.dialog.show()
                        self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
                    else:
                        years = toonbase.tcr.dateObject.getAge(self.dobMonth, self.dobYear, self.dobDay)
                        if years < 0:
                            self.dialog.setMessage(Localizer.CreateAccountScreenInvalidDob)
                            self.dialog.show()
                            self.acceptOnce(self.dialogDoneEvent, self.__handleDobAck)
                        else:
                            self.notify.debug('Age: %s years' % years)
                            self.age = years
                            self.fsm.request('getEmail')

    def __handleCancel(self):
        messenger.send(self.doneEvent, [{'mode': 'cancel'}])

    def __handleUsernameAck(self):
        self.dialog.hide()
        self.fsm.request('create')
        self.setFocus(self.nameEntry)

    def __handlePasswordAck(self):
        self.dialog.hide()
        self.fsm.request('create')
        self.setFocus(self.passwordEntry)

    def __handleDobAck(self):
        self.dialog.hide()
        self.fsm.request('create')
        self.removeFocus()

    def enterWaitForLoginResponse(self):
        self.tcr.handler = self.handleWaitForLoginResponse
        self.tcr.userName = self.userName
        self.tcr.password = self.password
        try:
            data = {'dobYear': self.dobYear, 'dobMonth': self.dobMonth, 'dobDay': self.dobDay, 'email': self.email}
            if launcher:
                referrer = launcher.getReferrerCode()
                if referrer is not None:
                    data['referrer'] = referrer
            error = self.loginInterface.createAccount(self.userName, self.password, data)
        except TTAccount.TTAccountException, e:
            error = str(e)
            self.notify.info(error)
            self.dialog.setMessage(error + Localizer.CreateAccountScreenConnectionErrorSuffix)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleConnectionErrorAck)
            return
        else:
            if error:
                self.notify.info(error)
                self.dialog.setMessage(error)
                self.dialog.show()
                self.acceptOnce(self.dialogDoneEvent, self.__handleBadAccountAck)
            self.tcr.logAccountInfo()
            self.loginInterface.sendLoginMsg()
            self.waitForDatabaseTimeout()

        return

    def exitWaitForLoginResponse(self):
        self.cleanupWaitingForDatabase()
        self.tcr.handler = None
        return

    def handleWaitForLoginResponse(self, msgType, di):
        if msgType == CLIENT_LOGIN_2_RESP:
            self.handleLoginResponseMsg2(di)
        else:
            if msgType == CLIENT_LOGIN_RESP:
                self.handleLoginResponseMsg(di)
            else:
                if msgType == CLIENT_SERVER_UP:
                    self.tcr.handleServerUp(di)
                else:
                    if msgType == CLIENT_SERVER_DOWN:
                        self.tcr.handleServerDown(di)
                    else:
                        self.tcr.handleUnexpectedMsgType(msgType, di)

    def handleLoginResponseMsg2(self, di):
        returnCode = di.getUint8()
        self.notify.info('Login response return code: ' + str(returnCode))
        if returnCode == 0:
            self.__handleLoginSuccess()
        else:
            errorString = di.getString()
            self.notify.warning(errorString)
            messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def __handleLoginSuccess(self):
        self.notify.info('Logged in with username: %s' % self.userName)
        if launcher:
            launcher.setGoUserName(self.userName)
            launcher.setLastLogin(self.userName)
            launcher.setUserLoggedIn()
        messenger.send(self.doneEvent, [{'mode': 'success'}])

    def handleLoginResponseMsg(self, di):
        returnCode = di.getUint8()
        self.notify.info('Login response return code: ' + str(returnCode))
        if returnCode == 0:
            accountCode = di.getUint32()
            commentString = di.getString()
            sec = di.getUint32()
            usec = di.getUint32()
            self.__handleLoginSuccess()
        else:
            if returnCode == 12:
                self.notify.info('Bad password')
                self.dialog.setMessage(Localizer.CreateAccountScreenUserNameTaken)
                self.dialog.show()
                self.acceptOnce(self.dialogDoneEvent, self.__handleBadPasswordAck)
            else:
                if returnCode == 14:
                    self.notify.info('Bad word in user name')
                    self.dialog.setMessage(Localizer.CreateAccountScreenInvalidUserName)
                    self.dialog.show()
                    self.acceptOnce(self.dialogDoneEvent, self.__handleBadWordInUserName)
                else:
                    if returnCode == 129:
                        self.notify.info('Username not found')
                        self.dialog.setMessage(Localizer.CreateAccountScreenUserNameNotFound)
                        self.dialog.show()
                        self.acceptOnce(self.dialogDoneEvent, self.__handleBadAccountAck)
                    else:
                        accountCode = di.getUint32()
                        errorString = di.getString()
                        self.notify.warning(errorString)
                        messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def __handleConnectionErrorAck(self):
        self.dialog.hide()
        messenger.send(self.doneEvent, [{'mode': 'failure'}])

    def __handleBadPasswordAck(self):
        self.dialog.hide()
        self.fsm.request('create')

    def __handleBadAccountAck(self):
        self.dialog.hide()
        self.fsm.request('create')

    def __handleBadWordInUserName(self):
        self.userName = ''
        self.nameEntry.set('')
        self.dialog.hide()
        self.fsm.request('create')