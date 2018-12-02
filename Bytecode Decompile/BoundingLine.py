import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, GeometricBoundingVolume

class BoundingLine(GeometricBoundingVolume.GeometricBoundingVolume, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPSkjPGsL1()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f_ptrConstLPoint3f(self, a, b):
        self.this = libpanda._inPSkjPAR_R(a.this, b.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPSkjPnAIV:
            libpanda._inPSkjPnAIV(self.this)

    def getClassType():
        returnValue = libpanda._inPSkjPlcUv()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getPointA(self):
        returnValue = libpanda._inPSkjPQIF_(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getPointB(self):
        returnValue = libpanda._inPSkjPJ2G_(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 2:
                import Point3
                if isinstance(_args[0], Point3.Point3):
                    import Point3
                    if isinstance(_args[1], Point3.Point3):
                        return self.__overloaded_constructor_ptrConstLPoint3f_ptrConstLPoint3f(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Point3.Point3> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 2 '