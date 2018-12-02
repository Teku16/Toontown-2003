import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, CollisionHandler

class CollisionHandlerEvent(CollisionHandler.CollisionHandler, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpanda._inPHwcaFTvw()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPHwcaT4lv:
            libpanda._inPHwcaT4lv(self.this)

    def getClassType():
        returnValue = libpanda._inPHwcaXcqn()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setInPattern(self, pattern):
        returnValue = libpanda._inPHwca7Szo(self.this, pattern)
        return returnValue

    def getInPattern(self):
        returnValue = libpanda._inPHwcaKxP0(self.this)
        return returnValue

    def setAgainPattern(self, pattern):
        returnValue = libpanda._inPHwcaHYTx(self.this, pattern)
        return returnValue

    def getAgainPattern(self):
        returnValue = libpanda._inPHwcakEDM(self.this)
        return returnValue

    def setOutPattern(self, pattern):
        returnValue = libpanda._inPHwcakKnm(self.this, pattern)
        return returnValue

    def getOutPattern(self):
        returnValue = libpanda._inPHwca9_5r(self.this)
        return returnValue

    def clear(self):
        returnValue = libpanda._inPHwcavtnS(self.this)
        return returnValue