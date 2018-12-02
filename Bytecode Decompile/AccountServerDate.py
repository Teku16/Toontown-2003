from ShowBaseGlobal import *
from HTTPUtil import *
import DirectNotifyGlobal, TTAccount, DateObject, TTDateObject, time

class AccountServerDate:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('AccountServerDate')

    def __init__(self):
        self.__grabbed = 0

    def getServer(self):
        return TTAccount.getAccountServer().cStr()

    def grabDate(self, force=0):
        if self.__grabbed and not force:
            self.notify.debug('using cached account server date')
            return
        if toonbase.tcr.accountOldAuth or base.config.GetBool('use-local-date', 0):
            self.__useLocalClock()
            return
        url = URLSpec(self.getServer())
        url.setPath('/getDate.php')
        self.notify.debug('grabbing account server date from %s' % url.cStr())
        response = getHTTPResponse(url)
        if response[0] != 'ACCOUNT SERVER DATE':
            self.notify.debug('invalid response header')
            raise UnexpectedResponse, 'unexpected response, response=%s' % response
        try:
            epoch = int(response[1])
        except ValueError, e:
            self.notify.debug(str(e))
            raise UnexpectedResponse, 'unexpected response, response=%s' % response

        timeTuple = time.gmtime(epoch)
        self.year = timeTuple[0]
        self.month = timeTuple[1]
        self.day = timeTuple[2]
        toonbase.tcr.dateObject = TTDateObject.TTDateObject(self)
        self.__grabbed = 1

    def __useLocalClock(self):
        self.month = toonbase.tcr.dateObject.getMonth()
        self.year = toonbase.tcr.dateObject.getYear()
        self.day = toonbase.tcr.dateObject.getDay()

    def getMonth(self):
        return self.month

    def getYear(self):
        return self.year

    def getDay(self):
        return self.day