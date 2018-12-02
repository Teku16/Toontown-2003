import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LinearRandomForce

class LinearJitterForce(LinearRandomForce.LinearRandomForce, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstLinearJitterForce(self, copy):
        self.this = libpandaphysics._inP9fJJWcP8(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_bool(self, a, m):
        self.this = libpandaphysics._inP9fJJzEEl(a, m)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, a):
        self.this = libpandaphysics._inP9fJJkctU(a)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inP9fJJF51r()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpandaphysics._inP9fJJDAAU()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], LinearJitterForce):
                        return self.__overloaded_constructor_ptrConstLinearJitterForce(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <LinearJitterForce> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_float_bool(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '