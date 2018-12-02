import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, LinearDistanceForce

class LinearSourceForce(LinearDistanceForce.LinearDistanceForce, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inP9fJJ76nW()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float_float_bool(self, p, f, r, a, mass):
        self.this = libpandaphysics._inP9fJJSjwD(p.this, f, r, a, mass)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float_float(self, p, f, r, a):
        self.this = libpandaphysics._inP9fJJPEul(p.this, f, r, a)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float(self, p, f, r):
        self.this = libpandaphysics._inP9fJJmKnZ(p.this, f, r)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLinearSourceForce(self, copy):
        self.this = libpandaphysics._inP9fJJmBjF(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpandaphysics._inP9fJJQ1Mb()
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
                if isinstance(_args[0], LinearSourceForce):
                    return self.__overloaded_constructor_ptrConstLinearSourceForce(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <LinearSourceForce> '
            else:
                if numArgs == 3:
                    import Point3
                    if isinstance(_args[0], Point3.Point3):
                        if isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                return self.__overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float(_args[0], _args[1], _args[2])
                            else:
                                raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
                else:
                    if numArgs == 4:
                        import Point3
                        if isinstance(_args[0], Point3.Point3):
                            if isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                        return self.__overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float_float(_args[0], _args[1], _args[2], _args[3])
                                    else:
                                        raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
                    else:
                        if numArgs == 5:
                            import Point3
                            if isinstance(_args[0], Point3.Point3):
                                if isinstance(_args[1], types.IntType):
                                    if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                        if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                            if isinstance(_args[4], types.IntType):
                                                return self.__overloaded_constructor_ptrConstLPoint3f___enum__FalloffType_float_float_bool(_args[0], _args[1], _args[2], _args[3], _args[4])
                                            else:
                                                raise TypeError, 'Invalid argument 4, expected one of: <types.IntType> '
                                        else:
                                            raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                    else:
                                        raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                            else:
                                raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
                        else:
                            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 3 4 5 '