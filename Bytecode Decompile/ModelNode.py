import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PandaNode

class ModelNode(PandaNode.PandaNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]
    PTNet = 2
    PTLocal = 1
    PTNone = 0

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyoUtdT(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyoQ7l3:
            libpanda._inPkJyoQ7l3(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyobGvp()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setPreserveTransform(self, preserveTransform):
        returnValue = libpanda._inPkJyocAt4(self.this, preserveTransform)
        return returnValue

    def getPreserveTransform(self):
        returnValue = libpanda._inPkJyoEjAF(self.this)
        return returnValue