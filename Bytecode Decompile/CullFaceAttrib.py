import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, RenderAttrib

class CullFaceAttrib(RenderAttrib.RenderAttrib, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]
    MCullCounterClockwise = 2
    MCullClockwise = 1
    MCullUnchanged = 3
    MCullNone = 0

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
        if libpanda and libpanda._inPkJyoREpA:
            libpanda._inPkJyoREpA(self.this)

    def __overloaded_make___enum__Mode(mode):
        returnValue = libpanda._inPkJyoIubb(mode)
        import RenderAttrib
        returnObject = RenderAttrib.RenderAttrib(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make___enum__Mode = staticmethod(__overloaded_make___enum__Mode)

    def __overloaded_make():
        returnValue = libpanda._inPkJyo4ry7()
        import RenderAttrib
        returnObject = RenderAttrib.RenderAttrib(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make = staticmethod(__overloaded_make)

    def makeReverse():
        returnValue = libpanda._inPkJyo1_sE()
        import RenderAttrib
        returnObject = RenderAttrib.RenderAttrib(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    makeReverse = staticmethod(makeReverse)

    def getClassType():
        returnValue = libpanda._inPkJyodcRA()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getActualMode(self):
        returnValue = libpanda._inPkJyouw1_(self.this)
        return returnValue

    def getReverse(self):
        returnValue = libpanda._inPkJyom_zu(self.this)
        return returnValue

    def getEffectiveMode(self):
        returnValue = libpanda._inPkJyoC1y1(self.this)
        return returnValue

    def make(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return CullFaceAttrib.__overloaded_make()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return CullFaceAttrib.__overloaded_make___enum__Mode(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    make = staticmethod(make)