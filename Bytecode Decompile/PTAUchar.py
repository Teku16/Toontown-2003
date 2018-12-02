import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PointerToBaseRefCountObjvectorunsignedchar

class PTAUchar(PointerToBaseRefCountObjvectorunsignedchar.PointerToBaseRefCountObjvectorunsignedchar, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaexpress._inPJoxtPkXb()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPTAUchar(self, copy):
        self.this = libpandaexpress._inPJoxt5Txu(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_unsignedint_unsignedchar(self, n, value):
        self.this = libpandaexpress._inPJoxtSmv9(n, value)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxtdEYV:
            libpandaexpress._inPJoxtdEYV(self.this)

    def emptyArray(n):
        returnValue = libpandaexpress._inPJoxt26ks(n)
        returnObject = PTAUchar(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    emptyArray = staticmethod(emptyArray)

    def size(self):
        returnValue = libpandaexpress._inPJoxtZxGV(self.this)
        return returnValue

    def pushBack(self, x):
        returnValue = libpandaexpress._inPJoxtxVTf(self.this, x)
        return returnValue

    def popBack(self):
        returnValue = libpandaexpress._inPJoxty2Bp(self.this)
        return returnValue

    def makeEmpty(self):
        returnValue = libpandaexpress._inPJoxt0Lkk(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], PTAUchar):
                    return self.__overloaded_constructor_ptrConstPTAUchar(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <PTAUchar> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_unsignedint_unsignedchar(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '