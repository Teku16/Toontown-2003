import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class Namable(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstNamable(self, copy):
        self.this = libpandaexpress._inPJoxtwaR_(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, initialName):
        self.this = libpandaexpress._inPJoxtYXC2(initialName)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpandaexpress._inPJoxtBFnx()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxtgzYG:
            libpandaexpress._inPJoxtgzYG(self.this)

    def getClassType():
        returnValue = libpandaexpress._inPJoxt4mnx()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def assign(self, other):
        returnValue = libpandaexpress._inPJoxtp1bI(self.this, other.this)
        returnObject = Namable(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setName(self, name):
        returnValue = libpandaexpress._inPJoxtLNBW(self.this, name)
        return returnValue

    def clearName(self):
        returnValue = libpandaexpress._inPJoxtavUl(self.this)
        return returnValue

    def hasName(self):
        returnValue = libpandaexpress._inPJoxtYjhC(self.this)
        return returnValue

    def getName(self):
        returnValue = libpandaexpress._inPJoxtfARN(self.this)
        return returnValue

    def output(self, out):
        returnValue = libpandaexpress._inPJoxtvz7q(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], Namable):
                        return self.__overloaded_constructor_ptrConstNamable(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <Namable> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '