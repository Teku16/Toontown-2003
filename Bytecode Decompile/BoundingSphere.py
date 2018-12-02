import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, FiniteBoundingVolume

class BoundingSphere(FiniteBoundingVolume.FiniteBoundingVolume, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPSkjPqeoF()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f_float(self, center, radius):
        self.this = libpanda._inPSkjPX3ZH(center.this, radius)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPSkjPtO8B:
            libpanda._inPSkjPtO8B(self.this)

    def getClassType():
        returnValue = libpanda._inPSkjPwySa()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getCenter(self):
        returnValue = libpanda._inPSkjPsKph(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getRadius(self):
        returnValue = libpanda._inPSkjPzYsx(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 2:
                import Point3
                if isinstance(_args[0], Point3.Point3):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return self.__overloaded_constructor_ptrConstLPoint3f_float(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 2 '