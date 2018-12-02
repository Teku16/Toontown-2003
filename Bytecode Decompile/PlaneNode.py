import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PandaNode

class PlaneNode(PandaNode.PandaNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyoTudM(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyotRHe:
            libpanda._inPkJyotRHe(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyobjRh()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setPlane(self, planeBase):
        returnValue = libpanda._inPkJyoBb4d(self.this, planeBase.this)
        return returnValue

    def getPlane(self):
        returnValue = libpanda._inPkJyoOSiz(self.this)
        import Plane
        returnObject = Plane.Plane(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return