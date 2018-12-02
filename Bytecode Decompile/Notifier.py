from LoggerGlobal import *
import PythonUtil, time

class Notifier:
    __module__ = __name__
    serverDelta = 0

    def __init__(self, name, logger=None):
        self.__name = name
        if logger == None:
            self.__logger = defaultLogger
        else:
            self.__logger = logger
        self.__info = 1
        self.__warning = 1
        self.__debug = 0
        self.__logging = 0
        return

    def setServerDelta(self, delta, timezone):
        delta = int(round(delta))
        Notifier.serverDelta = delta + time.timezone - timezone
        import NotifyCategory
        NotifyCategory.NotifyCategory.setServerDelta(self.serverDelta)
        self.info('Notify clock adjusted by %s (and timezone adjusted by %s hours) to synchronize with server.' % (PythonUtil.formatElapsedSeconds(delta), (time.timezone - timezone) / 3600))

    def getTime(self):
        return time.strftime(':%m-%d-%Y %H:%M:%S ', time.localtime(time.time() + self.serverDelta))

    def __str__(self):
        return '%s: info = %d, warning = %d, debug = %d, logging = %d' % (self.__name, self.__info, self.__warning, self.__debug, self.__logging)

    def setSeverity(self, severity):
        import NotifySeverity
        if severity >= NotifySeverity.NSError:
            self.setWarning(0)
            self.setInfo(0)
            self.setDebug(0)
        else:
            if severity == NotifySeverity.NSWarning:
                self.setWarning(1)
                self.setInfo(0)
                self.setDebug(0)
            else:
                if severity == NotifySeverity.NSInfo:
                    self.setWarning(1)
                    self.setInfo(1)
                    self.setDebug(0)
                else:
                    if severity <= NotifySeverity.NSDebug:
                        self.setWarning(1)
                        self.setInfo(1)
                        self.setDebug(1)

    def getSeverity(self):
        import NotifySeverity
        if self.getDebug():
            return NotifySeverity.NSDebug
        else:
            if self.getInfo():
                return NotifySeverity.NSInfo
            else:
                if self.getWarning():
                    return NotifySeverity.NSWarning
                else:
                    return NotifySeverity.NSError

    def error(self, errorString, exception=StandardError):
        string = self.getTime() + str(exception) + ': ' + self.__name + ': ' + errorString
        self.__log(string)
        raise exception(errorString)

    def warning(self, warningString):
        if self.__warning:
            string = self.getTime() + self.__name + '(warning): ' + warningString
            self.__log(string)
            self.__print(string)
        return 1

    def setWarning(self, bool):
        self.__warning = bool

    def getWarning(self):
        return self.__warning

    def debug(self, debugString):
        if self.__debug:
            string = self.getTime() + self.__name + '(debug): ' + debugString
            self.__log(string)
            self.__print(string)
        return 1

    def setDebug(self, bool):
        self.__debug = bool

    def getDebug(self):
        return self.__debug

    def info(self, infoString):
        if self.__info:
            string = self.getTime() + self.__name + '(info): ' + infoString
            self.__log(string)
            self.__print(string)
        return 1

    def getInfo(self):
        return self.__info

    def setInfo(self, bool):
        self.__info = bool

    def __log(self, logEntry):
        if self.__logging:
            self.__logger.log(logEntry)

    def getLogging(self):
        return self.__logging

    def setLogging(self, bool):
        self.__logging = bool

    def __print(self, string):
        print string