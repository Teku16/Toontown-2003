from PandaModules import *
import DirectNotifyGlobal, DirectObject, math
NetworkTimeBits = 16
NetworkTimePrecision = 100.0
NetworkTimeMask = (1 << NetworkTimeBits) - 1
NetworkTimeTopBits = 32 - NetworkTimeBits

class ClockDelta(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ClockDelta')

    def __init__(self):
        self.globalClock = ClockObject.getGlobalClock()
        self.delta = 0
        self.accept('resetClock', self.__resetClock)

    def __resetClock(self, timeDelta):
        self.notify.debug('adjusting timebase by %f seconds' % timeDelta)
        self.delta += timeDelta

    def resynchronize(self, localTime, networkTime):
        newDelta = float(localTime) - float(networkTime) / NetworkTimePrecision
        change = newDelta - self.delta
        self.delta = newDelta
        return self.networkToLocalTime(self.localToNetworkTime(change), 0.0)

    def networkToLocalTime(self, networkTime, now=None):
        if now == None:
            now = self.globalClock.getRealTime()
        if self.globalClock.getMode() == ClockObject.MNonRealTime:
            return now
        ntime = int(math.floor((now - self.delta) * NetworkTimePrecision + 0.5))
        diff = self.__signExtend(networkTime - ntime)
        return now + float(diff) / NetworkTimePrecision
        return

    def localToNetworkTime(self, localTime):
        ntime = int(math.floor((localTime - self.delta) * NetworkTimePrecision + 0.5))
        return self.__signExtend(ntime)

    def getRealNetworkTime(self):
        return self.localToNetworkTime(self.globalClock.getRealTime())

    def getFrameNetworkTime(self):
        return self.localToNetworkTime(self.globalClock.getFrameTime())

    def localElapsedTime(self, networkTime):
        now = self.globalClock.getFrameTime()
        dt = now - self.networkToLocalTime(networkTime, now)
        if dt >= 0.0:
            return dt
        else:
            self.notify.debug('negative clock delta: %.3f' % dt)
            return 0.0

    def __signExtend(self, networkTime):
        return (networkTime & NetworkTimeMask) << NetworkTimeTopBits >> NetworkTimeTopBits


globalClockDelta = ClockDelta()