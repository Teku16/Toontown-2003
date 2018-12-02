import types, libdirect, libdirectDowncasts, FFIExternalObject

class CIntervalManager(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libdirectDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libdirect._inPSpsC6SV3()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libdirect and libdirect._inPSpsCuhMu:
            libdirect._inPSpsCuhMu(self.this)

    def getGlobalPtr():
        returnValue = libdirect._inPSpsCQP38()
        returnObject = CIntervalManager(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    getGlobalPtr = staticmethod(getGlobalPtr)

    def setEventQueue(self, eventQueue):
        returnValue = libdirect._inPSpsCI947(self.this, eventQueue.this)
        return returnValue

    def getEventQueue(self):
        returnValue = libdirect._inPSpsC7ah3(self.this)
        import EventQueue
        returnObject = EventQueue.EventQueue(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def addCInterval(self, interval, external):
        returnValue = libdirect._inPSpsCyh7A(self.this, interval.this, external)
        return returnValue

    def findCInterval(self, name):
        returnValue = libdirect._inPSpsCH0H3(self.this, name)
        return returnValue

    def getCInterval(self, index):
        returnValue = libdirect._inPSpsCnvsF(self.this, index)
        import CInterval
        returnObject = CInterval.CInterval(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def removeCInterval(self, index):
        returnValue = libdirect._inPSpsCOxys(self.this, index)
        return returnValue

    def interrupt(self):
        returnValue = libdirect._inPSpsCwZTK(self.this)
        return returnValue

    def getNumIntervals(self):
        returnValue = libdirect._inPSpsCW9zD(self.this)
        return returnValue

    def getMaxIndex(self):
        returnValue = libdirect._inPSpsCrnjb(self.this)
        return returnValue

    def step(self):
        returnValue = libdirect._inPSpsCiQ_p(self.this)
        return returnValue

    def getNextEvent(self):
        returnValue = libdirect._inPSpsCjEV_(self.this)
        return returnValue

    def getNextRemoval(self):
        returnValue = libdirect._inPSpsCyDVA(self.this)
        return returnValue

    def output(self, out):
        returnValue = libdirect._inPSpsCJ5QE(self.this, out.this)
        return returnValue

    def write(self, out):
        returnValue = libdirect._inPSpsCzWze(self.this, out.this)
        return returnValue