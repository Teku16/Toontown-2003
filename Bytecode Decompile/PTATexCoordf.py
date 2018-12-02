import types, libpanda, libpandaDowncasts, FFIExternalObject, PointerToBaseRefCountObjvectorLPoint2f

class PTATexCoordf(PointerToBaseRefCountObjvectorLPoint2f.PointerToBaseRefCountObjvectorLPoint2f, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPUZN3Z1EP()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPTATexCoordf(self, copy):
        self.this = libpanda._inPUZN3UgWz(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_unsignedint_ptrConstLPoint2f(self, n, value):
        self.this = libpanda._inPUZN3sNOf(n, value.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPUZN35MGs:
            libpanda._inPUZN35MGs(self.this)

    def emptyArray(n):
        returnValue = libpanda._inPUZN3uJr3(n)
        returnObject = PTATexCoordf(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    emptyArray = staticmethod(emptyArray)

    def size(self):
        returnValue = libpanda._inPUZN3DO_L(self.this)
        return returnValue

    def pushBack(self, x):
        returnValue = libpanda._inPUZN3YTFP(self.this, x.this)
        return returnValue

    def popBack(self):
        returnValue = libpanda._inPUZN3pi7V(self.this)
        return returnValue

    def makeEmpty(self):
        returnValue = libpanda._inPUZN3k0tT(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], PTATexCoordf):
                    return self.__overloaded_constructor_ptrConstPTATexCoordf(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <PTATexCoordf> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.IntType):
                        import Point2
                        if isinstance(_args[1], Point2.Point2):
                            return self.__overloaded_constructor_unsignedint_ptrConstLPoint2f(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <Point2.Point2> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '