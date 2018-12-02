import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, ReferenceCount

class BaseParticleRenderer(ReferenceCount.ReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]
    PRALPHAUSER = 3
    PRALPHAIN = 2
    PRALPHAOUT = 1
    PRNOTINITIALIZEDYET = 4
    PRALPHANONE = 0
    PPNOBLEND = 0
    PPBLENDCUBIC = 2
    PPBLENDLINEAR = 1

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

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAcZ5b:
            libpandaphysics._inPKBUAcZ5b(self.this)

    def getRenderNode(self):
        returnValue = libpandaphysics._inPKBUAnoTT(self.this)
        import GeomNode
        returnObject = GeomNode.GeomNode(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def setAlphaMode(self, am):
        returnValue = libpandaphysics._inPKBUArp5w(self.this, am)
        return returnValue

    def getAlphaMode(self):
        returnValue = libpandaphysics._inPKBUAdz17(self.this)
        return returnValue

    def setUserAlpha(self, ua):
        returnValue = libpandaphysics._inPKBUAmPHY(self.this, ua)
        return returnValue

    def getUserAlpha(self):
        returnValue = libpandaphysics._inPKBUAl2V9(self.this)
        return returnValue