import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class GraphicsLayer(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
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
        returnValue = libpanda._inPO9cYBdnF()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_makeDisplayRegion_ptrGraphicsLayer(self):
        returnValue = libpanda._inPO9cYiC1O(self.this)
        import DisplayRegion
        returnObject = DisplayRegion.DisplayRegion(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded_makeDisplayRegion_ptrGraphicsLayer_float_float_float_float(self, l, r, b, t):
        returnValue = libpanda._inPO9cY9q23(self.this, l, r, b, t)
        import DisplayRegion
        returnObject = DisplayRegion.DisplayRegion(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getNumDrs(self):
        returnValue = libpanda._inPO9cYi79D(self.this)
        return returnValue

    def getDr(self, index):
        returnValue = libpanda._inPO9cY3RO1(self.this, index)
        import DisplayRegion
        returnObject = DisplayRegion.DisplayRegion(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded_removeDr_ptrGraphicsLayer_ptrDisplayRegion(self, displayRegion):
        returnValue = libpanda._inPO9cY7u5p(self.this, displayRegion.this)
        return returnValue

    def __overloaded_removeDr_ptrGraphicsLayer_int(self, index):
        returnValue = libpanda._inPO9cYOWCB(self.this, index)
        return returnValue

    def getChannel(self):
        returnValue = libpanda._inPO9cYbKvA(self.this)
        import GraphicsChannel
        returnObject = GraphicsChannel.GraphicsChannel(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def getWindow(self):
        returnValue = libpanda._inPO9cYz_Xk(self.this)
        import GraphicsWindow
        returnObject = GraphicsWindow.GraphicsWindow(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def getPipe(self):
        returnValue = libpanda._inPO9cYE9wO(self.this)
        import GraphicsPipe
        returnObject = GraphicsPipe.GraphicsPipe(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def setActive(self, active):
        returnValue = libpanda._inPO9cY_hJu(self.this, active)
        return returnValue

    def isActive(self):
        returnValue = libpanda._inPO9cYVCvw(self.this)
        return returnValue

    def makeDisplayRegion(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_makeDisplayRegion_ptrGraphicsLayer()
        else:
            if numArgs == 4:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                return self.__overloaded_makeDisplayRegion_ptrGraphicsLayer_float_float_float_float(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 4 '

    def removeDr(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import DisplayRegion
            if isinstance(_args[0], types.IntType):
                return self.__overloaded_removeDr_ptrGraphicsLayer_int(_args[0])
            else:
                if isinstance(_args[0], DisplayRegion.DisplayRegion):
                    return self.__overloaded_removeDr_ptrGraphicsLayer_ptrDisplayRegion(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> <DisplayRegion.DisplayRegion> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '