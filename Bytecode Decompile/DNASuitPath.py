import types, libtoontown, libtoontownDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class DNASuitPath(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libtoontownDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libtoontown._inPet4yvZAe()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstDNASuitPath(self, path):
        self.this = libtoontown._inPet4y6m9i(path.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libtoontown and libtoontown._inPet4y3tdl:
            libtoontown._inPet4y3tdl(self.this)

    def getClassType():
        returnValue = libtoontown._inPet4yiaRl()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getNumPoints(self):
        returnValue = libtoontown._inPet4ysfvS(self.this)
        return returnValue

    def copy(self, path):
        returnValue = libtoontown._inPet4ygz46(self.this, path.this)
        return returnValue

    def getPointIndex(self, i):
        returnValue = libtoontown._inPet4yzh4X(self.this, i)
        return returnValue

    def output(self, out):
        returnValue = libtoontown._inPet4yPK18(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], DNASuitPath):
                    return self.__overloaded_constructor_ptrConstDNASuitPath(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <DNASuitPath> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '