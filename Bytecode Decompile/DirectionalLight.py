import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LightNode

class DirectionalLight(LightNode.LightNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyoFmND(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyoORYZ:
            libpanda._inPkJyoORYZ(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyov7PH()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getSpecularColor(self):
        returnValue = libpanda._inPkJyoetKC(self.this)
        import VBase4
        returnObject = VBase4.VBase4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setSpecularColor(self, color):
        returnValue = libpanda._inPkJyoCHLU(self.this, color.this)
        return returnValue

    def getPoint(self):
        returnValue = libpanda._inPkJyopsIS(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setPoint(self, point):
        returnValue = libpanda._inPkJyoE91O(self.this, point.this)
        return returnValue

    def getDirection(self):
        returnValue = libpanda._inPkJyoEGi1(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setDirection(self, direction):
        returnValue = libpanda._inPkJyoaGF_(self.this, direction.this)
        return returnValue