import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, Istream

class ISocketStream(Istream.Istream, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

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
        if libpandaexpress and libpandaexpress._inP2KOdyeEe:
            libpandaexpress._inP2KOdyeEe(self.this)

    def receiveDatagram(self, dg):
        returnValue = libpandaexpress._inP2KOdabxT(self.this, dg.this)
        return returnValue

    def isClosed(self):
        returnValue = libpandaexpress._inP2KOdTnLp(self.this)
        return returnValue

    def close(self):
        returnValue = libpandaexpress._inP2KOdrVVb(self.this)
        return returnValue