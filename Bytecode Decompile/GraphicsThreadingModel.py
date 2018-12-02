import types, libpanda, libpandaDowncasts, FFIExternalObject

class GraphicsThreadingModel(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstGraphicsThreadingModel(self, copy):
        self.this = libpanda._inPO9cYzJOi(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, model):
        self.this = libpanda._inPO9cYtG_c(model)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpanda._inPO9cYIBJ_()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPO9cYnBW6:
            libpanda._inPO9cYnBW6(self.this)

    def assign(self, copy):
        returnValue = libpanda._inPO9cYGZxc(self.this, copy.this)
        returnObject = GraphicsThreadingModel(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getModel(self):
        returnValue = libpanda._inPO9cY6c0w(self.this)
        return returnValue

    def getCullName(self):
        returnValue = libpanda._inPO9cY9GWk(self.this)
        return returnValue

    def getDrawName(self):
        returnValue = libpanda._inPO9cYmbag(self.this)
        return returnValue

    def getCullSorting(self):
        returnValue = libpanda._inPO9cYwVRl(self.this)
        return returnValue

    def isSingleThreaded(self):
        returnValue = libpanda._inPO9cYzsdw(self.this)
        return returnValue

    def isDefault(self):
        returnValue = libpanda._inPO9cYKNCv(self.this)
        return returnValue

    def output(self, out):
        returnValue = libpanda._inPO9cYolSI(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], GraphicsThreadingModel):
                        return self.__overloaded_constructor_ptrConstGraphicsThreadingModel(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <GraphicsThreadingModel> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '