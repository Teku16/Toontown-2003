import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase3

class Vec3(VBase3.VBase3, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3gACr()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase3f(self, copy):
        self.this = libpanda._inPUZN3Z8LN(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, fillValue):
        self.this = libpanda._inPUZN36OMJ(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float(self, x, y, z):
        self.this = libpanda._inPUZN3hp6I(x, y, z)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3BySw:
            libpanda._inPUZN3BySw(self.this)

    def zero():
        returnValue = libpanda._inPUZN3Pixn()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3xo58()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3xExB()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def unitZ():
        returnValue = libpanda._inPUZN3xgqG()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitZ = staticmethod(unitZ)

    def __overloaded_up___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3kOZo(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_up___enum__CoordinateSystem = staticmethod(__overloaded_up___enum__CoordinateSystem)

    def __overloaded_up():
        returnValue = libpanda._inPUZN3z_MF()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_up = staticmethod(__overloaded_up)

    def __overloaded_right___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3osup(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_right___enum__CoordinateSystem = staticmethod(__overloaded_right___enum__CoordinateSystem)

    def __overloaded_right():
        returnValue = libpanda._inPUZN3ZM3h()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_right = staticmethod(__overloaded_right)

    def __overloaded_forward___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3k621(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_forward___enum__CoordinateSystem = staticmethod(__overloaded_forward___enum__CoordinateSystem)

    def __overloaded_forward():
        returnValue = libpanda._inPUZN3nQbv()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_forward = staticmethod(__overloaded_forward)

    def __overloaded_down___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN35s4e(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_down___enum__CoordinateSystem = staticmethod(__overloaded_down___enum__CoordinateSystem)

    def __overloaded_down():
        returnValue = libpanda._inPUZN3iBqg()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_down = staticmethod(__overloaded_down)

    def __overloaded_left___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3vT2J(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_left___enum__CoordinateSystem = staticmethod(__overloaded_left___enum__CoordinateSystem)

    def __overloaded_left():
        returnValue = libpanda._inPUZN31_pL()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_left = staticmethod(__overloaded_left)

    def __overloaded_back___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3_Pd_(cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_back___enum__CoordinateSystem = staticmethod(__overloaded_back___enum__CoordinateSystem)

    def __overloaded_back():
        returnValue = libpanda._inPUZN3UzPA()
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_back = staticmethod(__overloaded_back)

    def __overloaded_rfu_float_float_float___enum__CoordinateSystem(right, fwd, up, cs):
        returnValue = libpanda._inPUZN3hSqR(right, fwd, up, cs)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_rfu_float_float_float___enum__CoordinateSystem = staticmethod(__overloaded_rfu_float_float_float___enum__CoordinateSystem)

    def __overloaded_rfu_float_float_float(right, fwd, up):
        returnValue = libpanda._inPUZN3UW9c(right, fwd, up)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_rfu_float_float_float = staticmethod(__overloaded_rfu_float_float_float)

    def getClassType():
        returnValue = libpanda._inPUZN3g4QZ()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLVector3f_ptrConstLVecBase3f(self, copy):
        returnValue = libpanda._inPUZN3qZGE(self.this, copy.this)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLVector3f_float(self, fillValue):
        returnValue = libpanda._inPUZN3R_QE(self.this, fillValue)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector3f(self):
        returnValue = libpanda._inPUZN3WstI(self.this)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector3f_ptrConstLVecBase3f(self, other):
        returnValue = libpanda._inPUZN32o44(self.this, other.this)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector3f_ptrConstLVector3f(self, other):
        returnValue = libpanda._inPUZN38f3H(self.this, other.this)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector3f_ptrConstLVecBase3f(self, other):
        returnValue = libpanda._inPUZN3WrR4(self.this, other.this)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector3f_ptrConstLVector3f(self, other):
        returnValue = libpanda._inPUZN3ciQH(self.this, other.this)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def length(self):
        returnValue = libpanda._inPUZN3jiIl(self.this)
        return returnValue

    def lengthSquared(self):
        returnValue = libpanda._inPUZN3CMHA(self.this)
        return returnValue

    def normalize(self):
        returnValue = libpanda._inPUZN3vAzt(self.this)
        return returnValue

    def cross(self, other):
        returnValue = libpanda._inPUZN3WSXn(self.this, other.this)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN3cvTb(self.this, scalar)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3sH0c(self.this, scalar)
        returnObject = Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def down(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_down()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_down___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    down = staticmethod(down)

    def right(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_right()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_right___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    right = staticmethod(right)

    def rfu(*_args):
        numArgs = len(_args)
        if numArgs == 3:
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                    if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                        return Vec3.__overloaded_rfu_float_float_float(_args[0], _args[1], _args[2])
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
                            if isinstance(_args[3], types.IntType):
                                return Vec3.__overloaded_rfu_float_float_float___enum__CoordinateSystem(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <types.IntType> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 3 4 '

    rfu = staticmethod(rfu)

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                import VBase3
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], VBase3.VBase3):
                        return self.__overloaded_constructor_ptrConstLVecBase3f(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase3.VBase3> '
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
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 3 '

    def forward(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_forward()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_forward___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    forward = staticmethod(forward)

    def left(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_left()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_left___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    left = staticmethod(left)

    def back(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_back()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_back___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    back = staticmethod(back)

    def up(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Vec3.__overloaded_up()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Vec3.__overloaded_up___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    up = staticmethod(up)

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLVector3f()
        else:
            if numArgs == 1:
                import VBase3
                if isinstance(_args[0], VBase3.VBase3):
                    return self.__overloaded___sub___ptrConstLVector3f_ptrConstLVecBase3f(_args[0])
                else:
                    if isinstance(_args[0], Vec3):
                        return self.__overloaded___sub___ptrConstLVector3f_ptrConstLVector3f(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <VBase3.VBase3> <Vec3> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase3
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLVector3f_float(_args[0])
            else:
                if isinstance(_args[0], VBase3.VBase3):
                    return self.__overloaded_assign_ptrLVector3f_ptrConstLVecBase3f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase3.VBase3> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase3
            if isinstance(_args[0], VBase3.VBase3):
                return self.__overloaded___add___ptrConstLVector3f_ptrConstLVecBase3f(_args[0])
            else:
                if isinstance(_args[0], Vec3):
                    return self.__overloaded___add___ptrConstLVector3f_ptrConstLVector3f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase3.VBase3> <Vec3> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '