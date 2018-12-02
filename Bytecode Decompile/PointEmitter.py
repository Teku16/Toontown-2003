import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, BaseParticleEmitter

class PointEmitter(BaseParticleEmitter.BaseParticleEmitter, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inPKBUAtVW_()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPointEmitter(self, copy):
        self.this = libpandaphysics._inPKBUAhKUT(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAg60H:
            libpandaphysics._inPKBUAg60H(self.this)

    def setLocation(self, p):
        returnValue = libpandaphysics._inPKBUALDeR(self.this, p.this)
        return returnValue

    def getLocation(self):
        returnValue = libpandaphysics._inPKBUAHUJU(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], PointEmitter):
                    return self.__overloaded_constructor_ptrConstPointEmitter(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <PointEmitter> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '