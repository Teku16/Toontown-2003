import types, libdirect, libdirectDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, CLerpInterval

class CLerpAnimEffectInterval(CLerpInterval.CLerpInterval, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libdirectDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name, duration, blendType):
        self.this = libdirect._inPSpsCW1mi(name, duration, blendType)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libdirect and libdirect._inPSpsC6vyE:
            libdirect._inPSpsC6vyE(self.this)

    def getClassType():
        returnValue = libdirect._inPSpsCxulU()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def addControl(self, control, name, beginEffect, endEffect):
        returnValue = libdirect._inPSpsCOyvp(self.this, control.this, name, beginEffect, endEffect)
        return returnValue