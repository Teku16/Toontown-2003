import types, libpanda, libpandaDowncasts, FFIExternalObject, VBase2D

class Point2D(VBase2D.VBase2D, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3tKnR()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase2d(self, copy):
        self.this = libpanda._inPUZN3kCZP(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_double(self, fillValue):
        self.this = libpanda._inPUZN308Ro(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_double_double(self, x, y):
        self.this = libpanda._inPUZN3VLaV(x, y)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3_CIK:
            libpanda._inPUZN3_CIK(self.this)

    def zero():
        returnValue = libpanda._inPUZN3qnmp()
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3BGP2()
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3ZRZ2()
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def getClassType():
        returnValue = libpanda._inPUZN3mtGF()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLPoint2d_ptrConstLVecBase2d(self, copy):
        returnValue = libpanda._inPUZN38M99(self.this, copy.this)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLPoint2d_double(self, fillValue):
        returnValue = libpanda._inPUZN3MH4I(self.this, fillValue)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint2d(self):
        returnValue = libpanda._inPUZN311lG(self.this)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint2d_ptrConstLPoint2d(self, other):
        returnValue = libpanda._inPUZN3NGic(self.this, other.this)
        import Vec2D
        returnObject = Vec2D.Vec2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint2d_ptrConstLVecBase2d(self, other):
        returnValue = libpanda._inPUZN30Vlf(self.this, other.this)
        import VBase2D
        returnObject = VBase2D.VBase2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLPoint2d_ptrConstLVector2d(self, other):
        returnValue = libpanda._inPUZN3Fode(self.this, other.this)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint2d_ptrConstLVecBase2d(self, other):
        returnValue = libpanda._inPUZN3vLkf(self.this, other.this)
        import VBase2D
        returnObject = VBase2D.VBase2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___add___ptrConstLPoint2d_ptrConstLVector2d(self, other):
        returnValue = libpanda._inPUZN3Cmce(self.this, other.this)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN3rAiF(self.this, scalar)
        returnObject = Point2D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN39Vkl(self.this, scalar)
        returnObject = Point2D(None)
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
                import VBase2D
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_double(_args[0])
                else:
                    if isinstance(_args[0], VBase2D.VBase2D):
                        return self.__overloaded_constructor_ptrConstLVecBase2d(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase2D.VBase2D> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_double_double(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLPoint2d()
        else:
            if numArgs == 1:
                import VBase2D, Vec2D
                if isinstance(_args[0], VBase2D.VBase2D):
                    return self.__overloaded___sub___ptrConstLPoint2d_ptrConstLVecBase2d(_args[0])
                else:
                    if isinstance(_args[0], Vec2D.Vec2D):
                        return self.__overloaded___sub___ptrConstLPoint2d_ptrConstLVector2d(_args[0])
                    else:
                        if isinstance(_args[0], Point2D):
                            return self.__overloaded___sub___ptrConstLPoint2d_ptrConstLPoint2d(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <VBase2D.VBase2D> <Vec2D.Vec2D> <Point2D> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase2D
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLPoint2d_double(_args[0])
            else:
                if isinstance(_args[0], VBase2D.VBase2D):
                    return self.__overloaded_assign_ptrLPoint2d_ptrConstLVecBase2d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase2D.VBase2D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __add__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase2D, Vec2D
            if isinstance(_args[0], VBase2D.VBase2D):
                return self.__overloaded___add___ptrConstLPoint2d_ptrConstLVecBase2d(_args[0])
            else:
                if isinstance(_args[0], Vec2D.Vec2D):
                    return self.__overloaded___add___ptrConstLPoint2d_ptrConstLVector2d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase2D.VBase2D> <Vec2D.Vec2D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '