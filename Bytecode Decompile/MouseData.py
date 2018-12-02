import types, libpanda, libpandaDowncasts, FFIExternalObject

class MouseData(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPelbogWcW()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstMouseData(self, copy):
        self.this = libpanda._inPelboga_u(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPelboAm_W:
            libpanda._inPelboAm_W(self.this)

    def assign(self, copy):
        returnValue = libpanda._inPelboptbu(self.this, copy.this)
        returnObject = MouseData(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getX(self):
        returnValue = libpanda._inPelboQo5w(self.this)
        return returnValue

    def getY(self):
        returnValue = libpanda._inPelboo4Dx(self.this)
        return returnValue

    def getInWindow(self):
        returnValue = libpanda._inPelbo370X(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], MouseData):
                    return self.__overloaded_constructor_ptrConstMouseData(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <MouseData> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '