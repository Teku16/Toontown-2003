import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LinearForce

class LinearVectorForce(LinearForce.LinearForce, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstLVector3f_float_bool(self, vec, a, mass):
        self.this = libpandaphysics._inP9fJJn_HH(vec.this, a, mass)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVector3f_float(self, vec, a):
        self.this = libpandaphysics._inP9fJJ5pxV(vec.this, a)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVector3f(self, vec):
        self.this = libpandaphysics._inP9fJJ41f6(vec.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLinearVectorForce(self, copy):
        self.this = libpandaphysics._inP9fJJ2TTR(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float_float_bool(self, x, y, z, a, mass):
        self.this = libpandaphysics._inP9fJJ_9B9(x, y, z, a, mass)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float_float(self, x, y, z, a):
        self.this = libpandaphysics._inP9fJJyxk3(x, y, z, a)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float(self, x, y, z):
        self.this = libpandaphysics._inP9fJJpPZK(x, y, z)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float(self, x, y):
        self.this = libpandaphysics._inP9fJJQ8n5(x, y)
        self.userManagesMemory = 1

    def __overloaded_constructor_float(self, x):
        self.this = libpandaphysics._inP9fJJ1Z3E(x)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inP9fJJnFAc()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpandaphysics._inP9fJJlzdJ()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_setVector_ptrLinearVectorForce_ptrConstLVector3f(self, v):
        returnValue = libpandaphysics._inP9fJJkk_l(self.this, v.this)
        return returnValue

    def __overloaded_setVector_ptrLinearVectorForce_float_float_float(self, x, y, z):
        returnValue = libpandaphysics._inP9fJJSGyt(self.this, x, y, z)
        return returnValue

    def getLocalVector(self):
        returnValue = libpandaphysics._inP9fJJN4vu(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
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
                import Vec3
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_float(_args[0])
                else:
                    if isinstance(_args[0], Vec3.Vec3):
                        return self.__overloaded_constructor_ptrConstLVector3f(_args[0])
                    else:
                        if isinstance(_args[0], LinearVectorForce):
                            return self.__overloaded_constructor_ptrConstLinearVectorForce(_args[0])
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <Vec3.Vec3> <LinearVectorForce> '
            else:
                if numArgs == 2:
                    import Vec3
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_float_float(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        if isinstance(_args[0], Vec3.Vec3):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                return self.__overloaded_constructor_ptrConstLVector3f_float(_args[0], _args[1])
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <Vec3.Vec3> '
                else:
                    if numArgs == 3:
                        import Vec3
                        if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    return self.__overloaded_constructor_float_float_float(_args[0], _args[1], _args[2])
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                        else:
                            if isinstance(_args[0], Vec3.Vec3):
                                if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                    if isinstance(_args[2], types.IntType):
                                        return self.__overloaded_constructor_ptrConstLVector3f_float_bool(_args[0], _args[1], _args[2])
                                    else:
                                        raise TypeError, 'Invalid argument 2, expected one of: <types.IntType> '
                                else:
                                    raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <Vec3.Vec3> '
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
                            if numArgs == 5:
                                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                            if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                                if isinstance(_args[4], types.IntType):
                                                    return self.__overloaded_constructor_float_float_float_float_bool(_args[0], _args[1], _args[2], _args[3], _args[4])
                                                else:
                                                    raise TypeError, 'Invalid argument 4, expected one of: <types.IntType> '
                                            else:
                                                raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                        else:
                                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                                    else:
                                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 3 4 5 '

    def setVector(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Vec3
            if isinstance(_args[0], Vec3.Vec3):
                return self.__overloaded_setVector_ptrLinearVectorForce_ptrConstLVector3f(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Vec3.Vec3> '
        else:
            if numArgs == 3:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            return self.__overloaded_setVector_ptrLinearVectorForce_float_float_float(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 3 '