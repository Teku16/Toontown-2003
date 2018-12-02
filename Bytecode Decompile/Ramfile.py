import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class Ramfile(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpandaexpress._inPJoxtybIp()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxtswrg:
            libpandaexpress._inPJoxtswrg(self.this)

    def readline(self):
        returnValue = libpandaexpress._inPJoxtCYbY(self.this)
        return returnValue

    def readlines(self):
        lines = []
        line = self.readline()
        while line:
            lines.append(line)
            line = self.readline()

        return lines