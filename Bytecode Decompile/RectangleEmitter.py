import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, BaseParticleEmitter

class RectangleEmitter(BaseParticleEmitter.BaseParticleEmitter, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inPKBUAqyrE()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstRectangleEmitter(self, copy):
        self.this = libpandaphysics._inPKBUAiSSt(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAg60H:
            libpandaphysics._inPKBUAg60H(self.this)

    def setMinBound(self, vmin):
        returnValue = libpandaphysics._inPKBUA8_w9(self.this, vmin.this)
        return returnValue

    def setMaxBound(self, vmax):
        returnValue = libpandaphysics._inPKBUAE18N(self.this, vmax.this)
        return returnValue

    def getMinBound(self):
        returnValue = libpandaphysics._inPKBUANaOf(self.this)
        import Point2
        returnObject = Point2.Point2(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getMaxBound(self):
        returnValue = libpandaphysics._inPKBUAUbav(self.this)
        import Point2
        returnObject = Point2.Point2(None)
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
                if isinstance(_args[0], RectangleEmitter):
                    return self.__overloaded_constructor_ptrConstRectangleEmitter(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <RectangleEmitter> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '