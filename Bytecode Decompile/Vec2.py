import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase2

class Vec2(VBase2.VBase2, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3Tv_8()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase2f(self, copy):
        self.this = libpanda._inPUZN3_wFf(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, fillValue):
        self.this = libpanda._inPUZN3tvIb(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float(self, x, y):
        self.this = libpanda._inPUZN3Ps00(x, y)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3C7Pp:
            libpanda._inPUZN3C7Pp(self.this)

    def zero():
        returnValue = libpanda._inPUZN3MCtA()
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3yI1V()
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3ykua()
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def getClassType():
        returnValue = libpanda._inPUZN3gYMy()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLVector2f_ptrConstLVecBase2f(self, copy):
        returnValue = libpanda._inPUZN3rg1b(self.this, copy.this)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLVector2f_float(self, fillValue):
        returnValue = libpanda._inPUZN3OfPd(self.this, fillValue)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector2f(self):
        returnValue = libpanda._inPUZN3WMph(self.this)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector2f_ptrConstLVecBase2f(self, other):
        returnValue = libpanda._inPUZN3pPmQ(self.this, other.this)
        import VBase2
        returnObject = VBase2.VBase2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVector2f_ptrConstLVector2f(self, other):
        returnValue = libpanda._inPUZN3Cbxg(self.this, other.this)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector2f_ptrConstLVecBase2f(self, other):
        returnValue = libpanda._inPUZN3JC_P(self.this, other.this)
        import VBase2
        returnObject = VBase2.VBase2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLVector2f_ptrConstLVector2f(self, other):
        returnValue = libpanda._inPUZN3ifKg(self.this, other.this)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def length(self):
        returnValue = libpanda._inPUZN3iCF_(self.this)
        return returnValue

    def lengthSquared(self):
        returnValue = libpanda._inPUZN3DsDZ(self.this)
        return returnValue

    def normalize(self):
        returnValue = libpanda._inPUZN3ugwG(self.this)
        return returnValue

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN3cPP0(self.this, scalar)
        returnObject = Vec2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3snx1(self.this, scalar)
        returnObject = Vec2(None)
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
                import VBase2
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], VBase2.VBase2):
                        return self.__overloaded_constructor_ptrConstLVecBase2f(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase2.VBase2> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_float_float(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLVector2f()
        else:
            if numArgs == 1:
                import VBase2
                if isinstance(_args[0], VBase2.VBase2):
                    return self.__overloaded___sub___ptrConstLVector2f_ptrConstLVecBase2f(_args[0])
                else:
                    if isinstance(_args[0], Vec2):
                        return self.__overloaded___sub___ptrConstLVector2f_ptrConstLVector2f(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <VBase2.VBase2> <Vec2> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase2
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLVector2f_float(_args[0])
            else:
                if isinstance(_args[0], VBase2.VBase2):
                    return self.__overloaded_assign_ptrLVector2f_ptrConstLVecBase2f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase2.VBase2> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase2
            if isinstance(_args[0], VBase2.VBase2):
                return self.__overloaded___add___ptrConstLVector2f_ptrConstLVecBase2f(_args[0])
            else:
                if isinstance(_args[0], Vec2):
                    return self.__overloaded___add___ptrConstLVector2f_ptrConstLVector2f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase2.VBase2> <Vec2> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '