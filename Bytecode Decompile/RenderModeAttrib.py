import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, RenderAttrib

class RenderModeAttrib(RenderAttrib.RenderAttrib, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]
    MFilled = 0
    MWireframe = 1

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
        if libpanda and libpanda._inPkJyoDu_B:
            libpanda._inPkJyoDu_B(self.this)

    def __overloaded_make___enum__Mode_float(mode, lineWidth):
        returnValue = libpanda._inPkJyo_VB1(mode, lineWidth)
        import RenderAttrib
        returnObject = RenderAttrib.RenderAttrib(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make___enum__Mode_float = staticmethod(__overloaded_make___enum__Mode_float)

    def __overloaded_make___enum__Mode(mode):
        returnValue = libpanda._inPkJyo6BMo(mode)
        import RenderAttrib
        returnObject = RenderAttrib.RenderAttrib(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make___enum__Mode = staticmethod(__overloaded_make___enum__Mode)

    def getClassType():
        returnValue = libpanda._inPkJyoM0p3()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getMode(self):
        returnValue = libpanda._inPkJyoFaf_(self.this)
        return returnValue

    def getLineWidth(self):
        returnValue = libpanda._inPkJyoVxaK(self.this)
        return returnValue

    def make(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.IntType):
                return RenderModeAttrib.__overloaded_make___enum__Mode(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return RenderModeAttrib.__overloaded_make___enum__Mode_float(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    make = staticmethod(make)