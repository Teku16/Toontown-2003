import types, libpanda, libpandaDowncasts, FFIExternalObject

class QueuedReturnNetDatagram(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        raise RuntimeError, 'No C++ constructor defined for class: ' + self.__class__.__name__

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def setMaxQueueSize(self, maxSize):
        returnValue = libpanda._inP9ImMSCal(self.this, maxSize)
        return returnValue

    def getMaxQueueSize(self):
        returnValue = libpanda._inP9ImM2D9N(self.this)
        return returnValue

    def getCurrentQueueSize(self):
        returnValue = libpanda._inP9ImM4Ce3(self.this)
        return returnValue