from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
from TaskManagerGlobal import *
import OnscreenText, StateData, ToontownDialog, FSM, State, DirectNotifyGlobal, Task, Localizer, TTAccount, GuiScreen, time

class LoginScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    AutoLoginName = base.config.GetString('auto-login', '')
    AutoLoginPassword = base.config.GetString('auto-password', '')
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginScreen')
    ActiveEntryColor = Vec4(1, 1, 1, 1)
    InactiveEntryColor = Vec4(0.8, 0.8, 0.8, 1)
    hideForgotPassword = 0

    def __init__(self, tcr, doneEvent):
        self.notify.debug('__init__')
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.loginInterface = self.tcr.loginInterface
        self.allowNewAccounts = tcr.accountServerConstants.getBool('allowNewAccounts')
        self.userName = ''
        self.password = ''
        self.fsm = FSM.FSM('LoginScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'login', 'waitForLoginResponse']),
         State.State('login', self.enterLogin, self.exitLogin, [
          'waitForLoginResponse', 'login', 'showLoginFailDialog']),
         State.State('showLoginFailDialog', self.enterShowLoginFailDialog, self.exitShowLoginFailDialog, [
          'login', 'showLoginFailDialog']),
         State.State('waitForLoginResponse', self.enterWaitForLoginResponse, self.exitWaitForLoginResponse, [
          'login', 'showLoginFailDialog', 'showConnectionProblemDialog']),
         State.State('showConnectionProblemDialog', self.enterShowConnectionProblemDialog, self.exitShowConnectionProblemDialog, [
          'login'])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        self.notify.debug('load')
        masterScale = 0.8
        textScale = 0.1 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 1.15 * masterScale
        buttonLineHeight = 0.14 * masterScale
        background = loader.loadModel('phase_3/models/gui/login-background')
        nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.frame = DirectFrame(parent=aspect2d, image=background.find('**/first_time_install'), image_scale=(1, 1, 1), relief=None, sortOrder=20)
        self.frame.hide()
        linePos = -0.26
        self.nameLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.LoginScreenUserName, text_scale=textScale, text_align=TextNode.ARight)
        self.nameEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.125, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1)
        linePos -= lineHeight
        self.passwordLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.21, 0, linePos), text=Localizer.LoginScreenPassword, text_scale=textScale, text_align=TextNode.ARight)
        self.passwordEntry = DirectEntry(parent=self.frame, relief=None, image=nameBalloon, image1_color=self.InactiveEntryColor, scale=entryScale, pos=(-0.125, 0.0, linePos), width=maxLoginWidth, numLines=1, focus=0, cursorKeys=1, obscured=1, command=self.__handleLoginPassword)
        linePos -= lineHeight
        buttonImageScale = (
         1.7, 1.1, 1.1)
        self.loginButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.LoginScreenLogin, text_scale=0.06, text_pos=(0, -0.02), image_scale=buttonImageScale, command=self.__handleLoginButton)
        linePos -= buttonLineHeight
        if self.allowNewAccounts:
            image_color = Vec4(1, 1, 1, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        else:
            g = 0.5
            image_color = Vec4(g, g, g, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_UP'))
        self.createAccountButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=imageSet, image_color=image_color, text=Localizer.LoginScreenCreateAccount, text_scale=0.06, text_pos=(0, -0.02), image_scale=buttonImageScale, command=self.__handleCreateAccount)
        linePos -= buttonLineHeight
        self.forgotPasswordButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.LoginScreenForgotPassword, text_scale=0.06, text_pos=(0, -0.02), image_scale=buttonImageScale, command=self.__handleForgotPassword)
        if self.hideForgotPassword:
            self.forgotPasswordButton.hide()
        linePos -= buttonLineHeight
        self.quitButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.LoginScreenQuit, text_scale=0.06, text_pos=(0, -0.02), image_scale=buttonImageScale, command=self.__handleQuit)
        linePos -= buttonLineHeight
        self.dialogDoneEvent = 'loginDialogAck'
        self.dialog = ToontownDialog.GlobalDialog(dialogName='loginDialog', doneEvent=self.dialogDoneEvent, message='', style=ToontownDialog.Acknowledge, sortOrder=NO_FADE_SORT_INDEX + 100)
        self.dialog.hide()
        self.failDialog = DirectFrame(relief=None, pos=(0, 0.1, 0), image=getDefaultDialogGeom(), image_color=GlobalDialogColor, image_scale=(1.3, 1.0, 0.9), text='', text_scale=0.08, text_pos=(0.0, 0.3), text_wordwrap=15, sortOrder=NO_FADE_SORT_INDEX)
        linePos = -0.05
        self.failTryAgainButton = DirectButton(parent=self.failDialog, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=buttonImageScale, text=Localizer.LoginScreenTryAgain, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleFailTryAgain)
        linePos -= buttonLineHeight
        self.failForgotPasswordButton = DirectButton(parent=self.failDialog, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=buttonImageScale, text=Localizer.LoginScreenForgotPassword, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleFailForgotPassword)
        if self.hideForgotPassword:
            self.failForgotPasswordButton.hide()
        linePos -= buttonLineHeight
        if self.allowNewAccounts:
            image_color = Vec4(1, 1, 1, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        else:
            g = 0.5
            image_color = Vec4(g, g, g, 1)
            imageSet = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_UP'))
        self.failCreateAccountButton = DirectButton(parent=self.failDialog, relief=None, pos=(0, 0, linePos), scale=0.9, image=imageSet, image_color=image_color, image_scale=buttonImageScale, text=Localizer.LoginScreenCreateAccount, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleFailCreateAccount)
        linePos -= buttonLineHeight
        self.failDialog.hide()
        self.connectionProblemDialogDoneEvent = 'loginConnectionProblemDlgAck'
        self.connectionProblemDialog = ToontownDialog.GlobalDialog(dialogName='connectionProblemDialog', doneEvent=self.connectionProblemDialogDoneEvent, message='', style=ToontownDialog.Acknowledge, sortOrder=NO_FADE_SORT_INDEX + 100)
        self.connectionProblemDialog.hide()
        background.removeNode()
        guiButton.removeNode()
        nameBalloon.removeNode()
        return

    def unload(self):
        self.notify.debug('unload')
        self.dialog.cleanup()
        del self.dialog
        self.failDialog.destroy()
        del self.failDialog
        self.connectionProblemDialog.cleanup()
        del self.connectionProblemDialog
        self.frame.destroy()
        del self.fsm
        del self.loginInterface
        del self.tcr

    def enter(self):
        if self.tcr.blue:
            self.userName = 'blue'
            self.password = self.tcr.blue
            self.fsm.request('waitForLoginResponse')
        else:
            if self.tcr.playToken:
                self.userName = '*'
                self.password = self.tcr.playToken
                self.fsm.request('waitForLoginResponse')
            else:
                if self.AutoLoginName:
                    self.userName = self.AutoLoginName
                    self.password = self.AutoLoginPassword
                    self.fsm.request('waitForLoginResponse')
                else:
                    self.fsm.request('login')

    def exit(self):
        self.frame.hide()
        self.ignore(self.dialogDoneEvent)
        self.fsm.requestFinalState()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterLogin(self):
        toonbase.tcr.resetPeriodTimer(None)
        self.userName = ''
        self.password = ''
        if launcher:
            self.userName = launcher.getLastLogin()
        if self.userName and self.nameEntry.get():
            if self.userName != self.nameEntry.get():
                self.userName = ''
        self.frame.show()
        self.nameEntry.enterText(self.userName)
        self.passwordEntry.enterText(self.password)
        self.focusList = [
         self.nameEntry, self.passwordEntry]
        focusIndex = 0
        if self.userName:
            focusIndex = 1
        self.startFocusMgmt(startFocus=focusIndex)
        return

    def exitLogin(self):
        self.stopFocusMgmt()

    def enterShowLoginFailDialog(self, msg):
        base.transitions.fadeScreen(0.5)
        self.failDialog['text'] = msg
        self.failDialog.show()

    def __handleFailTryAgain(self):
        self.fsm.request('login')

    def __handleFailForgotPassword(self):
        messenger.send(self.doneEvent, [{'mode': 'forgotPassword'}])

    def __handleFailCreateAccount(self):
        if self.allowNewAccounts:
            messenger.send(self.doneEvent, [{'mode': 'createAccount'}])
            return
        self.dialog.setMessage(Localizer.LoginScreenNoNewAccounts)
        self.dialog.show()
        self.acceptOnce(self.dialogDoneEvent, self.__handleFailNoNewAccountsAck)
        self.failDialog.hide()

    def __handleFailNoNewAccountsAck(self):
        self.dialog.hide()
        self.fsm.request('showLoginFailDialog', [self.failDialog['text']])

    def exitShowLoginFailDialog(self):
        base.transitions.noTransitions()
        self.failDialog.hide()

    def __handleLoginPassword(self, password):
        if password != '':
            if self.nameEntry.get() != '':
                self.__handleLoginButton()

    def __handleLoginButton(self):
        self.removeFocus()
        self.userName = self.nameEntry.get()
        self.password = self.passwordEntry.get()
        if self.userName == '':
            self.dialog.setMessage(Localizer.LoginScreenLoginPrompt)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleEnterLoginAck)
        else:
            self.fsm.request('waitForLoginResponse')

    def __handleQuit(self):
        self.removeFocus()
        messenger.send(self.doneEvent, [{'mode': 'quit'}])

    def __handleCreateAccount(self):
        self.removeFocus()
        if self.allowNewAccounts:
            messenger.send(self.doneEvent, [{'mode': 'createAccount'}])
            return
        self.dialog.setMessage(Localizer.LoginScreenNoNewAccounts)
        self.dialog.show()
        self.acceptOnce(self.dialogDoneEvent, self.__handleNoNewAccountsAck)

    def __handleForgotPassword(self):
        self.removeFocus()
        messenger.send(self.doneEvent, [{'mode': 'forgotPassword'}])

    def enterWaitForLoginResponse(self):
        self.tcr.handler = self.handleWaitForLoginResponse
        self.tcr.userName = self.userName
        self.tcr.password = self.password
        try:
            error = self.loginInterface.authorize(self.userName, self.password)
        except TTAccount.TTAccountException, e:
            self.fsm.request('showConnectionProblemDialog', [str(e)])
            return
        else:
            if error:
                self.notify.info(error)
                freeTimeExpired = self.loginInterface.getErrorCode() == 10
                if freeTimeExpired:
                    self.tcr.logAccountInfo()
                    messenger.send(self.doneEvent, [{'mode': 'freeTimeExpired'}])
                else:
                    self.fsm.request('showLoginFailDialog', [error])
            self.loginInterface.sendLoginMsg()
            self.waitForDatabaseTimeout()

    def exitWaitForLoginResponse(self):
        self.cleanupWaitingForDatabase()
        self.tcr.handler = None
        return

    def enterShowConnectionProblemDialog(self, msg):
        self.connectionProblemDialog.setMessage(msg)
        self.connectionProblemDialog.show()
        self.acceptOnce(self.connectionProblemDialogDoneEvent, self.__handleConnectionProblemAck)

    def __handleConnectionProblemAck(self):
        self.connectionProblemDialog.hide()
        self.fsm.request('login')

    def exitShowConnectionProblemDialog(self):
        pass

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
        now = time.time()
        returnCode = di.getUint8()
        errorString = di.getString()
        self.userName = di.getString()
        toonbase.tcr.userName = self.userName
        toonbase.tcr.secretChatAllowed = di.getUint8()
        sec = di.getUint32()
        usec = di.getUint32()
        serverTime = sec + usec / 1000000.0
        serverDelta = serverTime - now
        toonbase.tcr.setServerDelta(serverDelta)
        self.notify.setServerDelta(serverDelta, 28800)
        self.isPaid = di.getUint8()
        toonbase.tcr.setIsPaid(self.isPaid)
        if launcher and self.isPaid:
            launcher.setPaidUserLoggedIn()
        self.notify.info('Paid from game server login: %s' % self.isPaid)
        if di.getRemainingSize() >= 4:
            minutesRemaining = di.getInt32()
            self.notify.info('Minutes remaining from server %s' % minutesRemaining)
            if minutesRemaining >= 0:
                toonbase.tcr.resetPeriodTimer(minutesRemaining * 60)
        self.notify.info('Login response return code %s' % returnCode)
        if returnCode == 0:
            self.__handleLoginSuccess()
        else:
            if returnCode == -13:
                self.notify.info('Period Time Expired')
                self.fsm.request('showLoginFailDialog', [
                 Localizer.LoginScreenPeriodTimeExpired])
            else:
                self.notify.info('Login failed: %s' % errorString)
                messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def handleLoginResponseMsg(self, di):
        now = time.time()
        returnCode = di.getUint8()
        accountCode = di.getUint32()
        errorString = di.getString()
        sec = di.getUint32()
        usec = di.getUint32()
        serverTime = sec + usec / 1000000.0
        serverDelta = serverTime - now
        toonbase.tcr.setServerDelta(serverDelta)
        self.notify.setServerDelta(serverDelta, 28800)
        self.notify.info('Login response return code %s' % returnCode)
        if returnCode == 0:
            self.__handleLoginSuccess()
        else:
            if returnCode == 12:
                self.notify.info('Bad password')
                self.fsm.request('showLoginFailDialog', [
                 Localizer.LoginScreenBadPassword])
            else:
                if returnCode == 14:
                    self.notify.info('Bad word in user name')
                    self.fsm.request('showLoginFailDialog', [
                     Localizer.LoginScreenInvalidUserName])
                else:
                    if returnCode == 129:
                        self.notify.info('Username not found')
                        self.fsm.request('showLoginFailDialog', [
                         Localizer.LoginScreenUserNameNotFound])
                    else:
                        self.notify.info('Login failed: %s' % errorString)
                        messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def __handleLoginSuccess(self):
        self.tcr.logAccountInfo()
        if launcher:
            launcher.setGoUserName(self.userName)
            launcher.setLastLogin(self.userName)
            launcher.setUserLoggedIn()
            if self.loginInterface.freeTimeExpires == -1:
                launcher.setPaidUserLoggedIn()
        if self.loginInterface.needToSetParentPassword():
            messenger.send(self.doneEvent, [{'mode': 'getChatPassword'}])
        else:
            messenger.send(self.doneEvent, [{'mode': 'success'}])

    def __handleEnterLoginAck(self):
        self.dialog.hide()
        self.fsm.request('login')

    def __handleNoNewAccountsAck(self):
        self.dialog.hide()
        self.fsm.request('login')