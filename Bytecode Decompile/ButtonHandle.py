import types, libpanda, libpandaDowncasts, FFIExternalObject

class ButtonHandle(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpanda._inPelbo40bO()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPelbowcFL:
            libpanda._inPelbowcFL(self.this)

    def none():
        returnValue = libpanda._inPelboXMlV()
        returnObject = ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    none = staticmethod(none)

    def getName(self):
        returnValue = libpanda._inPelbopq06(self.this)
        return returnValue

    def hasAsciiEquivalent(self):
        returnValue = libpanda._inPelbo2_MD(self.this)
        return returnValue

    def getAsciiEquivalent(self):
        returnValue = libpanda._inPelbovhsY(self.this)
        return returnValue

    def getIndex(self):
        returnValue = libpanda._inPelbolajp(self.this)
        return returnValue

    def output(self, out):
        returnValue = libpanda._inPelbo7vL2(self.this, out.this)
        return returnValue