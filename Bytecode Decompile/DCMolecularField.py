import types, libdirect, libdirectDowncasts, FFIExternalObject, DCField

class DCMolecularField(DCField.DCField, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libdirectDowncasts]

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
        if libdirect and libdirect._inP5HfQY378:
            libdirect._inP5HfQY378(self.this)

    def getNumAtomics(self):
        returnValue = libdirect._inP5HfQ9TYG(self.this)
        return returnValue

    def getAtomic(self, n):
        returnValue = libdirect._inP5HfQKxjf(self.this, n)
        import DCAtomicField
        returnObject = DCAtomicField.DCAtomicField(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return