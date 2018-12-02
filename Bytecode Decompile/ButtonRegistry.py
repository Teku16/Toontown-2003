import types, libpanda, libpandaDowncasts, FFIExternalObject

class ButtonRegistry(FFIExternalObject.FFIExternalObject):
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
        if libpanda and libpanda._inPelbo3pmE:
            libpanda._inPelbo3pmE(self.this)

    def ptr():
        returnValue = libpanda._inPelbodgyc()
        returnObject = ButtonRegistry(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    ptr = staticmethod(ptr)

    def getButton(self, name):
        returnValue = libpanda._inPelboLZsi(self.this, name)
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def findAsciiButton(self, asciiEquivalent):
        returnValue = libpanda._inPelbovc8u(self.this, asciiEquivalent)
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return