import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LerpFunctor

class SimpleLerpFunctorLPoint4f(LerpFunctor.LerpFunctor, FFIExternalObject.FFIExternalObject):
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
        returnValue = libpanda._inPgRdz_52c()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def interpolate(self, parameter1):
        returnValue = libpanda._inPgRdzWC1I(self.this, parameter1)
        import Point4
        returnObject = Point4.Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getStart(self):
        returnValue = libpanda._inPgRdzGIBB(self.this)
        import Point4
        returnObject = Point4.Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getEnd(self):
        returnValue = libpanda._inPgRdzpFm7(self.this)
        import Point4
        returnObject = Point4.Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return