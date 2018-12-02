import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, CollisionHandlerPhysical

class CollisionHandlerFloor(CollisionHandlerPhysical.CollisionHandlerPhysical, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpanda._inPHwca2EUx()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPHwcaT4lv:
            libpanda._inPHwcaT4lv(self.this)

    def getClassType():
        returnValue = libpanda._inPHwcaGYw3()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setOffset(self, offset):
        returnValue = libpanda._inPHwca2NQk(self.this, offset)
        return returnValue

    def getOffset(self):
        returnValue = libpanda._inPHwcaB9Un(self.this)
        return returnValue

    def setMaxVelocity(self, maxVel):
        returnValue = libpanda._inPHwca4LRc(self.this, maxVel)
        return returnValue

    def getMaxVelocity(self):
        returnValue = libpanda._inPHwcaT6Z5(self.this)
        return returnValue