import types, libdirect, libdirectDowncasts, FFIExternalObject

class Mersenne(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libdirectDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, seed):
        self.this = libdirect._inPL4GTklv3(seed)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libdirect and libdirect._inPL4GTA4FJ:
            libdirect._inPL4GTA4FJ(self.this)

    def getUint31(self):
        returnValue = libdirect._inPL4GTASDv(self.this)
        return returnValue