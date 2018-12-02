from ShowBaseGlobal import *
from ToontownMsgTypes import *
import DirectNotifyGlobal, LoginBase

class LoginGoAccount(LoginBase.LoginBase):
    __module__ = __name__

    def __init__(self, tcr):
        LoginBase.LoginBase.__init__(self, tcr)

    def createAccount(self, loginName, password, data):
        return 'Unsupported'

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.password = password
        return None
        return

    def supportsRelogin(self):
        return 0

    def sendLoginMsg(self):
        tcr = self.tcr
        datagram = Datagram()
        datagram.addUint16(CLIENT_LOGIN_2)
        datagram.addString(self.password)
        datagram.addString(tcr.serverVersion)
        datagram.addUint32(tcr.hashVal)
        self.__addTokenType(datagram)
        tcr.send(datagram)

    def resendPlayToken(self):
        return

    def requestPwdReminder(self, email=None, acctName=None):
        return 0

    def getAccountData(self, loginName, password):
        return 'Unsupported'

    def supportsParentPassword(self):
        return 0

    def authenticateParentPassword(self, loginName, password, parentPassword):
        return (
         0, None)
        return

    def supportsAuthenticateDelete(self):
        return 0

    def enableSecretFriends(self, loginName, password, parentPassword, enable=1):
        return (
         0, None)
        return

    def __addTokenType(self, datagram):
        datagram.addInt32(CLIENT_LOGIN_2_BLUE)