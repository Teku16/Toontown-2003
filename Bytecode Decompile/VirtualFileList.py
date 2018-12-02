import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, ReferenceCount

class VirtualFileList(ReferenceCount.ReferenceCount, FFIExternalObject.FFIExternalObject):
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
        if libpandaexpress and libpandaexpress._inPJoxtO1DS:
            libpandaexpress._inPJoxtO1DS(self.this)

    def getNumFiles(self):
        returnValue = libpandaexpress._inPJoxtqGsI(self.this)
        return returnValue

    def getFile(self, n):
        returnValue = libpandaexpress._inPJoxt3Wno(self.this, n)
        import VirtualFile
        returnObject = VirtualFile.VirtualFile(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return