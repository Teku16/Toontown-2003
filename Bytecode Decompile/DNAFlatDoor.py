import types, libtoontown, libtoontownDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, DNADoor

class DNAFlatDoor(DNADoor.DNADoor, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libtoontownDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstDNAFlatDoor(self, door):
        self.this = libtoontown._inPet4yn_L2(door.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, initialName):
        self.this = libtoontown._inPet4yd2xd(initialName)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libtoontown._inPet4y3kUU()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libtoontown and libtoontown._inPet4yD0kH:
            libtoontown._inPet4yD0kH(self.this)

    def getClassType():
        returnValue = libtoontown._inPet4ywULa()
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
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], DNAFlatDoor):
                        return self.__overloaded_constructor_ptrConstDNAFlatDoor(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <DNAFlatDoor> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '