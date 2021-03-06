import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, BaseParticleEmitter

class SphereVolumeEmitter(BaseParticleEmitter.BaseParticleEmitter, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inPKBUAvu67()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstSphereVolumeEmitter(self, copy):
        self.this = libpandaphysics._inPKBUA4FjC(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAg60H:
            libpandaphysics._inPKBUAg60H(self.this)

    def setRadius(self, r):
        returnValue = libpandaphysics._inPKBUAjvji(self.this, r)
        return returnValue

    def getRadius(self):
        returnValue = libpandaphysics._inPKBUACKpS(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], SphereVolumeEmitter):
                    return self.__overloaded_constructor_ptrConstSphereVolumeEmitter(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <SphereVolumeEmitter> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '