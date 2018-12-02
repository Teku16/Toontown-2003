from ShowBaseGlobal import *
from ToontownMsgTypes import *
import DirectNotifyGlobal, LoginBase, TTAccount

class LoginTTAccount(LoginBase.LoginBase, TTAccount.TTAccount):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginTTAcct')

    def supportsRelogin(self):
        return 1

    def sendLoginMsg(self):
        tcr = self.tcr
        datagram = Datagram()
        datagram.addUint16(CLIENT_LOGIN_2)
        self.__addPlayToken(datagram)
        datagram.addString(tcr.serverVersion)
        datagram.addUint32(tcr.hashVal)
        self.__addTokenType(datagram)
        tcr.send(datagram)

    def resendPlayToken(self):
        tcr = self.tcr
        datagram = Datagram()
        datagram.addUint16(CLIENT_SET_SECURITY)
        self.__addPlayToken(datagram)
        self.__addTokenType(datagram)
        tcr.send(datagram)

    def __addPlayToken(self, datagram):
        self.playToken = self.playToken.strip()
        datagram.addString(self.playToken)

    def __addTokenType(self, datagram):
        if self.playTokenIsEncrypted:
            datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)
        else:
            datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)

    def getErrorCode(self):
        return self.response.getInt('errorCode', 0)

    def needToSetParentPassword(self):
        return self.response.getBool('secretsPasswordNotSet', 0)