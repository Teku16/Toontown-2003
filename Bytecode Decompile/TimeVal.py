import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class TimeVal(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpandaexpress._inPJoxtZzSC()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxtSqaJ:
            libpandaexpress._inPJoxtSqaJ(self.this)

    def getSec(self):
        returnValue = libpandaexpress._inPJoxt2ZxR(self.this)
        return returnValue

    def getUsec(self):
        returnValue = libpandaexpress._inPJoxtblc7(self.this)
        return returnValue