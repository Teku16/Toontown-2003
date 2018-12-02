import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LightNode

class PointLight(LightNode.LightNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyodSGa(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyoD7C2:
            libpanda._inPkJyoD7C2(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyocV_e()
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
        returnValue = libpanda._inPkJyoVj3W(self.this)
        import VBase4
        returnObject = VBase4.VBase4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setSpecularColor(self, color):
        returnValue = libpanda._inPkJyo9PIn(self.this, color.this)
        return returnValue

    def getAttenuation(self):
        returnValue = libpanda._inPkJyoc4ld(self.this)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setAttenuation(self, attenuation):
        returnValue = libpanda._inPkJyoZO9o(self.this, attenuation.this)
        return returnValue

    def getPoint(self):
        returnValue = libpanda._inPkJyoHjL5(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setPoint(self, point):
        returnValue = libpanda._inPkJyoFPGB(self.this, point.this)
        return returnValue