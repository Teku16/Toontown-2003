import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, DataNode

class TrackerNode(DataNode.DataNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, client, deviceName):
        self.this = libpanda._inPOfOPHyCC(client.this, deviceName)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpanda._inPOfOPkA7p()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def isValid(self):
        returnValue = libpanda._inPOfOPDEoZ(self.this)
        return returnValue

    def getPos(self):
        returnValue = libpanda._inPOfOPfpbJ(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getOrient(self):
        returnValue = libpanda._inPOfOPd1d9(self.this)
        import LOrientationf
        returnObject = LOrientationf.LOrientationf(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getTransform(self):
        returnValue = libpanda._inPOfOPzbsf(self.this)
        import Mat4
        returnObject = Mat4.Mat4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setTrackerCoordinateSystem(self, cs):
        returnValue = libpanda._inPOfOPTq_7(self.this, cs)
        return returnValue

    def getTrackerCoordinateSystem(self):
        returnValue = libpanda._inPOfOPRtgh(self.this)
        return returnValue

    def setGraphCoordinateSystem(self, cs):
        returnValue = libpanda._inPOfOPhH95(self.this, cs)
        return returnValue

    def getGraphCoordinateSystem(self):
        returnValue = libpanda._inPOfOP_MOP(self.this)
        return returnValue