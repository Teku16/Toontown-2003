import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase3

class Point3(VBase3.VBase3, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3z3Qe()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase3f(self, copy):
        self.this = libpanda._inPUZN3b_6E(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, fillValue):
        self.this = libpanda._inPUZN3CO2W(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float(self, x, y, z):
        self.this = libpanda._inPUZN3Nxu6(x, y, z)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3eGrD:
            libpanda._inPUZN3eGrD(self.this)

    def zero():
        returnValue = libpanda._inPUZN3lu74()
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3CPkF()
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3aeuF()
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def unitZ():
        returnValue = libpanda._inPUZN3Sp3F()
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitZ = staticmethod(unitZ)

    def __overloaded_origin___enum__CoordinateSystem(cs):
        returnValue = libpanda._inPUZN3VRyH(cs)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_origin___enum__CoordinateSystem = staticmethod(__overloaded_origin___enum__CoordinateSystem)

    def __overloaded_origin():
        returnValue = libpanda._inPUZN3P16_()
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_origin = staticmethod(__overloaded_origin)

    def __overloaded_rfu_float_float_float___enum__CoordinateSystem(right, fwd, up, cs):
        returnValue = libpanda._inPUZN3laIy(right, fwd, up, cs)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_rfu_float_float_float___enum__CoordinateSystem = staticmethod(__overloaded_rfu_float_float_float___enum__CoordinateSystem)

    def __overloaded_rfu_float_float_float(right, fwd, up):
        returnValue = libpanda._inPUZN33tjk(right, fwd, up)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_rfu_float_float_float = staticmethod(__overloaded_rfu_float_float_float)

    def getClassType():
        returnValue = libpanda._inPUZN3nkbU()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLPoint3f_ptrConstLVecBase3f(self, copy):
        returnValue = libpanda._inPUZN3J6xP(self.this, copy.this)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLPoint3f_float(self, fillValue):
        returnValue = libpanda._inPUZN3qkxL(self.this, fillValue)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint3f(self):
        returnValue = libpanda._inPUZN30M7V(self.this)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint3f_ptrConstLPoint3f(self, other):
        returnValue = libpanda._inPUZN3SFwU(self.this, other.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint3f_ptrConstLVecBase3f(self, other):
        returnValue = libpanda._inPUZN3ALZx(self.this, other.this)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint3f_ptrConstLVector3f(self, other):
        returnValue = libpanda._inPUZN3fn3J(self.this, other.this)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint3f_ptrConstLVecBase3f(self, other):
        returnValue = libpanda._inPUZN3_4Xx(self.this, other.this)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint3f_ptrConstLVector3f(self, other):
        returnValue = libpanda._inPUZN3g12J(self.this, other.this)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def cross(self, other):
        returnValue = libpanda._inPUZN32m20(self.this, other.this)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN3VCf8(self.this, scalar)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3rOic(self.this, scalar)
        returnObject = Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def origin(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return Point3.__overloaded_origin()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.IntType):
                    return Point3.__overloaded_origin___enum__CoordinateSystem(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    origin = staticmethod(origin)

    def rfu(*_args):
        numArgs = len(_args)
        if numArgs == 3:
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                    if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                        return Point3.__overloaded_rfu_float_float_float(_args[0], _args[1], _args[2])
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
                                return Point3.__overloaded_rfu_float_float_float___enum__CoordinateSystem(_args[0], _args[1], _args[2], _args[3])
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

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLPoint3f()
        else:
            if numArgs == 1:
                import VBase3, Vec3
                if isinstance(_args[0], VBase3.VBase3):
                    return self.__overloaded___sub___ptrConstLPoint3f_ptrConstLVecBase3f(_args[0])
                else:
                    if isinstance(_args[0], Vec3.Vec3):
                        return self.__overloaded___sub___ptrConstLPoint3f_ptrConstLVector3f(_args[0])
                    else:
                        if isinstance(_args[0], Point3):
                            return self.__overloaded___sub___ptrConstLPoint3f_ptrConstLPoint3f(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <VBase3.VBase3> <Vec3.Vec3> <Point3> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase3
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLPoint3f_float(_args[0])
            else:
                if isinstance(_args[0], VBase3.VBase3):
                    return self.__overloaded_assign_ptrLPoint3f_ptrConstLVecBase3f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase3.VBase3> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase3, Vec3
            if isinstance(_args[0], VBase3.VBase3):
                return self.__overloaded___add___ptrConstLPoint3f_ptrConstLVecBase3f(_args[0])
            else:
                if isinstance(_args[0], Vec3.Vec3):
                    return self.__overloaded___add___ptrConstLPoint3f_ptrConstLVector3f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase3.VBase3> <Vec3.Vec3> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '