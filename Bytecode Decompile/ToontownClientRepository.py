from ShowBaseGlobal import *
from ToonBaseGlobal import *
from ToontownMsgTypes import *
from DownloadForceAcknowledge import *
from ClockDelta import *
from ToontownGlobals import *
from DCSubatomicType import *
from DirectGui import *
from IntervalGlobal import ivalMgr
import sys, AvatarDNA, DirectNotifyGlobal, ClientRepository, PotentialAvatar, PotentialShard, FSM, State, LocalToon, TTAccount, AccountServerConstants, AccountServerDate, NewPlayerScreen, CreateAccountScreen, LoginScreen, FreeTimeInformScreen, MemberAgreementScreen, BillingScreen, ParentPasswordScreen, WelcomeScreen, ForgotPasswordScreen, AvatarChooser, Avatar, MakeAToon, HoodMgr, PlayGame, FriendHandle, Task, ToontownDialog, FriendSecret, FriendsListPanel, types, DistributedAvatar, DistributedSmoothNode, time, Localizer, LoginGSAccount, LoginGoAccount, LoginWebPlayTokenAccount, LoginTTAccount, DateObject, HTTPUtil, PythonUtil

class ToontownClientRepository(ClientRepository.ClientRepository):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownClientRepository')
    avatarLimit = 6
    defaultServerPort = 5150

    def __init__(self, dcFileName, serverVersion, launcher=None):
        ClientRepository.ClientRepository.__init__(self, dcFileName)
        self.launcher = launcher
        self.__currentAvId = 0
        self.productName = config.GetString('product-name', 'DisneyOnline-US')
        self.blue = None
        if self.launcher:
            self.blue = self.launcher.getBlue()
        fakeBlue = config.GetString('fake-blue', '')
        if fakeBlue:
            self.blue = fakeBlue
        self.playToken = None
        if self.launcher:
            self.playToken = self.launcher.getPlayToken()
        fakePlayToken = config.GetString('fake-playtoken', '')
        if fakePlayToken:
            self.playToken = fakePlayToken
        self.requiredLogin = config.GetString('required-login', 'auto')
        if self.requiredLogin == 'auto':
            self.notify.info('required-login auto.')
        else:
            if self.requiredLogin == 'green':
                self.notify.error('The green code is out of date')
            else:
                if self.requiredLogin == 'blue':
                    if not self.blue:
                        self.notify.error('The tcr does not have the required blue login')
                else:
                    if self.requiredLogin == 'playToken':
                        if not self.playToken:
                            self.notify.error('The tcr does not have the required playToken login')
                    else:
                        if self.requiredLogin == 'gameServer':
                            self.notify.info('Using game server name/password.')
                        else:
                            self.notify.error('The required-login was not recognized.')
        if self.launcher and hasattr(self.launcher, 'http'):
            self.http = self.launcher.http
        else:
            self.http = HTTPClient()
        if self.http.getVerifySsl() != HTTPClient.VSNoVerify:
            self.http.setVerifySsl(HTTPClient.VSNoDateCheck)
        self.accountOldAuth = config.GetBool('account-old-auth', 0)
        if self.accountOldAuth:
            self.loginInterface = LoginGSAccount.LoginGSAccount(self)
            self.notify.info('loginInterface: LoginGSAccount')
        else:
            if self.blue:
                self.loginInterface = LoginGoAccount.LoginGoAccount(self)
                self.notify.info('loginInterface: LoginGoAccount')
            else:
                if self.playToken:
                    self.loginInterface = LoginWebPlayTokenAccount.LoginWebPlayTokenAccount(self)
                    self.notify.info('loginInterface: LoginWebPlayTokenAccount')
                else:
                    self.loginInterface = LoginTTAccount.LoginTTAccount(self)
                    self.notify.info('loginInterface: LoginTTAccount')
        self.secretChatAllowed = base.config.GetBool('allow-secret-chat', 0)
        self.freeTimeExpiresAt = -1
        self.__isPaid = 0
        self.periodTimerExpired = 0
        self.periodTimerStarted = None
        self.periodTimerSecondsRemaining = None
        self.heartbeatInterval = config.GetDouble('heartbeat-interval', 10)
        self.heartbeatStarted = 0
        self.lastHeartbeat = 0
        self.__forbidCheesyEffects = 0
        base.launcher = launcher
        self.token2nodePath = {}
        self.token2nodePath[SPRender] = base.render
        self.token2nodePath[SPHidden] = base.hidden
        self.friendManager = None
        self.timeManager = None
        self.trophyManager = None
        self.bankManager = None
        self.mailboxManager = None
        self.friendsMap = {}
        self.friendsOnline = {}
        self.friendsMapPending = 0
        self.friendsListError = 0
        self.elderFriendsMap = {}
        self.__queryAvatarMap = {}
        self.__shards = {}
        self.serverVersion = serverVersion
        self.waitingForDatabase = None
        self.dateObject = DateObject.DateObject()
        self.accountServerDate = AccountServerDate.AccountServerDate()
        self.loginFSM = FSM.FSM('ClientRepositoryLogin', [
         State.State('loginOff', self.enterLoginOff, self.exitLoginOff, [
          'connect']),
         State.State('connect', self.enterConnect, self.exitConnect, [
          'login', 'newPlayer', 'failedToConnect', 'failedToGetServerConstants', 'failedToGetServerDate']),
         State.State('newPlayer', self.enterNewPlayer, self.exitNewPlayer, [
          'noConnection', 'login', 'createAccount', 'shutdown']),
         State.State('login', self.enterLogin, self.exitLogin, [
          'noConnection', 'freeTimeInform', 'createAccount', 'forgotPassword', 'reject', 'failedToConnect', 'shutdown', 'billing', 'parentPassword', 'memberAgreement']),
         State.State('createAccount', self.enterCreateAccount, self.exitCreateAccount, [
          'noConnection', 'freeTimeInform', 'newPlayer', 'login', 'reject', 'failedToConnect', 'failedToGetServerDate', 'shutdown', 'billing', 'memberAgreement']),
         State.State('forgotPassword', self.enterForgotPassword, self.exitForgotPassword, [
          'noConnection', 'login']),
         State.State('freeTimeInform', self.enterFreeTimeInform, self.exitFreeTimeInform, [
          'noConnection', 'memberAgreement', 'billing', 'waitForShardList', 'shutdown']),
         State.State('memberAgreement', self.enterMemberAgreement, self.exitMemberAgreement, [
          'noConnection', 'failedToGetServerDate', 'login', 'billing', 'freeTimeInform', 'waitForShardList', 'shutdown', 'createAvatar', 'createAccount']),
         State.State('billing', self.enterBilling, self.exitBilling, [
          'noConnection', 'welcome', 'login', 'waitForShardList', 'reject', 'failedToConnect', 'failedToGetServerDate', 'shutdown', 'freeTimeInform', 'createAvatar', 'parentPassword']),
         State.State('parentPassword', self.enterParentPassword, self.exitParentPassword, [
          'noConnection', 'welcome', 'login', 'waitForShardList', 'reject', 'failedToConnect', 'failedToGetServerDate', 'shutdown', 'freeTimeInform', 'createAvatar']),
         State.State('welcome', self.enterWelcome, self.exitWelcome, [
          'noConnection', 'login', 'waitForShardList', 'reject', 'failedToConnect', 'shutdown', 'freeTimeInform', 'createAvatar']),
         State.State('failedToConnect', self.enterFailedToConnect, self.exitFailedToConnect, [
          'connect', 'shutdown']),
         State.State('failedToGetServerConstants', self.enterFailedToGetServerConstants, self.exitFailedToGetServerConstants, [
          'connect', 'shutdown']),
         State.State('failedToGetServerDate', self.enterFailedToGetServerDate, self.exitFailedToGetServerDate),
         State.State('shutdown', self.enterShutdown, self.exitShutdown, [
          'loginOff']),
         State.State('waitForShardList', self.enterWaitForShardList, self.exitWaitForShardList, [
          'noConnection', 'waitForAvatarList', 'noShards']),
         State.State('noShards', self.enterNoShards, self.exitNoShards, [
          'noConnection', 'waitForShardList', 'shutdown']),
         State.State('reject', self.enterReject, self.exitReject, [
          'shutdown']),
         State.State('noConnection', self.enterNoConnection, self.exitNoConnection, [
          'login', 'connect', 'shutdown']),
         State.State('afkTimeout', self.enterAfkTimeout, self.exitAfkTimeout, [
          'waitForAvatarList', 'shutdown']),
         State.State('periodTimeout', self.enterPeriodTimeout, self.exitPeriodTimeout, [
          'waitForAvatarList', 'shutdown']),
         State.State('waitForAvatarList', self.enterWaitForAvatarList, self.exitWaitForAvatarList, [
          'noConnection', 'chooseAvatar', 'createAvatar', 'shutdown']),
         State.State('chooseAvatar', self.enterChooseAvatar, self.exitChooseAvatar, [
          'noConnection', 'createAvatar', 'waitForSetAvatarResponse', 'waitForAvatarList', 'waitForDeleteAvatarResponse', 'shutdown', 'login']),
         State.State('createAvatar', self.enterCreateAvatar, self.exitCreateAvatar, [
          'noConnection', 'chooseAvatar', 'waitForSetAvatarResponse', 'memberAgreement']),
         State.State('waitForDeleteAvatarResponse', self.enterWaitForDeleteAvatarResponse, self.exitWaitForDeleteAvatarResponse, [
          'noConnection', 'chooseAvatar', 'createAvatar']),
         State.State('waitForSetAvatarResponse', self.enterWaitForSetAvatarResponse, self.exitWaitForSetAvatarResponse, [
          'noConnection', 'chooseAvatar', 'waitForAvatarList', 'login', 'memberAgreement', 'shutdown', 'afkTimeout', 'periodTimeout'])], 'loginOff', 'loginOff')
        self.gameFSM = FSM.FSM('ClientRepository', [
         State.State('gameOff', self.enterGameOff, self.exitGameOff, [
          'waitOnEnterResponses']),
         State.State('waitOnEnterResponses', self.enterWaitOnEnterResponses, self.exitWaitOnEnterResponses, [
          'playGame', 'waitForTimeManager', 'gameOff']),
         State.State('waitForTimeManager', self.enterWaitForTimeManager, self.exitWaitForTimeManager, [
          'playGame', 'tutorialQuestion', 'gameOff']),
         State.State('tutorialQuestion', self.enterTutorialQuestion, self.exitTutorialQuestion, [
          'playGame', 'gameOff']),
         State.State('playGame', self.enterPlayGame, self.exitPlayGame, [
          'gameOff', 'waitOnEnterResponses'])], 'gameOff', 'gameOff')
        self.loginFSM.getStateNamed('waitForSetAvatarResponse').addChild(self.gameFSM)
        self.loginFSM.enterInitialState()
        self.loginScreen = None
        self.music = None
        self.hoodMgr = HoodMgr.HoodMgr(self)
        self.gameDoneEvent = 'playGameDone'
        self.playGame = PlayGame.PlayGame(self.gameFSM, self.gameDoneEvent)
        return

    def getServerVersion(self):
        return self.serverVersion

    def enterLoginOff(self):
        self.handler = self.handleLoginOff

    def exitLoginOff(self):
        self.handler = None
        return

    def handleLoginOff(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def enterConnect(self, serverList):
        self.serverList = serverList
        self.connectingBox = ToontownDialog.GlobalDialog(message=Localizer.TCRConnecting)
        self.connectingBox.show()
        self.renderFrame()
        self.handler = self.handleConnect
        self.connect(self.serverList, 1, successCallback=self.gotoFirstScreen, failureCallback=self.failedToConnect)

    def failedToConnect(self, usedProxy, statusCode):
        if usedProxy:
            self.notify.info('Got %s from proxy, trying to connect again without proxy.' % statusCode)
            self.connect(self.serverList, 0, successCallback=self.gotoFirstScreen, failureCallback=self.failedToConnectAgain, failureArgs=[statusCode])
        else:
            self.loginFSM.request('failedToConnect', [statusCode])

    def failedToConnectAgain(self, usedProxy, statusCode, origStatusCode):
        self.notify.info('Unable to connect without proxy either (status = %s)' % statusCode)
        self.loginFSM.request('failedToConnect', [origStatusCode])

    def exitConnect(self):
        self.connectingBox.cleanup()
        del self.connectingBox

    def handleConnect(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def gotoFirstScreen(self):
        try:
            self.accountServerConstants = AccountServerConstants.AccountServerConstants()
        except TTAccount.TTAccountException, e:
            self.notify.debug(str(e))
            self.loginFSM.request('failedToGetServerConstants', [e])
            return
        else:
            self.startReaderPollTask()
            self.startHeartbeat()
            newInstall = 0
            if launcher:
                newInstall = launcher.getIsNewInstallation()
            newInstall = base.config.GetBool('new-installation', newInstall)
            if self.isWebPlayToken():
                firstScreen = 'login'
            else:
                if newInstall:
                    firstScreen = 'newPlayer'
                firstScreen = 'login'

        firstScreen = base.config.GetString('override-first-screen', firstScreen)
        self.loginFSM.request(firstScreen)

    def enterNewPlayer(self):
        self.newPlayerDoneEvent = 'newPlayerDone'
        self.newPlayerScreen = NewPlayerScreen.NewPlayerScreen(self, self.newPlayerDoneEvent)
        self.accept(self.newPlayerDoneEvent, self.__handleNewPlayerDone)
        self.newPlayerScreen.load()
        self.newPlayerScreen.enter()

    def __handleNewPlayerDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'newAccount':
            self.loginFSM.request('createAccount', [{'back': 'newPlayer', 'backArgs': []}])
        else:
            if mode == 'login':
                self.loginFSM.request('login')
            else:
                if mode == 'quit':
                    self.loginFSM.request('shutdown')
                else:
                    self.notify.error('Invalid doneStatus mode from newPlayerScreen: ' + str(mode))

    def exitNewPlayer(self):
        if self.newPlayerScreen:
            self.newPlayerScreen.exit()
            self.newPlayerScreen.unload()
            self.newPlayerScreen = None
            self.renderFrame()
        self.ignore(self.newPlayerDoneEvent)
        del self.newPlayerDoneEvent
        self.handler = None
        return

    def enterLogin(self):
        self.sendSetAvatarIdMsg(0)
        self.loginDoneEvent = 'loginDone'
        self.loginScreen = LoginScreen.LoginScreen(self, self.loginDoneEvent)
        self.accept(self.loginDoneEvent, self.__handleLoginDone)
        self.loginScreen.load()
        self.loginScreen.enter()

    def __handleLoginDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'success':
            self.setIsNotNewInstallation()
            self.loginFSM.request('freeTimeInform')
        else:
            if mode == 'getChatPassword':
                self.loginFSM.request('parentPassword')
            else:
                if mode == 'freeTimeExpired':
                    self.loginFSM.request('freeTimeInform')
                else:
                    if mode == 'createAccount':
                        if self.getCreditCardUpFront():
                            self.loginFSM.request('memberAgreement', [{'forward': 'waitForShardList', 'forwardArgs': [], 'back': 'login', 'backArgs': []}])
                        else:
                            self.loginFSM.request('createAccount', [{'back': 'login', 'backArgs': []}])
                    else:
                        if mode == 'forgotPassword':
                            self.loginFSM.request('forgotPassword')
                        else:
                            if mode == 'reject':
                                self.loginFSM.request('reject')
                            else:
                                if mode == 'quit':
                                    self.loginFSM.request('shutdown')
                                else:
                                    if mode == 'failure':
                                        self.loginFSM.request('failedToConnect')
                                    else:
                                        self.notify.error('Invalid doneStatus mode from loginScreen: ' + str(mode))

    def exitLogin(self):
        if self.loginScreen:
            self.loginScreen.exit()
            self.loginScreen.unload()
            self.loginScreen = None
            self.renderFrame()
        self.ignore(self.loginDoneEvent)
        del self.loginDoneEvent
        self.handler = None
        return

    def enterCreateAccount(self, createAccountDoneData={'back': 'login', 'backArgs': []}):
        self.createAccountDoneData = createAccountDoneData
        self.createAccountDoneEvent = 'createAccountDone'
        self.createAccountScreen = None
        if self.refreshAccountServerDate():
            self.loginFSM.request('failedToGetServerDate', [{'retry': 'createAccount', 'retryArgs': [], 'cancel': 'login', 'cancelArgs': []}])
            return
        self.createAccountScreen = CreateAccountScreen.CreateAccountScreen(self, self.createAccountDoneEvent)
        self.accept(self.createAccountDoneEvent, self.__handleCreateAccountDone)
        self.createAccountScreen.load()
        self.createAccountScreen.enter()
        return

    def __handleCreateAccountDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'success':
            self.setIsNotNewInstallation()
            if self.getCreditCardUpFront():
                self.loginFSM.request('billing', [{'forward': 'waitForShardList', 'forwardArgs': [], 'back': 'login', 'backArgs': []}])
            else:
                self.loginFSM.request('freeTimeInform')
        else:
            if mode == 'reject':
                self.loginFSM.request('reject')
            else:
                if mode == 'cancel':
                    self.loginFSM.request(self.createAccountDoneData['back'], self.createAccountDoneData['backArgs'])
                else:
                    if mode == 'failure':
                        self.loginFSM.request(self.createAccountDoneData['back'], self.createAccountDoneData['backArgs'])
                    else:
                        if mode == 'quit':
                            self.loginFSM.request('shutdown')
                        else:
                            self.notify.error('Invalid doneStatus mode from CreateAccountScreen: ' + str(mode))

    def exitCreateAccount(self):
        if self.createAccountScreen:
            self.createAccountScreen.exit()
            self.createAccountScreen.unload()
            self.createAccountScreen = None
            self.renderFrame()
        self.ignore(self.createAccountDoneEvent)
        del self.createAccountDoneEvent
        self.handler = None
        return

    def enterForgotPassword(self):
        self.forgotPasswordDoneEvent = 'forgotPasswordDone'
        self.accept(self.forgotPasswordDoneEvent, self.__handleForgotPasswordDone)
        self.forgotPasswordScreen = ForgotPasswordScreen.ForgotPasswordScreen(self, self.forgotPasswordDoneEvent)
        self.forgotPasswordScreen.load()
        self.forgotPasswordScreen.enter()

    def __handleForgotPasswordDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'success':
            self.loginFSM.request('login')
        else:
            if mode == 'cancel':
                self.loginFSM.request('login')
            else:
                if mode == 'fail':
                    self.loginFSM.request('login')
                else:
                    self.notify.error('Invalid doneStatus mode from ForgotPasswordScreen: ' + str(mode))

    def exitForgotPassword(self):
        if self.forgotPasswordScreen:
            self.forgotPasswordScreen.exit()
            self.forgotPasswordScreen.unload()
            self.forgotPasswordScreen = None
            self.renderFrame()
        self.ignore(self.forgotPasswordDoneEvent)
        del self.forgotPasswordDoneEvent
        self.handler = None
        return

    def enterFreeTimeInform(self):
        self.freeTimeInformScreen = None
        self.freeTimeInformDoneEvent = 'freeTimeInformDone'
        if self.accountOldAuth or self.isPaid() or self.isWebPlayToken():
            self.loginFSM.request('waitForShardList')
            return
        self.freeTimeInformScreen = FreeTimeInformScreen.FreeTimeInformScreen(self, self.freeTimeInformDoneEvent)
        self.accept(self.freeTimeInformDoneEvent, self.__handleFreeTimeInformDone)
        self.freeTimeInformScreen.load()
        self.freeTimeInformScreen.enter()
        self.handler = self.handleFreeTimeInform
        return

    def __handleFreeTimeInformDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'join':
            if self.getCreditCardUpFront():
                self.loginFSM.request('billing', [{'forward': 'waitForShardList', 'forwardArgs': [], 'back': 'freeTimeInform', 'backArgs': []}])
            else:
                self.loginFSM.request('memberAgreement')
        else:
            if mode == 'free':
                self.loginFSM.request('waitForShardList')
            else:
                if mode == 'quit':
                    self.loginFSM.request('shutdown')
                else:
                    self.notify.error('Invalid doneStatus mode from FreeTimeInformScreen: ' + str(mode))

    def exitFreeTimeInform(self):
        if self.freeTimeInformScreen:
            self.freeTimeInformScreen.exit()
            self.freeTimeInformScreen.unload()
            self.freeTimeInformScreen = None
            self.renderFrame()
        self.ignore(self.freeTimeInformDoneEvent)
        self.handler = None
        return

    def handleFreeTimeInform(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def enterMemberAgreement(self, memAgrDoneData={'forward': 'waitForShardList', 'forwardArgs': [], 'back': 'freeTimeInform', 'backArgs': []}):
        self.memAgrDoneData = memAgrDoneData
        self.sendSetAvatarIdMsg(0)
        self.memberAgreementDoneEvent = 'memberAgreementDone'
        self.memberAgreementScreen = None
        if self.refreshAccountServerDate():
            self.loginFSM.request('failedToGetServerDate', [{'retry': 'memberAgreement', 'retryArgs': [self.memAgrDoneData], 'cancel': self.memAgrDoneData['back'], 'cancelArgs': self.memAgrDoneData['backArgs']}])
            return
        self.memberAgreementScreen = MemberAgreementScreen.MemberAgreementScreen(self, self.memberAgreementDoneEvent)
        self.accept(self.memberAgreementDoneEvent, self.__handleMemberAgreementDone)
        self.memberAgreementScreen.load()
        self.memberAgreementScreen.enter()
        self.handler = self.handleMemberAgreement
        return

    def __handleMemberAgreementDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'agree':
            if self.getCreditCardUpFront():
                self.loginFSM.request('createAccount', [{'back': 'login', 'backArgs': []}])
            else:
                self.loginFSM.request('billing', [self.memAgrDoneData])
        else:
            if mode == 'disagree':
                self.loginFSM.request(self.memAgrDoneData['back'], self.memAgrDoneData['backArgs'])
            else:
                if mode == 'cancel':
                    self.loginFSM.request(self.memAgrDoneData['back'], self.memAgrDoneData['backArgs'])
                else:
                    if mode == 'quit':
                        self.loginFSM.request('shutdown')
                    else:
                        self.notify.error('Invalid doneStatus mode from MemberAgreementScreen: ' + str(mode))

    def exitMemberAgreement(self):
        if self.memberAgreementScreen:
            self.memberAgreementScreen.exit()
            self.memberAgreementScreen.unload()
            self.memberAgreementScreen = None
            self.renderFrame()
        self.ignore(self.memberAgreementDoneEvent)
        self.handler = None
        del self.memAgrDoneData
        return

    def handleMemberAgreement(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def enterBilling(self, billingDoneData={'forward': '', 'forwardArgs': [], 'back': '', 'backArgs': []}):
        self.billingDoneData = billingDoneData
        self.billingDoneEvent = 'billingDone'
        self.billingScreen = None
        if self.refreshAccountServerDate():
            self.loginFSM.request('failedToGetServerDate', [{'retry': 'billing', 'retryArgs': [self.billingDoneData], 'cancel': self.billingDoneData['back'], 'cancelArgs': self.billingDoneData['backArgs']}])
            return
        self.billingScreen = BillingScreen.BillingScreen(self, self.billingDoneEvent)
        self.billingScreen.load()
        self.billingScreen.enter()
        self.accept(self.billingDoneEvent, self.__handleBillingDone)
        self.handler = self.handleBilling
        return

    def __handleBillingDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'success':
            self.loginFSM.request('parentPassword', [{'forward': self.billingDoneData['forward'], 'forwardArgs': self.billingDoneData['forwardArgs']}])
        else:
            if mode == 'reject':
                self.loginFSM.request('reject')
            else:
                if mode == 'cancel':
                    self.loginFSM.request(self.billingDoneData['back'], self.billingDoneData['backArgs'])
                else:
                    if mode == 'failure':
                        self.loginFSM.request(self.billingDoneData['back'], self.billingDoneData['backArgs'])
                    else:
                        if mode == 'quit':
                            self.loginFSM.request('shutdown')
                        else:
                            self.notify.error('Invalid doneStatus mode from BillingScreen: ' + str(mode))

    def exitBilling(self):
        if self.billingScreen:
            self.billingScreen.exit()
            self.billingScreen.unload()
            self.billingScreen = None
            self.renderFrame()
        self.ignore(self.billingDoneEvent)
        self.handler = None
        del self.billingDoneData
        return

    def handleBilling(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def enterParentPassword(self, parentPwdDoneData={'forward': 'waitForShardList', 'forwardArgs': []}):
        self.parentPwdDoneData = parentPwdDoneData
        self.parentPasswordDoneEvent = 'parentPasswordDone'
        self.parentPasswordScreen = None
        self.parentPasswordScreen = ParentPasswordScreen.ParentPasswordScreen(self, self.parentPasswordDoneEvent)
        self.parentPasswordScreen.load()
        self.parentPasswordScreen.enter()
        self.accept(self.parentPasswordDoneEvent, self.__handleParentPasswordDone)
        self.handler = self.handleParentPassword
        return

    def __handleParentPasswordDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'success':
            self.loginFSM.request('welcome', [{'forward': self.parentPwdDoneData['forward'], 'forwardArgs': self.parentPwdDoneData['forwardArgs']}])
        else:
            if mode == 'failure':
                self.loginFSM.request('login')
            else:
                self.notify.error('Invalid doneStatus mode from ParentPasswordScreen: ' + str(mode))

    def exitParentPassword(self):
        if self.parentPasswordScreen:
            self.parentPasswordScreen.exit()
            self.parentPasswordScreen.unload()
            self.parentPasswordScreen = None
            self.renderFrame()
        self.ignore(self.parentPasswordDoneEvent)
        self.handler = None
        del self.parentPwdDoneData
        return

    def handleParentPassword(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def enterWelcome(self, welcomeDoneData={'forward': '', 'forwardArgs': []}):
        self.welcomeDoneData = welcomeDoneData
        self.welcomeDoneEvent = 'welcomeDone'
        self.welcomeScreen = WelcomeScreen.WelcomeScreen(self, self.welcomeDoneEvent)
        self.accept(self.welcomeDoneEvent, self.__handleWelcomeScreenDone)
        self.welcomeScreen.load()
        self.welcomeScreen.enter()
        self.handler = self.handleWelcomeScreen

    def __handleWelcomeScreenDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'ok':
            self.loginFSM.request(self.welcomeDoneData['forward'], self.welcomeDoneData['forwardArgs'])
        else:
            if mode == 'quit':
                self.loginFSM.request('shutdown')
            else:
                self.notify.error('Invalid doneStatus mode from FreeTimeInformScreen: ' + str(mode))

    def exitWelcome(self):
        if self.welcomeScreen:
            self.welcomeScreen.exit()
            self.welcomeScreen.unload()
            self.welcomeScreen = None
            self.renderFrame()
        self.ignore(self.welcomeDoneEvent)
        self.handler = None
        return

    def handleWelcomeScreen(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                self.handleUnexpectedMsgType(msgType, di)

    def enterFailedToConnect(self, statusCode=0):
        self.handler = self.handleFailedToConnect
        url = self.serverList[0]
        self.notify.warning('Failed to connect to %s (status code %s).  Notifying user.' % (url.cStr(), statusCode))
        if statusCode == 1403 or statusCode == 1405 or statusCode == 1400:
            message = Localizer.TCRNoConnectProxyNoPort % (url.getServer(), url.getPort(), url.getPort())
            style = ToontownDialog.CancelOnly
        else:
            message = Localizer.TCRNoConnectTryAgain % (url.getServer(), url.getPort())
            style = ToontownDialog.TwoChoice
        self.failedToConnectBox = ToontownDialog.GlobalDialog(message=message, doneEvent='failedToConnectAck', text_wordwrap=18, style=style)
        self.failedToConnectBox.show()
        self.notify.info(message)
        self.accept('failedToConnectAck', self.__handleFailedToConnectAck)

    def __handleFailedToConnectAck(self):
        doneStatus = self.failedToConnectBox.doneStatus
        if doneStatus == 'ok':
            self.loginFSM.request('connect', [self.serverList])
        else:
            if doneStatus == 'cancel':
                self.loginFSM.request('shutdown')
            else:
                self.notify.error('Unrecognized doneStatus: ' + str(doneStatus))

    def handleFailedToConnect(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def exitFailedToConnect(self):
        self.handler = None
        self.ignore('failedToConnectAck')
        self.failedToConnectBox.cleanup()
        del self.failedToConnectBox
        return

    def enterFailedToGetServerConstants(self, e):
        self.handler = self.handleFailedToGetConstants
        url = AccountServerConstants.AccountServerConstants.getServerURL()
        statusCode = 0
        if isinstance(e, HTTPUtil.ConnectionError):
            statusCode = e.statusCode
            self.notify.warning('Got status code %s from connection to %s.' % (statusCode, url.cStr()))
        else:
            self.notify.warning("Didn't get status code from connection to %s." % url.cStr())
        if statusCode == 1403 or statusCode == 1400:
            message = Localizer.TCRServerConstantsProxyNoPort % (url.cStr(), url.getPort())
            style = ToontownDialog.CancelOnly
        else:
            if statusCode == 1405:
                message = Localizer.TCRServerConstantsProxyNoCONNECT % url.cStr()
                style = ToontownDialog.CancelOnly
            else:
                message = Localizer.TCRServerConstantsTryAgain % url.cStr()
                style = ToontownDialog.TwoChoice
        self.failedToGetConstantsBox = ToontownDialog.GlobalDialog(message=message, doneEvent='failedToGetConstantsAck', text_wordwrap=18, style=style)
        self.failedToGetConstantsBox.show()
        self.accept('failedToGetConstantsAck', self.__handleFailedToGetConstantsAck)
        self.notify.warning('Failed to get account server constants. Notifying user.')

    def __handleFailedToGetConstantsAck(self):
        doneStatus = self.failedToGetConstantsBox.doneStatus
        if doneStatus == 'ok':
            self.loginFSM.request('connect', [self.serverList])
        else:
            if doneStatus == 'cancel':
                self.loginFSM.request('shutdown')
            else:
                self.notify.error('Unrecognized doneStatus: ' + str(doneStatus))

    def handleFailedToGetConstants(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def exitFailedToGetServerConstants(self):
        self.handler = None
        self.ignore('failedToGetConstantsAck')
        self.failedToGetConstantsBox.cleanup()
        del self.failedToGetConstantsBox
        return

    def enterFailedToGetServerDate(self, retryData={'retry': None, 'retryArgs': [], 'cancel': 'shutdown', 'cancelArgs': []}):
        self.handler = self.handleFailedToGetDate
        self.retryData = retryData
        if self.retryData['retry'] == None:
            self.retryData['retry'] = 'connect'
            self.retryData['retryArgs'] = [self.serverList]
        self.failedToGetDateBox = ToontownDialog.GlobalDialog(message=Localizer.TCRServerDateTryAgain % self.accountServerDate.getServer(), doneEvent='failedToGetDateAck', style=ToontownDialog.TwoChoice)
        self.failedToGetDateBox.show()
        self.accept('failedToGetDateAck', self.__handleFailedToGetDateAck)
        self.notify.warning('Failed to get date from account server. Notifying user.')
        return

    def __handleFailedToGetDateAck(self):
        doneStatus = self.failedToGetDateBox.doneStatus
        if doneStatus == 'ok':
            self.loginFSM.request(self.retryData['retry'], self.retryData['retryArgs'])
        else:
            if doneStatus == 'cancel':
                self.loginFSM.request(self.retryData['cancel'], self.retryData['cancelArgs'])
            else:
                self.notify.error('Unrecognized doneStatus: ' + str(doneStatus))

    def handleFailedToGetDate(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def exitFailedToGetServerDate(self):
        self.handler = None
        self.ignore('failedToGetDateAck')
        self.failedToGetDateBox.cleanup()
        del self.failedToGetDateBox
        return

    def sendDisconnect(self):
        if self.tcpConn:
            datagram = Datagram()
            datagram.addUint16(CLIENT_DISCONNECT)
            self.send(datagram)
            self.notify.info('Sent disconnect message to server')
            self.disconnect()
        self.stopHeartbeat()

    def enterShutdown(self):
        self.handler = self.handleShutdown
        self.sendDisconnect()
        self.notify.info('Exiting Toontown cleanly')
        toonbase.exitShow()

    def exitShutdown(self):
        self.handler = None
        return

    def handleShutdown(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def enterWaitForShardList(self):
        self.handler = self.handleWaitForGetShardListResponse
        self.sendGetShardListMsg()

    def sendGetShardListMsg(self):
        datagram = Datagram()
        datagram.addUint16(CLIENT_GET_SHARD_LIST)
        self.send(datagram)

    def exitWaitForShardList(self):
        self.handler = None
        return

    def handleWaitForGetShardListResponse(self, msgType, di):
        if msgType == CLIENT_GET_SHARD_LIST_RESP:
            self.handleLoginGetShardListResponseMsg(di)
        else:
            if msgType == CLIENT_SERVER_UP:
                self.handleServerUp(di)
            else:
                if msgType == CLIENT_SERVER_DOWN:
                    self.handleServerDown(di)
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def handleGetShardListResponseMsg(self, di):
        numberOfShards = di.getUint16()
        if numberOfShards == 0:
            return 0
        for i in range(numberOfShards):
            shardId = di.getUint32()
            shardName = di.getString()
            shardPop = di.getUint32()
            if self.__shards.has_key(shardId):
                self.__shards[shardId].population = shardPop
            else:
                self.__shards[shardId] = PotentialShard.PotentialShard(shardId, shardName, shardPop)

        messenger.send('shardInfoUpdated')
        return numberOfShards

    def handleLoginGetShardListResponseMsg(self, di):
        numberOfShards = self.handleGetShardListResponseMsg(di)
        if numberOfShards != 0:
            self.loginFSM.request('waitForAvatarList')
        else:
            self.loginFSM.request('noShards')

    def enterNoShards(self):
        self.handler = self.handleNoShards
        self.noShardsBox = ToontownDialog.GlobalDialog(message=Localizer.TCRNoDistrictsTryAgain, doneEvent='noShardsAck', style=ToontownDialog.TwoChoice)
        self.noShardsBox.show()
        self.accept('noShardsAck', self.__handleNoShardsAck)
        self.notify.warning('No shards are available.')

    def __handleNoShardsAck(self):
        doneStatus = self.noShardsBox.doneStatus
        print doneStatus
        if doneStatus == 'ok':
            self.loginFSM.request('waitForShardList')
        else:
            if doneStatus == 'cancel':
                self.loginFSM.request('shutdown')
            else:
                self.notify.error('Unrecognized doneStatus: ' + str(doneStatus))

    def handleNoShards(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def exitNoShards(self):
        self.handler = None
        self.ignore('noShardsAck')
        self.noShardsBox.cleanup()
        del self.noShardsBox
        return

    def enterReject(self):
        self.handler = self.handleReject
        self.notify.warning('Connection Rejected')
        if launcher:
            launcher.setPandaErrorCode(13)
        sys.exit()

    def exitReject(self):
        self.handler = None
        return

    def handleReject(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def enterNoConnection(self):
        self.handler = self.handleNoConnection
        self.__currentAvId = 0
        self.stopHeartbeat()
        self.stopReaderPollTask()
        if self.bootedIndex != None and Localizer.TCRBootedReasons.has_key(self.bootedIndex):
            message = Localizer.TCRBootedReasons[self.bootedIndex]
        else:
            if self.bootedText != None:
                message = Localizer.TCRBootedReasonUnknownCode % self.bootedIndex
            else:
                message = Localizer.TCRLostConnection
        style = ToontownDialog.Acknowledge
        if self.loginInterface.supportsRelogin():
            message += Localizer.TCRTryConnectAgain
            style = ToontownDialog.TwoChoice
        self.lostConnectionBox = ToontownDialog.GlobalDialog(doneEvent='lostConnectionAck', message=message, text_wordwrap=18, style=style)
        self.lostConnectionBox.show()
        self.accept('lostConnectionAck', self.__handleLostConnectionAck)
        self.notify.warning('Lost connection to server. Notifying user.')
        return

    def __handleLostConnectionAck(self):
        if self.lostConnectionBox.doneStatus == 'ok' and self.loginInterface.supportsRelogin():
            self.loginFSM.request('connect', [self.serverList])
        else:
            self.loginFSM.request('shutdown')

    def handleNoConnection(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def exitNoConnection(self):
        self.handler = None
        self.ignore('lostConnectionAck')
        self.lostConnectionBox.cleanup()
        return

    def enterAfkTimeout(self):
        self.sendSetAvatarIdMsg(0)
        msg = Localizer.AfkForceAcknowledgeMessage
        self.afkDialog = ToontownDialog.ToontownDialog(text=msg, command=self.__handleAfkOk, style=ToontownDialog.Acknowledge)
        self.handler = self.handleAfkMessage

    def __handleAfkOk(self, value):
        self.loginFSM.request('waitForAvatarList')

    def exitAfkTimeout(self):
        if self.afkDialog:
            self.afkDialog.cleanup()
            self.afkDialog = None
        self.handler = None
        return

    def handleAfkMessage(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                if msgType == CLIENT_GET_STATE_RESP:
                    pass
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def enterPeriodTimeout(self):
        self.sendSetAvatarIdMsg(0)
        self.sendDisconnect()
        msg = Localizer.PeriodForceAcknowledgeMessage
        self.periodDialog = ToontownDialog.ToontownDialog(text=msg, command=self.__handlePeriodOk, style=ToontownDialog.Acknowledge)
        self.handler = self.handleShutdown

    def __handlePeriodOk(self, value):
        toonbase.exitShow()

    def exitPeriodTimeout(self):
        if self.periodDialog:
            self.periodDialog.cleanup()
            self.periodDialog = None
        self.handler = None
        return

    def enterWaitForAvatarList(self):
        self.handler = self.handleWaitForAvatarList
        self.sendGetAvatarsMsg()
        self.__waitForDatabaseTimeout()

    def sendGetAvatarsMsg(self):
        datagram = Datagram()
        datagram.addUint16(CLIENT_GET_AVATARS)
        self.send(datagram)

    def exitWaitForAvatarList(self):
        self.__cleanupWaitingForDatabase()
        self.handler = None
        return

    def handleWaitForAvatarList(self, msgType, di):
        if msgType == CLIENT_GET_AVATARS_RESP:
            self.handleGetAvatarsRespMsg(di)
        else:
            if msgType == CLIENT_SERVER_UP:
                self.handleServerUp(di)
            else:
                if msgType == CLIENT_SERVER_DOWN:
                    self.handleServerDown(di)
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def handleGetAvatarsRespMsg(self, di):
        returnCode = di.getUint8()
        if returnCode == 0:
            avatarTotal = di.getUint16()
            avList = []
            for i in range(0, avatarTotal):
                avNum = di.getUint32()
                avNames = [
                 '', '', '', '']
                avNames[0] = di.getString()
                avNames[1] = di.getString()
                avNames[2] = di.getString()
                avNames[3] = di.getString()
                avDNA = di.getString()
                avPosition = di.getUint8()
                aname = di.getUint8()
                potAv = PotentialAvatar.PotentialAvatar(avNum, avNames, avDNA, avPosition, aname)
                avList.append(potAv)

            self.avList = avList
            self.loginFSM.request('chooseAvatar', [self.avList])
        else:
            self.notify.error('Bad avatar list return code: ' + str(returnCode))
            self.loginFSM.request('off')

    def enterChooseAvatar(self, avList):
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        self.sendSetAvatarIdMsg(0)
        self.clearFriendState()
        if self.music == None and base.musicManagerIsValid:
            self.music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.mid')
            if self.music:
                self.music.setLoop(1)
                self.music.setVolume(0.9)
                self.music.play()
        base.playMusic(self.music, looping=1, volume=0.9, interrupt=None)
        self.handler = self.handleChooseAvatar
        self.avChoiceDoneEvent = 'avatarChooserDone'
        self.avChoice = AvatarChooser.AvatarChooser(avList, self.loginFSM, self.avChoiceDoneEvent)
        self.avChoice.load(self.isPaid())
        self.avChoice.enter()
        self.accept(self.avChoiceDoneEvent, self.__handleAvatarChooserDone, [
         avList])
        return

    def __handleAvatarChooserDone(self, avList, doneStatus):
        done = doneStatus['mode']
        if done == 'exit':
            self.loginFSM.request('shutdown')
            return
        index = self.avChoice.getChoice()
        for av in avList:
            if av.position == index:
                avatarChoice = av
                self.notify.info('================')
                self.notify.info('Chose avatar id: %s' % av.id)
                self.notify.info('Chose avatar name: %s' % av.name)
                dna = AvatarDNA.AvatarDNA()
                dna.makeFromNetString(av.dna)
                self.notify.info('Chose avatar dna: %s' % (dna.asTuple(),))
                self.notify.info('Chose avatar position: %s' % av.position)
                self.notify.info('isPaid: %s' % self.isPaid())
                self.notify.info('freeTimeLeft: %s' % self.freeTimeLeft())
                self.notify.info('allowSecretChat: %s' % self.allowSecretChat())
                self.notify.info('================')

        if done == 'chose':
            self.avChoice.exit()
            if avatarChoice.approvedName != '':
                self.congratulations(avatarChoice)
                avatarChoice.approvedName = ''
            else:
                if avatarChoice.rejectedName != '':
                    avatarChoice.rejectedName = ''
                    self.betterlucknexttime(avList, index)
                else:
                    self.loginFSM.request('waitForSetAvatarResponse', [
                     avatarChoice])
        else:
            if done == 'nameIt':
                self.goToPickAName(avList, index)
            else:
                if done == 'create':
                    self.loginFSM.request('createAvatar', [avList, index])
                else:
                    if done == 'delete':
                        self.loginFSM.request('waitForDeleteAvatarResponse', [avatarChoice])

    def congratulations(self, avatarChoice):
        self.acceptedScreen = loader.loadModel('phase_3/models/gui/toon_council')
        self.acceptedScreen.setScale(0.667)
        self.acceptedScreen.reparentTo(aspect2d)
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        self.acceptedBanner = DirectLabel(parent=self.acceptedScreen, relief=None, text=Localizer.TCRNameCongratulations, text_scale=0.18, text_fg=Vec4(0.6, 0.1, 0.1, 1), text_pos=(0, 0.05), text_font=getMinnieFont())
        newName = avatarChoice.approvedName
        self.acceptedText = DirectLabel(parent=self.acceptedScreen, relief=None, text=Localizer.TCRNameAccepted % newName, text_scale=0.125, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, -0.15))
        self.okButton = DirectButton(parent=self.acceptedScreen, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief=None, text='Ok', scale=1.5, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0, 0, -1), command=self.__handleCongrats, extraArgs=[avatarChoice])
        buttons.removeNode()
        return

    def __handleCongrats(self, avatarChoice):
        self.acceptedBanner.destroy()
        self.acceptedText.destroy()
        self.okButton.destroy()
        self.acceptedScreen.removeNode()
        del self.acceptedScreen
        del self.okButton
        del self.acceptedText
        del self.acceptedBanner
        datagram = Datagram()
        datagram.addUint16(CLIENT_SET_WISHNAME_CLEAR)
        datagram.addUint32(avatarChoice.id)
        datagram.addUint8(1)
        self.send(datagram)
        self.loginFSM.request('waitForSetAvatarResponse', [avatarChoice])

    def betterlucknexttime(self, avList, index):
        self.rejectDoneEvent = 'rejectDone'
        self.rejectDialog = ToontownDialog.GlobalDialog(doneEvent=self.rejectDoneEvent, message=Localizer.NameShopNameRejected, style=ToontownDialog.Acknowledge)
        self.rejectDialog.show()
        self.acceptOnce(self.rejectDoneEvent, self.__handleReject, [
         avList, index])

    def __handleReject(self, avList, index):
        self.rejectDialog.cleanup()
        datagram = Datagram()
        datagram.addUint16(CLIENT_SET_WISHNAME_CLEAR)
        avid = 0
        for k in avList:
            if k.position == index:
                avid = k.id

        if avid == 0:
            self.notify.error('Avatar rejected not found in avList.  Index is: ' + str(index))
        datagram.addUint32(avid)
        datagram.addUint8(0)
        self.send(datagram)
        self.loginFSM.request('waitForAvatarList')

    def handleChooseAvatar(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                if msgType == CLIENT_GET_STATE_RESP:
                    pass
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def exitChooseAvatar(self):
        self.handler = None
        self.avChoice.exit()
        self.avChoice.unload()
        self.avChoice = None
        self.ignore(self.avChoiceDoneEvent)
        return

    def goToPickAName(self, avList, index):
        self.avChoice.exit()
        self.loginFSM.request('createAvatar', [avList, index])

    def cancelledPay(self, avList, index):
        self.avChoice.exit()
        self.loginFSM.request('createAvatar', [avList, index])

    def enterCreateAvatar(self, avList, index, newDNA=None):
        if self.music:
            self.music.stop()
            self.music = None
        if newDNA != None:
            self.newPotAv = PotentialAvatar.PotentialAvatar('deleteMe', [
             '', '', '', ''], newDNA.makeNetString(), index, 1)
            avList.append(self.newPotAv)
        base.transitions.noFade()
        self.avCreate = MakeAToon.MakeAToon(self.loginFSM, avList, 'makeAToonComplete', index, self.isPaid())
        self.avCreate.load()
        self.avCreate.enter()
        self.handler = self.handleCreateAvatar
        self.accept('makeAToonComplete', self.__handleMakeAToon, [avList, index])
        self.accept('nameShopPost', self.relayMessage)
        return

    def relayMessage(self, dg):
        self.send(dg)

    def handleCreateAvatar(self, msgType, di):
        if msgType == CLIENT_SERVER_UP:
            self.handleServerUp(di)
        else:
            if msgType == CLIENT_SERVER_DOWN:
                self.handleServerDown(di)
            else:
                if msgType == CLIENT_CREATE_AVATAR_RESP or msgType == CLIENT_SET_NAME_PATTERN_ANSWER or msgType == CLIENT_SET_WISHNAME_RESP:
                    self.avCreate.ns.nameShopHandler(msgType, di)
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def __handleMakeAToon(self, avList, avPosition):
        done = self.avCreate.getDoneStatus()
        if done == 'cancel':
            if hasattr(self, 'newPotAv'):
                if self.newPotAv in avList:
                    avList.remove(self.newPotAv)
            self.avCreate.exit()
            self.loginFSM.request('chooseAvatar', [avList])
        else:
            if done == 'paynow':
                retArgs = [self.avCreate.ns.avList, self.avCreate.ns.index, self.avCreate.dna]
                if hasattr(self, 'newPotAv'):
                    if self.newPotAv in avList:
                        avList.remove(self.newPotAv)
                self.avCreate.exit()
                self.loginFSM.request('memberAgreement', [{'forward': 'createAvatar', 'forwardArgs': retArgs, 'back': 'createAvatar', 'backArgs': retArgs}])
            else:
                if done == 'created':
                    self.avCreate.exit()
                    if not base.launcher or base.launcher.getPhaseComplete(3.5):
                        for i in avList:
                            if i.position == avPosition:
                                newPotAv = i

                        self.loginFSM.request('waitForSetAvatarResponse', [newPotAv])
                    else:
                        self.loginFSM.request('chooseAvatar', [avList])
                else:
                    self.notify.error('Invalid doneStatus from MakeAToon: ' + str(done))

    def exitCreateAvatar(self):
        self.ignore('makeAToonComplete')
        self.ignore('nameShopPost')
        self.avCreate.unload()
        self.avCreate = None
        self.handler = None
        if hasattr(self, 'newPotAv'):
            del self.newPotAv
        return

    def enterWaitForDeleteAvatarResponse(self, potAv):
        self.handler = self.handleWaitForDeleteAvatarResponse
        self.sendDeleteAvatarMsg(potAv.id)
        self.__waitForDatabaseTimeout()

    def sendDeleteAvatarMsg(self, avId):
        datagram = Datagram()
        datagram.addUint16(CLIENT_DELETE_AVATAR)
        datagram.addUint32(avId)
        self.send(datagram)

    def exitWaitForDeleteAvatarResponse(self):
        self.__cleanupWaitingForDatabase()
        self.handler = None
        return

    def handleWaitForDeleteAvatarResponse(self, msgType, di):
        if msgType == CLIENT_DELETE_AVATAR_RESP:
            self.handleGetAvatarsRespMsg(di)
        else:
            if msgType == CLIENT_SERVER_UP:
                self.handleServerUp(di)
            else:
                if msgType == CLIENT_SERVER_DOWN:
                    self.handleServerDown(di)
                else:
                    self.handleUnexpectedMsgType(msgType, di)

    def enterWaitForSetAvatarResponse(self, potAv):
        self.handler = self.handleWaitForSetAvatarResponse
        self.sendSetAvatarMsg(potAv)
        self.__waitForDatabaseTimeout()

    def sendSetAvatarMsg(self, potAv):
        self.sendSetAvatarIdMsg(potAv.id)
        self.avData = potAv

    def sendSetAvatarIdMsg(self, avId):
        if avId != self.__currentAvId:
            self.__currentAvId = avId
            datagram = Datagram()
            datagram.addUint16(CLIENT_SET_AVATAR)
            datagram.addUint32(avId)
            self.send(datagram)
            if avId == 0:
                self.stopPeriodTimer()
            else:
                self.startPeriodTimer()

    def resetPeriodTimer(self, secondsRemaining):
        self.periodTimerExpired = 0
        self.periodTimerSecondsRemaining = secondsRemaining

    def recordPeriodTimer(self, task):
        freq = 60.0
        elapsed = globalClock.getFrameTime() - self.periodTimerStarted
        self.runningPeriodTimeRemaining -= elapsed
        launcher.recordPeriodTimeRemaining(self.runningPeriodTimeRemaining)
        taskMgr.doMethodLater(freq, self.recordPeriodTimer, 'periodTimerRecorder')
        return Task.done

    def startPeriodTimer(self):
        if self.periodTimerStarted == None and self.periodTimerSecondsRemaining != None:
            self.periodTimerStarted = globalClock.getFrameTime()
            taskMgr.doMethodLater(self.periodTimerSecondsRemaining, self.__periodTimerExpired, 'periodTimerCountdown')
            for warning in ToontownGlobals.PeriodTimerWarningTime:
                if self.periodTimerSecondsRemaining > warning:
                    taskMgr.doMethodLater(self.periodTimerSecondsRemaining - warning, self.__periodTimerWarning, 'periodTimerCountdown')

            self.runningPeriodTimeRemaining = self.periodTimerSecondsRemaining
            self.recordPeriodTimer(None)
        return

    def stopPeriodTimer(self):
        if self.periodTimerStarted != None:
            elapsed = globalClock.getFrameTime() - self.periodTimerStarted
            self.periodTimerSecondsRemaining -= elapsed
            self.periodTimerStarted = None
        taskMgr.remove('periodTimerCountdown')
        taskMgr.remove('periodTimerRecorder')
        return

    def __periodTimerWarning(self, task):
        toonbase.localToon.setSystemMessage(0, Localizer.PeriodTimerWarning)
        return Task.done

    def __periodTimerExpired(self, task):
        self.notify.info("User's period timer has just expired!")
        self.periodTimerExpired = 1
        self.periodTimerStarted = None
        self.periodTimerSecondsRemaining = None
        messenger.send('periodTimerExpired')
        return Task.done
        return

    def handleWaitForSetAvatarResponse(self, msgType, di):
        if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
            self.handleAvatarResponseMsg(di)
        else:
            if msgType == CLIENT_GET_FRIEND_LIST_RESP:
                self.__handleGetFriendsList(di)
            else:
                if msgType == CLIENT_FRIEND_ONLINE:
                    self.__handleFriendOnline(di)
                else:
                    if msgType == CLIENT_FRIEND_OFFLINE:
                        self.__handleFriendOffline(di)
                    else:
                        if msgType == CLIENT_SERVER_UP:
                            self.handleServerUp(di)
                        else:
                            if msgType == CLIENT_SERVER_DOWN:
                                self.handleServerDown(di)
                            else:
                                self.handleUnexpectedMsgType(msgType, di)

    def handleAvatarResponseMsg(self, di):
        self.__cleanupWaitingForDatabase()
        avatarId = di.getUint32()
        returnCode = di.getUint8()
        if returnCode == 0:
            if self.notify.getDebug():
                self.notify.debug('name2cdc: ' + str(self.name2cdc))
            cdc = self.name2cdc['DistributedToon']
            NametagGlobals.setMasterArrowsOn(0)
            loader.beginBulkLoad('localToonPlayGame', Localizer.TCREnteringToontown, 122)
            localToon = LocalToon.LocalToon(self)
            toonbase.localToon = localToon
            NametagGlobals.setToon(toonbase.localToon)
            localToon.doId = avatarId
            self.localToonDoId = avatarId
            localToon.updateAllRequiredFields(cdc, di)
            self.doId2do[avatarId] = localToon
            self.doId2cdc[avatarId] = cdc
            localToon.generate()
            localToon.announceGenerate()
            self.__sendGetFriendsListRequest()
            self.gameFSM.request('waitOnEnterResponses', [
             localToon.defaultShard, localToon.defaultZone, localToon.defaultZone, -1])
        else:
            self.notify.error('Bad avatar: return code %d' % returnCode)

    def exitWaitForSetAvatarResponse(self):
        self.__cleanupWaitingForDatabase()
        self.handler = None
        ivalMgr.interrupt()
        if hasattr(toonbase, 'localToon'):
            camera.reparentTo(render)
            camera.setPos(0, 0, 0)
            camera.setHpr(0, 0, 0)
            del self.doId2do[toonbase.localToon.getDoId()]
            del self.doId2cdc[toonbase.localToon.getDoId()]
            toonbase.localToon.disable()
            toonbase.localToon.delete()
            NametagGlobals.setToon(base.cam)
            del toonbase.localToon
        if self.friendManager != None:
            self.friendManager.delete()
            self.friendManager = None
        if self.timeManager != None:
            self.timeManager.delete()
            self.timeManager = None
        if self.trophyManager != None:
            self.trophyManager.delete()
            self.trophyManager = None
        if self.bankManager != None:
            self.bankManager.delete()
            self.bankManager = None
        if self.mailboxManager != None:
            self.mailboxManager.delete()
            self.mailboxManager = None
        FriendSecret.unloadFriendSecret()
        FriendsListPanel.unloadFriendsList()
        messenger.send('cancelFriendInvitation')
        loader.abortBulkLoad()
        allowedTasks = (
         'dataloop', 'doLaterProcessor', 'eventManager', 'readerPollTask', 'heartBeat', 'igloop', 'collisionloop', 'ivalloop', 'downloadSequence', 'patchAndHash', 'launcher-download', 'launcher-download-multifile', 'launcher-decompressFile', 'launcher-decompressMultifile', 'launcher-extract', 'launcher-patch', 'tkloop', 'manager-update', 'downloadStallTask', 'irisTask', 'fadeTask')
        problems = []
        for taskPriList in taskMgr.taskList:
            for task in taskPriList:
                if task is None:
                    continue
                else:
                    if task.isRemoved():
                        continue
                    else:
                        if task.name in allowedTasks:
                            continue
                        else:
                            problems.append(task.name)

        if problems:
            print taskMgr
            msg = "You can't leave toontown until you clean up your tasks:"
            for task in problems:
                msg += '\n  ' + task

            self.notify.error(msg)
        allowedHooks = [
         'destroy-DownloadWatcherBar', 'destroy-DownloadWatcherText', 'destroy-ToontownLoaderWaitBar', 'destroy-fade', 'f9-up', 'launcherAllPhasesComplete', 'launcherPercentPhaseComplete', 'page_down', 'page_up', 'PandaPaused', 'PandaRestarted', 'phaseComplete-3', 'press-mouse2-fade', 'print-fade', 'release-mouse2-fade', 'resetClock', 'window-event']
        problems = []
        for hook in messenger.dict.keys():
            if hook in allowedHooks:
                pass
            else:
                problems.append(hook)

        if problems:
            print messenger
            msg = "You can't leave toontown until you clean up your hooks:"
            for hook in problems:
                msg += '\n  ' + hook

            self.notify.error(msg)
        if ivalMgr.getNumIntervals() > 0:
            print ivalMgr
            self.notify.error("You can't leave toontown until you clean up your intervals.")
        return None
        return

    def enterGameOff(self):
        self.handler = self.handleGameOff
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def exitGameOff(self):
        self.handler = None
        return

    def handleGameOff(self, msgType, di):
        self.handleUnexpectedMsgType(msgType, di)

    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        self.handler = self.handleWaitOnEnterResponses
        self.handlerArgs = {'hoodId': hoodId, 'zoneId': zoneId, 'avId': avId}
        self.sendSetShardMsg(shardId)
        toonbase.localToon.defaultShard = shardId
        time.sleep(1)
        self.__waitForDatabaseTimeout()

    def handleWaitOnEnterResponses(self, msgType, di):
        if msgType == CLIENT_GET_STATE_RESP:
            self.handleSetShardResponse(di)
        else:
            if msgType == CLIENT_GET_FRIEND_LIST_RESP:
                self.__handleGetFriendsList(di)
            else:
                if msgType == CLIENT_FRIEND_ONLINE:
                    self.__handleFriendOnline(di)
                else:
                    if msgType == CLIENT_FRIEND_OFFLINE:
                        self.__handleFriendOffline(di)
                    else:
                        if msgType == CLIENT_SERVER_UP:
                            self.handleServerUp(di)
                        else:
                            if msgType == CLIENT_SERVER_DOWN:
                                self.handleServerDown(di)
                            else:
                                self.handleUnexpectedMsgType(msgType, di)

    def handleSetShardResponse(self, di):
        self.__cleanupWaitingForDatabase()
        hoodId = self.handlerArgs['hoodId']
        zoneId = self.handlerArgs['zoneId']
        avId = self.handlerArgs['avId']
        self.gameFSM.request('waitForTimeManager', [hoodId, zoneId, avId])
        return

    def exitWaitOnEnterResponses(self):
        self.__cleanupWaitingForDatabase()
        self.handler = None
        self.handlerArgs = None
        return

    def enterWaitForTimeManager(self, hoodId, zoneId, avId):
        self.handler = self.handleWaitForTimeManager
        self.handlerArgs = {'hoodId': hoodId, 'zoneId': zoneId, 'avId': avId}
        self.sendSetZoneMsg(QuietZone)
        self.__waitForDatabaseTimeout(20)
        return

    def handleWaitForTimeManager(self, msgType, di):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        else:
            if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
                self.handleGenerateWithRequiredOther(di)
            else:
                if msgType == CLIENT_OBJECT_UPDATE_FIELD:
                    self.handleUpdateField(di)
                else:
                    if msgType == CLIENT_OBJECT_DISABLE_RESP:
                        self.handleDisable(di)
                    else:
                        if msgType == CLIENT_OBJECT_DELETE_RESP:
                            self.handleDelete(di)
                        else:
                            if msgType == CLIENT_GET_FRIEND_LIST_RESP:
                                self.__handleGetFriendsList(di)
                            else:
                                if msgType == CLIENT_FRIEND_ONLINE:
                                    self.__handleFriendOnline(di)
                                else:
                                    if msgType == CLIENT_FRIEND_OFFLINE:
                                        self.__handleFriendOffline(di)
                                    else:
                                        if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
                                            self.__handleGetAvatarDetailsResp(di)
                                        else:
                                            if msgType == CLIENT_SERVER_UP:
                                                self.handleServerUp(di)
                                            else:
                                                if msgType == CLIENT_SERVER_DOWN:
                                                    self.handleServerDown(di)
                                                else:
                                                    if msgType == CLIENT_GET_STATE_RESP:
                                                        pass
                                                    else:
                                                        if msgType == CLIENT_DONE_SET_ZONE_RESP:
                                                            zoneId = di.getInt16()
                                                            if zoneId == QuietZone:
                                                                self.gotTimeManager()
                                                        else:
                                                            self.handleUnexpectedMsgType(msgType, di)

    def gotTimeManager(self):
        self.__cleanupWaitingForDatabase()
        if self.trophyManager != None:
            self.trophyManager.d_requestTrophyScore()
        if self.timeManager == None:
            self.notify.info('TimeManager is not present.')
            DistributedSmoothNode.activateSmoothing(0, 0)
            self.gotTimeSync()
        else:
            DistributedSmoothNode.activateSmoothing(1, 0)
            if self.timeManager.synchronize('startup'):
                self.accept('gotTimeSync', self.gotTimeSync)
                taskMgr.doMethodLater(5.0, self.timeSyncTimeout, 'timeSyncTimeout')
            else:
                self.notify.info('No sync from TimeManager.')
                self.gotTimeSync()
        return

    def timeSyncTimeout(self, task):
        self.notify.warning('Timeout waiting for sync from TimeManager.')
        self.gotTimeSync()
        return Task.done

    def gotTimeSync(self):
        self.ignore('gotTimeSync')
        taskMgr.remove('timeSyncTimeout')
        hoodId = self.handlerArgs['hoodId']
        zoneId = self.handlerArgs['zoneId']
        avId = self.handlerArgs['avId']
        if toonbase.localToon.tutorialAck:
            self.gameFSM.request('playGame', [hoodId, zoneId, avId])
        else:
            if base.config.GetBool('force-tutorial', 1):
                self.gameFSM.request('tutorialQuestion', [hoodId, zoneId, avId])
            else:
                self.gameFSM.request('playGame', [hoodId, zoneId, avId])
        return

    def exitWaitForTimeManager(self):
        self.__cleanupWaitingForDatabase()
        self.ignore('gotTimeSync')
        self.handler = None
        self.handlerArgs = None
        return
        return

    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        self.handler = self.handleTutorialQuestion
        self.__requestTutorial(hoodId, zoneId, avId)
        return

    def handleTutorialQuestion(self, msgType, di):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        else:
            if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
                self.handleGenerateWithRequiredOther(di)
            else:
                if msgType == CLIENT_OBJECT_UPDATE_FIELD:
                    self.handleUpdateField(di)
                else:
                    if msgType == CLIENT_OBJECT_DISABLE_RESP:
                        self.handleDisable(di)
                    else:
                        if msgType == CLIENT_OBJECT_DELETE_RESP:
                            self.handleDelete(di)
                        else:
                            if msgType == CLIENT_GET_FRIEND_LIST_RESP:
                                self.__handleGetFriendsList(di)
                            else:
                                if msgType == CLIENT_FRIEND_ONLINE:
                                    self.__handleFriendOnline(di)
                                else:
                                    if msgType == CLIENT_FRIEND_OFFLINE:
                                        self.__handleFriendOffline(di)
                                    else:
                                        if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
                                            self.__handleGetAvatarDetailsResp(di)
                                        else:
                                            if msgType == CLIENT_SERVER_UP:
                                                self.handleServerUp(di)
                                            else:
                                                if msgType == CLIENT_SERVER_DOWN:
                                                    self.handleServerDown(di)
                                                else:
                                                    if msgType == CLIENT_GET_STATE_RESP:
                                                        pass
                                                    else:
                                                        if msgType == CLIENT_DONE_SET_ZONE_RESP:
                                                            pass
                                                        else:
                                                            self.handleUnexpectedMsgType(msgType, di)

    def __requestTutorial(self, hoodId, zoneId, avId):
        self.acceptOnce('startTutorial', self.__handleStartTutorial, [
         avId])
        messenger.send('requestTutorial')
        abandonTask = taskMgr.doMethodLater(10, self.__abandonTutorialTask, 'waitingForTutorial')
        abandonTask.hoodId = hoodId
        abandonTask.zoneId = zoneId
        abandonTask.avId = avId
        return

    def __abandonTutorialTask(self, task):
        self.gameFSM.request('playGame', [task.hoodId, task.zoneId, task.avId])
        return Task.done

    def __handleStartTutorial(self, avId, zoneId):
        self.gameFSM.request('playGame', [Tutorial, zoneId, avId])
        return

    def exitTutorialQuestion(self):
        self.handler = None
        self.handlerArgs = None
        self.ignore('startTutorial')
        taskMgr.remove('waitingForTutorial')
        return
        return

    def enterPlayGame(self, hoodId, zoneId, avId):
        if self.music:
            self.music.stop()
            self.music = None
        self.handler = self.handlePlayGame
        self.accept(self.gameDoneEvent, self.handleGameDone)
        base.transitions.noFade()
        self.playGame.load()
        loader.endBulkLoad('localToonPlayGame')
        self.playGame.enter(hoodId, zoneId, avId)
        return

    def handleGameDone(self):
        if self.timeManager:
            self.timeManager.setDisconnectReason(ToontownGlobals.DisconnectSwitchShards)
        doneStatus = self.playGame.getDoneStatus()
        how = doneStatus['how']
        shardId = doneStatus['shardId']
        hoodId = doneStatus['hoodId']
        zoneId = doneStatus['zoneId']
        avId = doneStatus['avId']
        if how == 'teleportIn':
            self.gameFSM.request('waitOnEnterResponses', [
             shardId, hoodId, zoneId, avId])
        else:
            self.notify.error('Exited shard with unexpected mode %s' % how)

    def exitPlayGame(self):
        self.handler = None
        self.playGame.exit()
        self.playGame.unload()
        self.disableAllBetweenShards()
        self.ignore(self.gameDoneEvent)
        return

    def handlePlayGame(self, msgType, di):
        if self.notify.getDebug():
            self.notify.debug('handle play game got message type: ' + `msgType`)
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        else:
            if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
                self.handleGenerateWithRequiredOther(di)
            else:
                if msgType == CLIENT_OBJECT_UPDATE_FIELD:
                    self.handleUpdateField(di)
                else:
                    if msgType == CLIENT_OBJECT_DISABLE_RESP:
                        self.handleDisable(di)
                    else:
                        if msgType == CLIENT_OBJECT_DELETE_RESP:
                            self.handleDelete(di)
                        else:
                            if msgType == CLIENT_GET_FRIEND_LIST_RESP:
                                self.__handleGetFriendsList(di)
                            else:
                                if msgType == CLIENT_FRIEND_ONLINE:
                                    self.__handleFriendOnline(di)
                                else:
                                    if msgType == CLIENT_FRIEND_OFFLINE:
                                        self.__handleFriendOffline(di)
                                    else:
                                        if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
                                            self.__handleGetAvatarDetailsResp(di)
                                        else:
                                            if msgType == CLIENT_SERVER_UP:
                                                self.handleServerUp(di)
                                            else:
                                                if msgType == CLIENT_SERVER_DOWN:
                                                    self.handleServerDown(di)
                                                else:
                                                    if msgType == CLIENT_GET_SHARD_LIST_RESP:
                                                        self.handleGetShardListResponseMsg(di)
                                                    else:
                                                        if msgType == CLIENT_GET_STATE_RESP:
                                                            di.skipBytes(12)
                                                            zoneId = di.getInt16()
                                                        else:
                                                            if msgType == CLIENT_DONE_SET_ZONE_RESP:
                                                                zoneId = di.getInt16()
                                                            else:
                                                                self.handleUnexpectedMsgType(msgType, di)

    def sendQuietZoneRequest(self):
        self.disableAll()
        datagram = Datagram()
        datagram.addUint16(CLIENT_SET_ZONE)
        datagram.addUint16(QuietZone)
        self.send(datagram)

    def disableAll(self):
        distObjs = self.doId2do.values()
        for distObj in distObjs:
            if distObj.getNeverDisable():
                pass
            else:
                self.disableDoId(distObj.doId)

    def disableAllBetweenShards(self):
        distObjs = self.doId2do.values()
        for distObj in distObjs:
            if distObj.doId == toonbase.localToon.doId:
                pass
            else:
                self.disableDoId(distObj.doId)

    def fillUpFriendsMap(self):
        if self.isFriendsMapComplete():
            return 1
        if not self.friendsMapPending and not self.friendsListError:
            self.notify.warning('Friends list stale; fetching new list.')
            self.__sendGetFriendsListRequest()
        return 0

    def isFriend(self, doId):
        for friendId, flags in toonbase.localToon.friendsList:
            if friendId == doId:
                self.identifyFriend(doId)
                return 1

        return 0

    def getFriendFlags(self, doId):
        for friendId, flags in toonbase.localToon.friendsList:
            if friendId == doId:
                return flags

        return 0

    def isFriendOnline(self, doId):
        return self.friendsOnline.has_key(doId)

    def identifyFriend(self, doId):
        if self.friendsMap.has_key(doId):
            return self.friendsMap[doId]
        avatar = None
        if self.doId2do.has_key(doId):
            avatar = self.doId2do[doId]
        else:
            if self.cache.contains(doId):
                avatar = self.cache.dict[doId]
            else:
                self.notify.warning("Don't know who friend %d is." % doId)
                return None
        handle = FriendHandle.FriendHandle(doId, avatar.getName(), avatar.style)
        self.friendsMap[doId] = handle
        return handle
        return

    def identifyAvatar(self, doId):
        if self.doId2do.has_key(doId):
            return self.doId2do[doId]
        else:
            return self.identifyFriend(doId)

    def isFriendsMapComplete(self):
        for friendId, flags in toonbase.localToon.friendsList:
            if self.identifyFriend(friendId) == None:
                return 0

        return 1
        return

    def removeFriend(self, avatarId):
        toonbase.localToon.sendUpdate('friendsNotify', [toonbase.localToon.doId, 1], sendToId=avatarId)
        datagram = Datagram()
        datagram.addUint16(CLIENT_REMOVE_FRIEND)
        datagram.addUint32(avatarId)
        self.send(datagram)
        self.estateMgr.removeFriend(toonbase.localToon.doId, avatarId)
        for pair in toonbase.localToon.friendsList:
            friendId = pair[0]
            if friendId == avatarId:
                toonbase.localToon.friendsList.remove(pair)
                return

    def clearFriendState(self):
        self.friendsMap = {}
        self.friendsOnline = {}
        self.friendsMapPending = 0
        self.friendsListError = 0

    def __sendGetFriendsListRequest(self):
        self.friendsMapPending = 1
        self.friendsListError = 0
        datagram = Datagram()
        datagram.addUint16(CLIENT_GET_FRIEND_LIST)
        self.send(datagram)

    def __handleGetFriendsList(self, di):
        error = di.getUint8()
        if error:
            self.notify.warning('Got error return from friends list.')
            self.friendsListError = 1
        count = di.getUint16()
        for i in range(0, count):
            doId = di.getUint32()
            name = di.getString()
            dnaString = di.getString()
            dna = AvatarDNA.AvatarDNA()
            dna.makeFromNetString(dnaString)
            handle = FriendHandle.FriendHandle(doId, name, dna)
            self.friendsMap[doId] = handle
            if self.friendsOnline.has_key(doId):
                self.friendsOnline[doId] = handle

        self.friendsMapPending = 0
        messenger.send('friendsMapComplete')

    def __handleFriendOnline(self, di):
        doId = di.getUint32()
        self.notify.debug('Friend %d now online.' % doId)
        if not self.friendsOnline.has_key(doId):
            self.friendsOnline[doId] = self.identifyFriend(doId)
            messenger.send('friendOnline', [doId])

    def __handleFriendOffline(self, di):
        doId = di.getUint32()
        self.notify.debug('Friend %d now offline.' % doId)
        try:
            del self.friendsOnline[doId]
            messenger.send('friendOffline', [doId])
        except:
            pass

    def getAvatarDetails(self, avatar, func, *args):
        task = Task.Task(func)
        task.args = args
        task.avatar = avatar
        avId = avatar.doId
        self.__queryAvatarMap[avId] = task
        self.__sendGetAvatarDetails(avId)

    def cancelAvatarDetailsRequest(self, avatar):
        avId = avatar.doId
        if self.__queryAvatarMap.has_key(avId):
            del self.__queryAvatarMap[avId]

    def __sendGetAvatarDetails(self, avId):
        datagram = Datagram()
        datagram.addUint16(CLIENT_GET_AVATAR_DETAILS)
        datagram.addUint32(avId)
        self.send(datagram)

    def __handleGetAvatarDetailsResp(self, di):
        avId = di.getUint32()
        returnCode = di.getUint8()
        self.notify.info('Got query response for avatar %d, code = %d.' % (avId, returnCode))
        try:
            task = self.__queryAvatarMap[avId]
        except:
            self.notify.warning('Received unexpected or outdated details for avatar %d.' % avId)
            return
        else:
            del self.__queryAvatarMap[avId]
            gotData = 0
            if returnCode != 0:
                self.notify.warning('No information available for avatar %d.' % avId)
            else:
                cdc = self.name2cdc['DistributedToon']
                task.avatar.updateAllRequiredFields(cdc, di)
                gotData = 1
            if isinstance(task.__call__, types.StringType):
                messenger.send(task.__call__, list((gotData, task.avatar) + task.args))
            apply(task.__call__, (gotData, task.avatar) + task.args)

    def isFreeTimeExpired(self):
        if self.accountOldAuth:
            return 0
        if base.config.GetBool('free-time-expired', 0):
            return 1
        if base.config.GetBool('unlimited-free-time', 0):
            return 0
        if self.freeTimeExpiresAt == -1:
            return 0
        if self.freeTimeExpiresAt == 0:
            return 1
        if self.freeTimeExpiresAt < -1:
            self.notify.warning('freeTimeExpiresAt is less than -1 (%s)' % self.freeTimeExpiresAt)
        if self.freeTimeExpiresAt < time.time():
            return 1
        else:
            return 0

    def freeTimeLeft(self):
        if self.freeTimeExpiresAt == -1 or self.freeTimeExpiresAt == 0:
            return 0
        secsLeft = self.freeTimeExpiresAt - time.time()
        return max(0, secsLeft)

    def isWebPlayToken(self):
        return self.playToken != None
        return

    def isPaid(self):
        if base.config.GetBool('force-paid', 0):
            return 1
        return self.__isPaid

    def setIsPaid(self, isPaid):
        self.__isPaid = isPaid

    def allowFreeNames(self):
        return base.config.GetInt('allow-free-names', 1)

    def allowSecretChat(self):
        return self.isPaid() and self.secretChatAllowed

    def logAccountInfo(self):
        self.notify.info('*** ACCOUNT INFO ***')
        self.notify.info('username: %s' % self.userName)
        if self.blue:
            self.notify.info('paid: %s (blue)' % self.isPaid())
        else:
            self.notify.info('paid: %s' % self.isPaid())
        if not self.isPaid():
            if self.isFreeTimeExpired():
                self.notify.info('free time is expired')
            else:
                secs = self.freeTimeLeft()
                self.notify.info('free time left: %s' % PythonUtil.formatElapsedSeconds(secs))
        if self.periodTimerSecondsRemaining != None:
            self.notify.info('period time left: %s' % PythonUtil.formatElapsedSeconds(self.periodTimerSecondsRemaining))
        return

    def getShardName(self, shardId):
        try:
            return self.__shards[shardId].name
        except:
            return None

        return

    def isShardAvailable(self, shardId):
        try:
            return self.__shards[shardId].available
        except:
            return 0

    def listAvailableShards(self):
        list = []
        for s in self.__shards.values():
            if s.available:
                list.append((s.id, s.name, s.population))

        return list

    def handleServerUp(self, di):
        shardId = di.getUint32()
        shardName = di.getString()
        potShard = PotentialShard.PotentialShard(shardId, shardName, 0)
        potShard.available = 1
        self.__shards[shardId] = potShard
        self.notify.info('shard %s is now available.' % shardName)
        messenger.send('shardInfoUpdated')

    def handleServerDown(self, di):
        shardId = di.getUint32()
        try:
            potShard = self.__shards[shardId]
            potShard.available = 0
            self.notify.info('shard %s is no longer available.' % potShard.name)
        except:
            self.notify.info('Unknown shard %d is no longer available.' % shardId)

        messenger.send('shardInfoUpdated')

    def handleDatagram(self, datagram):
        if self.notify.getDebug():
            print 'ToontownClientRepository received datagram:'
            datagram.dumpHex(ostream)
        di = DatagramIterator(datagram)
        msgType = di.getUint16()
        if self.notify.getDebug():
            self.notify.debug('handleDatagram: msgType: ' + `msgType`)
        if self.handler == None:
            self.handleUnexpectedMsgType(msgType, di)
        else:
            self.handler(msgType, di)
        self.considerHeartbeat()
        return

    def sendHeartbeat(self):
        datagram = Datagram()
        datagram.addUint16(CLIENT_HEARTBEAT)
        self.send(datagram)
        self.lastHeartbeat = globalClock.getRealTime()
        if self.tcpConn:
            self.tcpConn.considerFlush()

    def considerHeartbeat(self):
        if not self.heartbeatStarted:
            self.notify.debug('Heartbeats not started; not sending.')
            return
        elapsed = globalClock.getRealTime() - self.lastHeartbeat
        if elapsed < 0 or elapsed > self.heartbeatInterval:
            self.notify.info('Sending heartbeat mid-frame.')
            self.startHeartbeat()

    def stopHeartbeat(self):
        taskMgr.remove('heartBeat')
        self.heartbeatStarted = 0

    def startHeartbeat(self):
        self.stopHeartbeat()
        self.heartbeatStarted = 1
        self.sendHeartbeat()
        self.waitForNextHeartBeat()

    def sendHeartbeatTask(self, task):
        self.sendHeartbeat()
        self.waitForNextHeartBeat()
        return Task.done

    def waitForNextHeartBeat(self):
        taskMgr.doMethodLater(self.heartbeatInterval, self.sendHeartbeatTask, 'heartBeat')

    def __waitForDatabaseTimeout(self, extraTimeout=0):
        taskMgr.remove('waitingForDatabase')
        globalClock.tick()
        print 'started waiting at %s' % globalClock.getFrameTime()
        taskMgr.doMethodLater(DatabaseDialogTimeout + extraTimeout, self.__showWaitingForDatabase, 'waitingForDatabase')

    def __showWaitingForDatabase(self, task):
        print 'timed out waiting at %s' % globalClock.getFrameTime()
        self.waitingForDatabase = ToontownDialog.ToontownDialog(text=Localizer.TCRToontownUnavailable, dialogName='WaitingForDatabase', buttonTextList=[Localizer.TCRToontownUnavailableCancel], style=ToontownDialog.Acknowledge, command=self.__handleCancelWaiting)
        self.waitingForDatabase.show()
        taskMgr.remove('waitingForDatabase')
        taskMgr.doMethodLater(DatabaseGiveupTimeout, self.__giveUpWaitingForDatabase, 'waitingForDatabase')
        return Task.done

    def __giveUpWaitingForDatabase(self, task):
        self.__cleanupWaitingForDatabase()
        self.loginFSM.request('noConnection')
        return Task.done

    def __cleanupWaitingForDatabase(self):
        if self.waitingForDatabase != None:
            self.waitingForDatabase.hide()
            self.waitingForDatabase.cleanup()
            self.waitingForDatabase = None
        taskMgr.remove('waitingForDatabase')
        return

    def __handleCancelWaiting(self, value):
        self.loginFSM.request('shutdown')

    def getFirstBattle(self):
        import DistributedBattleBase
        for dobj in self.doId2do.values():
            if isinstance(dobj, DistributedBattleBase.DistributedBattleBase):
                return dobj

        return None
        return

    def setIsNotNewInstallation(self):
        if launcher:
            launcher.setIsNotNewInstallation()

    def renderFrame(self):
        base.graphicsEngine.renderFrame()

    def forbidCheesyEffects(self, forbid):
        wasAllowed = self.__forbidCheesyEffects != 0
        if forbid:
            self.__forbidCheesyEffects += 1
        else:
            self.__forbidCheesyEffects -= 1
        isAllowed = self.__forbidCheesyEffects != 0
        if wasAllowed != isAllowed:
            for av in Avatar.Avatar.ActiveAvatars:
                if hasattr(av, 'reconsiderCheesyEffect'):
                    av.reconsiderCheesyEffect()

            toonbase.localToon.reconsiderCheesyEffect()

    def areCheesyEffectsAllowed(self):
        return self.__forbidCheesyEffects == 0

    def refreshAccountServerDate(self, forceRefresh=0):
        try:
            self.accountServerDate.grabDate(force=forceRefresh)
        except TTAccount.TTAccountException, e:
            self.notify.debug(str(e))
            return 1

    def getCreditCardUpFront(self):
        if not hasattr(toonbase, 'creditCardUpFront'):
            return self.accountServerConstants.getBool('creditCardUpFront')
        return toonbase.creditCardUpFront != 0