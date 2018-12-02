import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase4

class Point4(VBase4.VBase4, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN30UXk()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase4f(self, copy):
        self.this = libpanda._inPUZN3RD57(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, fillValue):
        self.this = libpanda._inPUZN3Cj8c(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float_float(self, x, y, z, w):
        self.this = libpanda._inPUZN3zr8M(x, y, z, w)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3R5Hh:
            libpanda._inPUZN3R5Hh(self.this)

    def zero():
        returnValue = libpanda._inPUZN3l1J6()
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3C0yG()
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3aH8G()
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def unitZ():
        returnValue = libpanda._inPUZN3SWGH()
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitZ = staticmethod(unitZ)

    def unitW():
        returnValue = libpanda._inPUZN3KloG()
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitW = staticmethod(unitW)

    def getClassType():
        returnValue = libpanda._inPUZN3nbpV()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLPoint4f_ptrConstLVecBase4f(self, copy):
        returnValue = libpanda._inPUZN3bZBR(self.this, copy.this)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLPoint4f_float(self, fillValue):
        returnValue = libpanda._inPUZN3qdAN(self.this, fillValue)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint4f(self):
        returnValue = libpanda._inPUZN30LJX(self.this)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint4f_ptrConstLPoint4f(self, other):
        returnValue = libpanda._inPUZN3MM2G(self.this, other.this)
        import Vec4
        returnObject = Vec4.Vec4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint4f_ptrConstLVecBase4f(self, other):
        returnValue = libpanda._inPUZN3Supy(self.this, other.this)
        import VBase4
        returnObject = VBase4.VBase4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint4f_ptrConstLVector4f(self, other):
        returnValue = libpanda._inPUZN3WbFn(self.this, other.this)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint4f_ptrConstLVecBase4f(self, other):
        returnValue = libpanda._inPUZN3Jcoy(self.this, other.this)
        import VBase4
        returnObject = VBase4.VBase4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint4f_ptrConstLVector4f(self, other):
        returnValue = libpanda._inPUZN3ppEn(self.this, other.this)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN3Vdt9(self.this, scalar)
        returnObject = Point4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3rXwd(self.this, scalar)
        returnObject = Point4(None)
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
                import VBase4
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], VBase4.VBase4):
                        return self.__overloaded_constructor_ptrConstLVecBase4f(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase4.VBase4> '
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
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 4 '

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLPoint4f()
        else:
            if numArgs == 1:
                import VBase4, Vec4
                if isinstance(_args[0], VBase4.VBase4):
                    return self.__overloaded___sub___ptrConstLPoint4f_ptrConstLVecBase4f(_args[0])
                else:
                    if isinstance(_args[0], Vec4.Vec4):
                        return self.__overloaded___sub___ptrConstLPoint4f_ptrConstLVector4f(_args[0])
                    else:
                        if isinstance(_args[0], Point4):
                            return self.__overloaded___sub___ptrConstLPoint4f_ptrConstLPoint4f(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <VBase4.VBase4> <Vec4.Vec4> <Point4> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase4
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLPoint4f_float(_args[0])
            else:
                if isinstance(_args[0], VBase4.VBase4):
                    return self.__overloaded_assign_ptrLPoint4f_ptrConstLVecBase4f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase4.VBase4> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase4, Vec4
            if isinstance(_args[0], VBase4.VBase4):
                return self.__overloaded___add___ptrConstLPoint4f_ptrConstLVecBase4f(_args[0])
            else:
                if isinstance(_args[0], Vec4.Vec4):
                    return self.__overloaded___add___ptrConstLPoint4f_ptrConstLVector4f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase4.VBase4> <Vec4.Vec4> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '