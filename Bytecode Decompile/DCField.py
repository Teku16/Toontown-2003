import types, libdirect, libdirectDowncasts, FFIExternalObject

class DCField(FFIExternalObject.FFIExternalObject):
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
        if libdirect and libdirect._inP5HfQI__K:
            libdirect._inP5HfQI__K(self.this)

    def getNumber(self):
        returnValue = libdirect._inP5HfQfIQq(self.this)
        return returnValue

    def getName(self):
        returnValue = libdirect._inP5HfQhx9a(self.this)
        return returnValue

    def asAtomicField(self):
        returnValue = libdirect._inP5HfQFiDu(self.this)
        import DCAtomicField
        returnObject = DCAtomicField.DCAtomicField(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def asMolecularField(self):
        returnValue = libdirect._inP5HfQvhmz(self.this)
        import DCMolecularField
        returnObject = DCMolecularField.DCMolecularField(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return