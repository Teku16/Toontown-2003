import types, libpanda, libpandaDowncasts, FFIExternalObject

class NurbsCurveInterface(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        raise RuntimeError, 'No C++ constructor defined for class: ' + self.__class__.__name__

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPHc9WJi5Q:
            libpanda._inPHc9WJi5Q(self.this)

    def getClassType():
        returnValue = libpanda._inPHc9Wmfnq()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def setOrder(self, order):
        returnValue = libpanda._inPHc9WKhK6(self.this, order)
        return returnValue

    def getOrder(self):
        returnValue = libpanda._inPHc9WhPY_(self.this)
        return returnValue

    def getNumCvs(self):
        returnValue = libpanda._inPHc9WWaqD(self.this)
        return returnValue

    def getNumKnots(self):
        returnValue = libpanda._inPHc9WPQ5_(self.this)
        return returnValue

    def insertCv(self, t):
        returnValue = libpanda._inPHc9W8ScU(self.this, t)
        return returnValue

    def __overloaded_appendCv_ptrNurbsCurveInterface_ptrConstLVecBase3f(self, v):
        returnValue = libpanda._inPHc9WpfTi(self.this, v.this)
        return returnValue

    def __overloaded_appendCv_ptrNurbsCurveInterface_ptrConstLVecBase4f(self, v):
        returnValue = libpanda._inPHc9WhMdi(self.this, v.this)
        return returnValue

    def __overloaded_appendCv_ptrNurbsCurveInterface_float_float_float(self, x, y, z):
        returnValue = libpanda._inPHc9WB3ZR(self.this, x, y, z)
        return returnValue

    def removeCv(self, n):
        returnValue = libpanda._inPHc9WpA5o(self.this, n)
        return returnValue

    def removeAllCvs(self):
        returnValue = libpanda._inPHc9W0Nej(self.this)
        return returnValue

    def __overloaded_setCvPoint_ptrNurbsCurveInterface_int_ptrConstLVecBase3f(self, n, v):
        returnValue = libpanda._inPHc9W13Z_(self.this, n, v.this)
        return returnValue

    def __overloaded_setCvPoint_ptrNurbsCurveInterface_int_float_float_float(self, n, x, y, z):
        returnValue = libpanda._inPHc9WvbUc(self.this, n, x, y, z)
        return returnValue

    def getCvPoint(self, n):
        returnValue = libpanda._inPHc9WKFJB(self.this, n)
        import VBase3
        returnObject = VBase3.VBase3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def setCvWeight(self, n, w):
        returnValue = libpanda._inPHc9WkgWd(self.this, n, w)
        return returnValue

    def getCvWeight(self, n):
        returnValue = libpanda._inPHc9WQgDH(self.this, n)
        return returnValue

    def setCv(self, n, v):
        returnValue = libpanda._inPHc9WvLws(self.this, n, v.this)
        return returnValue

    def getCv(self, n):
        returnValue = libpanda._inPHc9W_TRe(self.this, n)
        import VBase4
        returnObject = VBase4.VBase4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def setKnot(self, n, t):
        returnValue = libpanda._inPHc9WCnR8(self.this, n, t)
        return returnValue

    def getKnot(self, n):
        returnValue = libpanda._inPHc9W_MjW(self.this, n)
        return returnValue

    def writeCv(self, out, n):
        returnValue = libpanda._inPHc9W6ybU(self.this, out.this, n)
        return returnValue

    def setCvPoint(self, *_args):
        numArgs = len(_args)
        if numArgs == 2:
            if isinstance(_args[0], types.IntType):
                import VBase3
                if isinstance(_args[1], VBase3.VBase3):
                    return self.__overloaded_setCvPoint_ptrNurbsCurveInterface_int_ptrConstLVecBase3f(_args[0], _args[1])
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <VBase3.VBase3> '
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
        else:
            if numArgs == 4:
                if isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                return self.__overloaded_setCvPoint_ptrNurbsCurveInterface_int_float_float_float(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 2 4 '

    def appendCv(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import VBase4, VBase3
            if isinstance(_args[0], VBase4.VBase4):
                return self.__overloaded_appendCv_ptrNurbsCurveInterface_ptrConstLVecBase4f(_args[0])
            else:
                if isinstance(_args[0], VBase3.VBase3):
                    return self.__overloaded_appendCv_ptrNurbsCurveInterface_ptrConstLVecBase3f(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <VBase4.VBase4> <VBase3.VBase3> '
        else:
            if numArgs == 3:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            return self.__overloaded_appendCv_ptrNurbsCurveInterface_float_float_float(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 3 '