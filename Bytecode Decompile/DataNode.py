import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PandaNode

class DataNode(PandaNode.PandaNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPSLSecRQs(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPSLSelsRt:
            libpanda._inPSLSelsRt(self.this)

    def getClassType():
        returnValue = libpanda._inPSLSePSzN()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def writeInputs(self, out):
        returnValue = libpanda._inPSLSe4fqQ(self.this, out.this)
        return returnValue

    def writeOutputs(self, out):
        returnValue = libpanda._inPSLSeVk5z(self.this, out.this)
        return returnValue

    def writeConnections(self, out):
        returnValue = libpanda._inPSLSeXqT4(self.this, out.this)
        return returnValue