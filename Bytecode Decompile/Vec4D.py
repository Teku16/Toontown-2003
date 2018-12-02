import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase4D

class Vec4D(VBase4D.VBase4D, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3STkV()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase4d(self, copy):
        self.this = libpanda._inPUZN3ocU1(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_double(self, fillValue):
        self.this = libpanda._inPUZN38AKA(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_double_double_double_double(self, x, y, z, w):
        self.this = libpanda._inPUZN372XI(x, y, z, w)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3d6Oz:
            libpanda._inPUZN3d6Oz(self.this)

    def zero():
        returnValue = libpanda._inPUZN32FUL()
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3vXcg()
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3v7Vl()
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def unitZ():
        returnValue = libpanda._inPUZN3vfNq()
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitZ = staticmethod(unitZ)

    def unitW():
        returnValue = libpanda._inPUZN3ozkb()
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitW = staticmethod(unitW)

    def getClassType():
        returnValue = libpanda._inPUZN3GZz8()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLVector4d_ptrConstLVecBase4d(self, copy):
        returnValue = libpanda._inPUZN3y3xa(self.this, copy.this)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLVector4d_double(self, fillValue):
        returnValue = libpanda._inPUZN3o_A2(self.this, fillValue)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector4d(self):
        returnValue = libpanda._inPUZN3wNQs(self.this)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector4d_ptrConstLVecBase4d(self, other):
        returnValue = libpanda._inPUZN3OQiP(self.this, other.this)
        import VBase4D
        returnObject = VBase4D.VBase4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector4d_ptrConstLVector4d(self, other):
        returnValue = libpanda._inPUZN3AwBp(self.this, other.this)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector4d_ptrConstLVecBase4d(self, other):
        returnValue = libpanda._inPUZN3uV7O(self.this, other.this)
        import VBase4D
        returnObject = VBase4D.VBase4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector4d_ptrConstLVector4d(self, other):
        returnValue = libpanda._inPUZN3g1ao(self.this, other.this)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def length(self):
        returnValue = libpanda._inPUZN3cNsI(self.this)
        return returnValue

    def lengthSquared(self):
        returnValue = libpanda._inPUZN3osqj(self.this)
        return returnValue

    def normalize(self):
        returnValue = libpanda._inPUZN3UhXR(self.this)
        return returnValue

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN39Z8K(self.this, scalar)
        returnObject = Vec4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3twdM(self.this, scalar)
        returnObject = Vec4D(None)
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
                import VBase4D
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_double(_args[0])
                else:
                    if isinstance(_args[0], VBase4D.VBase4D):
                        return self.__overloaded_constructor_ptrConstLVecBase4d(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase4D.VBase4D> '
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
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 4 '

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLVector4d()
        else:
            if numArgs == 1:
                import VBase4D
                if isinstance(_args[0], VBase4D.VBase4D):
                    return self.__overloaded___sub___ptrConstLVector4d_ptrConstLVecBase4d(_args[0])
                else:
                    if isinstance(_args[0], Vec4D):
                        return self.__overloaded___sub___ptrConstLVector4d_ptrConstLVector4d(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <VBase4D.VBase4D> <Vec4D> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase4D
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLVector4d_double(_args[0])
            else:
                if isinstance(_args[0], VBase4D.VBase4D):
                    return self.__overloaded_assign_ptrLVector4d_ptrConstLVecBase4d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase4D.VBase4D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase4D
            if isinstance(_args[0], VBase4D.VBase4D):
                return self.__overloaded___add___ptrConstLVector4d_ptrConstLVecBase4d(_args[0])
            else:
                if isinstance(_args[0], Vec4D):
                    return self.__overloaded___add___ptrConstLVector4d_ptrConstLVector4d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase4D.VBase4D> <Vec4D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '