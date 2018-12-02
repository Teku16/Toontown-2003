import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedWritableReferenceCount

class RenderAttrib(TypedWritableReferenceCount.TypedWritableReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]
    MLessEqual = 4
    MGreaterEqual = 7
    MNone = 0
    MGreater = 5
    MEqual = 3
    MLess = 2
    MNever = 1
    MNotEqual = 6
    MAlways = 8

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

    def getClassType():
        returnValue = libpanda._inPkJyoLWjP()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def output(self, out):
        returnValue = libpanda._inPkJyooTLC(self.this, out.this)
        return returnValue

    def write(self, out, indentLevel):
        returnValue = libpanda._inPkJyodBRS(self.this, out.this, indentLevel)
        return returnValue