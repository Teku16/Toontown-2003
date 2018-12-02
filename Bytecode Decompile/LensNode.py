import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PandaNode

class LensNode(PandaNode.PandaNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyoZGLe(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyo10eB:
            libpanda._inPkJyo10eB(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyoF6_K()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def copyLens(self, lens):
        returnValue = libpanda._inPkJyo1vNW(self.this, lens.this)
        return returnValue

    def setLens(self, lens):
        returnValue = libpanda._inPkJyo_2fA(self.this, lens.this)
        return returnValue

    def getLens(self):
        returnValue = libpanda._inPkJyoC5Ow(self.this)
        import Lens
        returnObject = Lens.Lens(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def isInView(self, pos):
        returnValue = libpanda._inPkJyoVo66(self.this, pos.this)
        return returnValue