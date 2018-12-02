import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class ClientBase(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

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

    def getClassType():
        returnValue = libpanda._inPOfOPXw0P()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def forkAsynchronousThread(self, pollTime):
        returnValue = libpanda._inPOfOP_6xH(self.this, pollTime)
        return returnValue

    def isForked(self):
        returnValue = libpanda._inPOfOPpe_A(self.this)
        return returnValue

    def poll(self):
        returnValue = libpanda._inPOfOP0HyU(self.this)
        return returnValue

    def getLastPollTime(self):
        returnValue = libpanda._inPOfOPlkN3(self.this)
        return returnValue

    def setCoordinateSystem(self, cs):
        returnValue = libpanda._inPOfOPGNkp(self.this, cs)
        return returnValue

    def getCoordinateSystem(self):
        returnValue = libpanda._inPOfOPxXH8(self.this)
        return returnValue