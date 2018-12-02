import types, libpanda, libpandaDowncasts, FFIExternalObject

class GraphicsPipeSelection(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

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

    def getGlobalPtr():
        returnValue = libpanda._inPO9cYb86m()
        returnObject = GraphicsPipeSelection(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    getGlobalPtr = staticmethod(getGlobalPtr)

    def getNumPipeTypes(self):
        returnValue = libpanda._inPO9cYkGJV(self.this)
        return returnValue

    def getPipeType(self, n):
        returnValue = libpanda._inPO9cYcWon(self.this, n)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def printPipeTypes(self):
        returnValue = libpanda._inPO9cYLhch(self.this)
        return returnValue

    def makePipe(self, type):
        returnValue = libpanda._inPO9cYgtWV(self.this, type.this)
        import GraphicsPipe
        returnObject = GraphicsPipe.GraphicsPipe(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def makeDefaultPipe(self):
        returnValue = libpanda._inPO9cYJlGM(self.this)
        import GraphicsPipe
        returnObject = GraphicsPipe.GraphicsPipe(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getNumAuxModules(self):
        returnValue = libpanda._inPO9cYqQ2r(self.this)
        return returnValue

    def loadAuxModules(self):
        returnValue = libpanda._inPO9cY5_4n(self.this)
        return returnValue