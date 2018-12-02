import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, RenderEffect

class CompassEffect(RenderEffect.RenderEffect, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]
    PSz = 64
    PScale = 112
    PSx = 16
    PY = 2
    PAll = 127
    PSy = 32
    PZ = 4
    PX = 1
    PRot = 8
    PPos = 7

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
        if libpanda and libpanda._inPkJyoP6Wp:
            libpanda._inPkJyoP6Wp(self.this)

    def __overloaded_make_ptrConstNodePath_int(reference, properties):
        returnValue = libpanda._inPkJyo2e7i(reference.this, properties)
        import RenderEffect
        returnObject = RenderEffect.RenderEffect(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make_ptrConstNodePath_int = staticmethod(__overloaded_make_ptrConstNodePath_int)

    def __overloaded_make_ptrConstNodePath(reference):
        returnValue = libpanda._inPkJyoo3bC(reference.this)
        import RenderEffect
        returnObject = RenderEffect.RenderEffect(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    __overloaded_make_ptrConstNodePath = staticmethod(__overloaded_make_ptrConstNodePath)

    def getClassType():
        returnValue = libpanda._inPkJyoeHvU()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getReference(self):
        returnValue = libpanda._inPkJyo_Dfu(self.this)
        import NodePath
        returnObject = NodePath.NodePath(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getProperties(self):
        returnValue = libpanda._inPkJyoNQdF(self.this)
        return returnValue

    def make(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            import NodePath
            if isinstance(_args[0], NodePath.NodePath):
                return CompassEffect.__overloaded_make_ptrConstNodePath(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
        else:
            if numArgs == 2:
                import NodePath
                if isinstance(_args[0], NodePath.NodePath):
                    if isinstance(_args[1], types.IntType):
                        return CompassEffect.__overloaded_make_ptrConstNodePath_int(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    make = staticmethod(make)