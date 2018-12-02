import types, libpanda, libpandaDowncasts, FFIExternalObject

class VBase3D(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3iiry()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVecBase3d(self, copy):
        self.this = libpanda._inPUZN3uakN(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_double(self, fillValue):
        self.this = libpanda._inPUZN3_fFc(fillValue)
        self.userManagesMemory = 1

    def __overloaded_constructor_double_double_double(self, x, y, z):
        self.this = libpanda._inPUZN3occq(x, y, z)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN3wwsX:
            libpanda._inPUZN3wwsX(self.this)

    def zero():
        returnValue = libpanda._inPUZN3trfB()
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    zero = staticmethod(zero)

    def unitX():
        returnValue = libpanda._inPUZN3FxVl()
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitX = staticmethod(unitX)

    def unitY():
        returnValue = libpanda._inPUZN3HxjB()
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitY = staticmethod(unitY)

    def unitZ():
        returnValue = libpanda._inPUZN3Bxxd()
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    unitZ = staticmethod(unitZ)

    def getClassType():
        returnValue = libpanda._inPUZN3zA_x()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_assign_ptrLVecBase3d_ptrConstLVecBase3d(self, copy):
        returnValue = libpanda._inPUZN3yavJ(self.this, copy.this)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrLVecBase3d_double(self, fillValue):
        returnValue = libpanda._inPUZN3_NPY(self.this, fillValue)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___getitem___ptrLVecBase3d_int(self, i):
        returnValue = libpanda._inPUZN3VmHn(self.this, i)
        return returnValue

    def __overloaded___getitem___ptrConstLVecBase3d_int(self, i):
        returnValue = libpanda._inPUZN3IH7D(self.this, i)
        return returnValue

    def isNan(self):
        returnValue = libpanda._inPUZN36uGy(self.this)
        return returnValue

    def getCell(self, i):
        returnValue = libpanda._inPUZN3gqfX(self.this, i)
        return returnValue

    def getX(self):
        returnValue = libpanda._inPUZN38t_C(self.this)
        return returnValue

    def getY(self):
        returnValue = libpanda._inPUZN38J4H(self.this)
        return returnValue

    def getZ(self):
        returnValue = libpanda._inPUZN38lwM(self.this)
        return returnValue

    def setCell(self, i, value):
        returnValue = libpanda._inPUZN3j_Qe(self.this, i, value)
        return returnValue

    def setX(self, value):
        returnValue = libpanda._inPUZN3eZV6(self.this, value)
        return returnValue

    def setY(self, value):
        returnValue = libpanda._inPUZN3e9N_(self.this, value)
        return returnValue

    def setZ(self, value):
        returnValue = libpanda._inPUZN3eBGE(self.this, value)
        return returnValue

    def getData(self):
        returnValue = libpanda._inPUZN3C9D2(self.this)
        return returnValue

    def getNumComponents(self):
        returnValue = libpanda._inPUZN3IxGp(self.this)
        return returnValue

    def fill(self, fillValue):
        returnValue = libpanda._inPUZN3wac_(self.this, fillValue)
        return returnValue

    def set(self, x, y, z):
        returnValue = libpanda._inPUZN3K816(self.this, x, y, z)
        return returnValue

    def dot(self, other):
        returnValue = libpanda._inPUZN37N6j(self.this, other.this)
        return returnValue

    def cross(self, other):
        returnValue = libpanda._inPUZN3vmLU(self.this, other.this)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def lessThan(self, other):
        returnValue = libpanda._inPUZN3c_c1(self.this, other.this)
        return returnValue

    def eq(self, other):
        returnValue = libpanda._inPUZN35E4P(self.this, other.this)
        return returnValue

    def ne(self, other):
        returnValue = libpanda._inPUZN3Fkg_(self.this, other.this)
        return returnValue

    def __overloaded_compareTo_ptrConstLVecBase3d_ptrConstLVecBase3d(self, other):
        returnValue = libpanda._inPUZN3BqT1(self.this, other.this)
        return returnValue

    def __overloaded_compareTo_ptrConstLVecBase3d_ptrConstLVecBase3d_double(self, other, threshold):
        returnValue = libpanda._inPUZN3DVKA(self.this, other.this, threshold)
        return returnValue

    def __overloaded___sub___ptrConstLVecBase3d(self):
        returnValue = libpanda._inPUZN3Ey_f(self.this)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___sub___ptrConstLVecBase3d_ptrConstLVecBase3d(self, other):
        returnValue = libpanda._inPUZN3eG_i(self.this, other.this)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __add__(self, other):
        returnValue = libpanda._inPUZN3Z2dP(self.this, other.this)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __mul__(self, scalar):
        returnValue = libpanda._inPUZN37_m2(self.this, scalar)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __div__(self, scalar):
        returnValue = libpanda._inPUZN3kWdn(self.this, scalar)
        returnObject = VBase3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __iadd__(self, other):
        returnValue = libpanda._inPUZN3bzWw(self.this, other.this)
        return self

    def __isub__(self, other):
        returnValue = libpanda._inPUZN3bD4D(self.this, other.this)
        return self

    def __imul__(self, scalar):
        returnValue = libpanda._inPUZN3KCn2(self.this, scalar)
        return self

    def __idiv__(self, scalar):
        returnValue = libpanda._inPUZN3L6bn(self.this, scalar)
        return self

    def crossInto(self, other):
        returnValue = libpanda._inPUZN3nWqm(self.this, other.this)
        return returnValue

    def __overloaded_almostEqual_ptrConstLVecBase3d_ptrConstLVecBase3d(self, other):
        returnValue = libpanda._inPUZN3gl6W(self.this, other.this)
        return returnValue

    def __overloaded_almostEqual_ptrConstLVecBase3d_ptrConstLVecBase3d_double(self, other, threshold):
        returnValue = libpanda._inPUZN35Cbn(self.this, other.this, threshold)
        return returnValue

    def output(self, out):
        returnValue = libpanda._inPUZN3mBt4(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    return self.__overloaded_constructor_double(_args[0])
                else:
                    if isinstance(_args[0], VBase3D):
                        return self.__overloaded_constructor_ptrConstLVecBase3d(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase3D> '
            else:
                if numArgs == 3:
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                return self.__overloaded_constructor_double_double_double(_args[0], _args[1], _args[2])
                            else:
                                raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 3 '

    def almostEqual(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], VBase3D):
                return self.__overloaded_almostEqual_ptrConstLVecBase3d_ptrConstLVecBase3d(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <VBase3D> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], VBase3D):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return self.__overloaded_almostEqual_ptrConstLVecBase3d_ptrConstLVecBase3d_double(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase3D> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def __sub__(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded___sub___ptrConstLVecBase3d()
        else:
            if numArgs == 1:
                if isinstance(_args[0], VBase3D):
                    return self.__overloaded___sub___ptrConstLVecBase3d_ptrConstLVecBase3d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase3D> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                return self.__overloaded_assign_ptrLVecBase3d_double(_args[0])
            else:
                if isinstance(_args[0], VBase3D):
                    return self.__overloaded_assign_ptrLVecBase3d_ptrConstLVecBase3d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> <VBase3D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def __getitem__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.IntType):
                return self.__overloaded___getitem___ptrConstLVecBase3d_int(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    def compareTo(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], VBase3D):
                return self.__overloaded_compareTo_ptrConstLVecBase3d_ptrConstLVecBase3d(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <VBase3D> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], VBase3D):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return self.__overloaded_compareTo_ptrConstLVecBase3d_ptrConstLVecBase3d_double(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase3D> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '