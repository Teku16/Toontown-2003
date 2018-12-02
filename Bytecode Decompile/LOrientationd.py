import types, libpanda, libpandaDowncasts, FFIExternalObject, QuatD

class LOrientationd(QuatD.QuatD, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN33Y6p()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLMatrix3d(self, parameter0):
        self.this = libpanda._inPUZN3Yrfb(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLMatrix4d(self, parameter0):
        self.this = libpanda._inPUZN3Grmp(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLQuaterniond(self, parameter0):
        self.this = libpanda._inPUZN3QFe9(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVector3d_float(self, parameter0, parameter1):
        self.this = libpanda._inPUZN3zi3y(parameter0.this, parameter1)
        self.userManagesMemory = 1

    def __overloaded_constructor_double_double_double_double(self, parameter0, parameter1, parameter2, parameter3):
        self.this = libpanda._inPUZN3QOxM(parameter0, parameter1, parameter2, parameter3)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3c2Kq:
            libpanda._inPUZN3c2Kq(self.this)

    def getClassType():
        returnValue = libpanda._inPUZN3wK29()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded___mul___ptrConstLOrientationd_ptrConstLOrientationd(self, other):
        returnValue = libpanda._inPUZN3HPvB(self.this, other.this)
        returnObject = LOrientationd(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___mul___ptrConstLOrientationd_ptrConstLQuaterniond(self, other):
        returnValue = libpanda._inPUZN3lgBQ(self.this, other.this)
        returnObject = LOrientationd(None)
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
            if numArgs == 1:
                import QuatD, Mat4D, Mat3D
                if isinstance(_args[0], QuatD.QuatD):
                    return self.__overloaded_constructor_ptrConstLQuaterniond(_args[0])
                else:
                    if isinstance(_args[0], Mat4D.Mat4D):
                        return self.__overloaded_constructor_ptrConstLMatrix4d(_args[0])
                    else:
                        if isinstance(_args[0], Mat3D.Mat3D):
                            return self.__overloaded_constructor_ptrConstLMatrix3d(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <QuatD.QuatD> <Mat4D.Mat4D> <Mat3D.Mat3D> '
            else:
                if numArgs == 2:
                    import Vec3D
                    if isinstance(_args[0], Vec3D.Vec3D):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_ptrConstLVector3d_float(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Vec3D.Vec3D> '
                else:
                    if numArgs == 4:
                        if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                        return self.__overloaded_constructor_double_double_double_double(_args[0], _args[1], _args[2], _args[3])
                                    else:
                                        raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 4 '

    def __mul__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import QuatD
            if isinstance(_args[0], QuatD.QuatD):
                return self.__overloaded___mul___ptrConstLOrientationd_ptrConstLQuaterniond(_args[0])
            else:
                if isinstance(_args[0], LOrientationd):
                    return self.__overloaded___mul___ptrConstLOrientationd_ptrConstLOrientationd(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <QuatD.QuatD> <LOrientationd> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '