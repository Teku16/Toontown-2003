import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, SelectiveChildNode

class LODNode(SelectiveChildNode.SelectiveChildNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, name):
        self.this = libpanda._inPkJyomKZh(name)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPkJyorgkj:
            libpanda._inPkJyorgkj(self.this)

    def getClassType():
        returnValue = libpanda._inPkJyolHCR()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def addSwitch(self, _in, out):
        returnValue = libpanda._inPkJyoQFoz(self.this, _in, out)
        return returnValue

    def setSwitch(self, index, _in, out):
        returnValue = libpanda._inPkJyohpdI(self.this, index, _in, out)
        return returnValue

    def clearSwitches(self):
        returnValue = libpanda._inPkJyo25DC(self.this)
        return returnValue

    def getNumSwitches(self):
        returnValue = libpanda._inPkJyob65Z(self.this)
        return returnValue

    def getIn(self, index):
        returnValue = libpanda._inPkJyoTHPo(self.this, index)
        return returnValue

    def getOut(self, index):
        returnValue = libpanda._inPkJyoRO_6(self.this, index)
        return returnValue

    def setCenter(self, center):
        returnValue = libpanda._inPkJyoOHp_(self.this, center.this)
        return returnValue

    def getCenter(self):
        returnValue = libpanda._inPkJyo7mat(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return