import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LinearForce

class LinearFrictionForce(LinearForce.LinearForce, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstLinearFrictionForce(self, copy):
        self.this = libpandaphysics._inP9fJJs_V5(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_bool(self, coef, a, m):
        self.this = libpandaphysics._inP9fJJyAho(coef, a, m)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float(self, coef, a):
        self.this = libpandaphysics._inP9fJJegK3(coef, a)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, coef):
        self.this = libpandaphysics._inP9fJJZk3b(coef)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inP9fJJurU5()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpandaphysics._inP9fJJ_un1()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setCoef(self, coef):
        returnValue = libpandaphysics._inP9fJJ5iox(self.this, coef)
        return returnValue

    def getCoef(self):
        returnValue = libpandaphysics._inP9fJJPTwt(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], LinearFrictionForce):
                        return self.__overloaded_constructor_ptrConstLinearFrictionForce(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <LinearFrictionForce> '
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
                    if numArgs == 3:
                        if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.IntType):
                                    return self.__overloaded_constructor_float_float_bool(_args[0], _args[1], _args[2])
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <types.IntType> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 3 '