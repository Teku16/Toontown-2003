import types, libpanda, libpandaDowncasts, FFIExternalObject, Quat

class LRotationf(Quat.Quat, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3yufs()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLMatrix3f(self, parameter0):
        self.this = libpanda._inPUZN3pHWm(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLMatrix4f(self, parameter0):
        self.this = libpanda._inPUZN3pMkn(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLQuaternionf(self, parameter0):
        self.this = libpanda._inPUZN3cC6k(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVector3f_float(self, parameter0, parameter1):
        self.this = libpanda._inPUZN3zssT(parameter0.this, parameter1)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float(self, parameter0, parameter1, parameter2):
        self.this = libpanda._inPUZN3KwNm(parameter0, parameter1, parameter2)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float_float(self, parameter0, parameter1, parameter2, parameter3):
        self.this = libpanda._inPUZN36t_a(parameter0, parameter1, parameter2, parameter3)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3Qd7l:
            libpanda._inPUZN3Qd7l(self.this)

    def getClassType():
        returnValue = libpanda._inPUZN3scCI()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded___mul___ptrConstLRotationf_ptrConstLQuaternionf(self, other):
        returnValue = libpanda._inPUZN3dT59(self.this, other.this)
        import Quat
        returnObject = Quat.Quat(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___mul___ptrConstLRotationf_ptrConstLRotationf(self, other):
        returnValue = libpanda._inPUZN3stc8(self.this, other.this)
        returnObject = LRotationf(None)
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
                import Quat, Mat4, Mat3
                if isinstance(_args[0], Quat.Quat):
                    return self.__overloaded_constructor_ptrConstLQuaternionf(_args[0])
                else:
                    if isinstance(_args[0], Mat4.Mat4):
                        return self.__overloaded_constructor_ptrConstLMatrix4f(_args[0])
                    else:
                        if isinstance(_args[0], Mat3.Mat3):
                            return self.__overloaded_constructor_ptrConstLMatrix3f(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <Quat.Quat> <Mat4.Mat4> <Mat3.Mat3> '
            else:
                if numArgs == 2:
                    import Vec3
                    if isinstance(_args[0], Vec3.Vec3):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_ptrConstLVector3f_float(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Vec3.Vec3> '
                else:
                    if numArgs == 3:
                        if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    return self.__overloaded_constructor_float_float_float(_args[0], _args[1], _args[2])
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                    else:
                        if numArgs == 4:
                            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                                if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                    if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                        if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                            return self.__overloaded_constructor_float_float_float_float(_args[0], _args[1], _args[2], _args[3])
                                        else:
                                            raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                    else:
                                        raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 3 4 '

    def __mul__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Quat
            if isinstance(_args[0], Quat.Quat):
                return self.__overloaded___mul___ptrConstLRotationf_ptrConstLQuaternionf(_args[0])
            else:
                if isinstance(_args[0], LRotationf):
                    return self.__overloaded___mul___ptrConstLRotationf_ptrConstLRotationf(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Quat.Quat> <LRotationf> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '