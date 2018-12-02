import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, BaseParticleEmitter

class BoxEmitter(BaseParticleEmitter.BaseParticleEmitter, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inPKBUAlwIq()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstBoxEmitter(self, copy):
        self.this = libpandaphysics._inPKBUA42fc(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAg60H:
            libpandaphysics._inPKBUAg60H(self.this)

    def setMinBound(self, vmin):
        returnValue = libpandaphysics._inPKBUAYUdv(self.this, vmin.this)
        return returnValue

    def setMaxBound(self, vmax):
        returnValue = libpandaphysics._inPKBUAhptT(self.this, vmax.this)
        return returnValue

    def getMinBound(self):
        returnValue = libpandaphysics._inPKBUAufR4(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getMaxBound(self):
        returnValue = libpandaphysics._inPKBUAgZgc(self.this)
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
                if isinstance(_args[0], BoxEmitter):
                    return self.__overloaded_constructor_ptrConstBoxEmitter(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <BoxEmitter> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '