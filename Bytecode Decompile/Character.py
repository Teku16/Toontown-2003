import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, PartBundleNode

class Character(PartBundleNode.PartBundleNode, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

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
        returnValue = libpanda._inPnRYRBCxW()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getBundle(self):
        returnValue = libpanda._inPnRYRMPjU(self.this)
        import CharacterJointBundle
        returnObject = CharacterJointBundle.CharacterJointBundle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def getComputedVertices(self):
        returnValue = libpanda._inPnRYRI6Xe(self.this)
        import ComputedVertices
        returnObject = ComputedVertices.ComputedVertices(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getNumParts(self):
        returnValue = libpanda._inPnRYRUaOF(self.this)
        return returnValue

    def getPart(self, n):
        returnValue = libpanda._inPnRYRY7uH(self.this, n)
        import PartGroup
        returnObject = PartGroup.PartGroup(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def writeParts(self, out):
        returnValue = libpanda._inPnRYRoBhZ(self.this, out.this)
        return returnValue

    def writePartValues(self, out):
        returnValue = libpanda._inPnRYR3iP2(self.this, out.this)
        return returnValue

    def updateToNow(self):
        returnValue = libpanda._inPnRYR9b_8(self.this)
        return returnValue

    def update(self):
        returnValue = libpanda._inPnRYRoVfb(self.this)
        return returnValue

    def forceUpdate(self):
        returnValue = libpanda._inPnRYRCgKI(self.this)
        return returnValue