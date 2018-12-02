import types, libpandaphysics, libpandaphysicsDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, BaseParticleEmitter

class LineEmitter(BaseParticleEmitter.BaseParticleEmitter, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaphysics._inPKBUAnO71()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLineEmitter(self, copy):
        self.this = libpandaphysics._inPKBUAsJIy(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaphysics and libpandaphysics._inPKBUAg60H:
            libpandaphysics._inPKBUAg60H(self.this)

    def setEndpoint1(self, point):
        returnValue = libpandaphysics._inPKBUAkFGJ(self.this, point.this)
        return returnValue

    def setEndpoint2(self, point):
        returnValue = libpandaphysics._inPKBUAEBtJ(self.this, point.this)
        return returnValue

    def getEndpoint1(self):
        returnValue = libpandaphysics._inPKBUA9l0h(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getEndpoint2(self):
        returnValue = libpandaphysics._inPKBUAdobi(self.this)
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
                if isinstance(_args[0], LineEmitter):
                    return self.__overloaded_constructor_ptrConstLineEmitter(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <LineEmitter> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '