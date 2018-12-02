import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class GraphicsChannel(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

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

    def getClassType():
        returnValue = libpanda._inPO9cYkR3A()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_makeLayer_ptrGraphicsChannel_int(self, index):
        returnValue = libpanda._inPO9cYTgeC(self.this, index)
        import GraphicsLayer
        returnObject = GraphicsLayer.GraphicsLayer(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def __overloaded_makeLayer_ptrGraphicsChannel(self):
        returnValue = libpanda._inPO9cYWEYv(self.this)
        import GraphicsLayer
        returnObject = GraphicsLayer.GraphicsLayer(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getNumLayers(self):
        returnValue = libpanda._inPO9cYpjyB(self.this)
        return returnValue

    def getLayer(self, index):
        returnValue = libpanda._inPO9cYmtbt(self.this, index)
        import GraphicsLayer
        returnObject = GraphicsLayer.GraphicsLayer(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def moveLayer(self, fromIndex, toIndex):
        returnValue = libpanda._inPO9cYAqBQ(self.this, fromIndex, toIndex)
        return returnValue

    def removeLayer(self, index):
        returnValue = libpanda._inPO9cYCgTJ(self.this, index)
        return returnValue

    def getWindow(self):
        returnValue = libpanda._inPO9cYLob5(self.this)
        import GraphicsWindow
        returnObject = GraphicsWindow.GraphicsWindow(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def getPipe(self):
        returnValue = libpanda._inPO9cYknwJ(self.this)
        import GraphicsPipe
        returnObject = GraphicsPipe.GraphicsPipe(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def setActive(self, active):
        returnValue = libpanda._inPO9cYvvNq(self.this, active)
        return returnValue

    def isActive(self):
        returnValue = libpanda._inPO9cYtMTC(self.this)
        return returnValue

    def makeLayer(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_makeLayer_ptrGraphicsChannel()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return self.__overloaded_makeLayer_ptrGraphicsChannel_int(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '