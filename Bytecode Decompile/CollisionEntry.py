import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class CollisionEntry(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
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

    def destructor(self):
        if libpanda and libpanda._inPHwcatQwG:
            libpanda._inPHwcatQwG(self.this)

    def getClassType():
        returnValue = libpanda._inPHwcaSIuZ()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getFrom(self):
        returnValue = libpanda._inPHwcaGwYK(self.this)
        import CollisionSolid
        returnObject = CollisionSolid.CollisionSolid(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def hasInto(self):
        returnValue = libpanda._inPHwcavTcn(self.this)
        return returnValue

    def getInto(self):
        returnValue = libpanda._inPHwcaGQba(self.this)
        import CollisionSolid
        returnObject = CollisionSolid.CollisionSolid(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getFromNode(self):
        returnValue = libpanda._inPHwcae4xC(self.this)
        import CollisionNode
        returnObject = CollisionNode.CollisionNode(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getIntoNode(self):
        returnValue = libpanda._inPHwca_40S(self.this)
        import PandaNode
        returnObject = PandaNode.PandaNode(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getIntoNodePath(self):
        returnValue = libpanda._inPHwca_3Sn(self.this)
        import NodePath
        returnObject = NodePath.NodePath(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getFromSpace(self):
        returnValue = libpanda._inPHwcawz01(self.this)
        import Mat4
        returnObject = Mat4.Mat4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getIntoSpace(self):
        returnValue = libpanda._inPHwcaQx3F(self.this)
        import Mat4
        returnObject = Mat4.Mat4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getWrtSpace(self):
        returnValue = libpanda._inPHwcaFHed(self.this)
        import Mat4
        returnObject = Mat4.Mat4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getInvWrtSpace(self):
        returnValue = libpanda._inPHwca7dHE(self.this)
        import Mat4
        returnObject = Mat4.Mat4(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setFromVelocity(self, vel):
        returnValue = libpanda._inPHwcawQUi(self.this, vel.this)
        return returnValue

    def hasFromVelocity(self):
        returnValue = libpanda._inPHwcapT1c(self.this)
        return returnValue

    def getFromVelocity(self):
        returnValue = libpanda._inPHwcaB00P(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setIntoIntersectionPoint(self, point):
        returnValue = libpanda._inPHwcaTR8J(self.this, point.this)
        return returnValue

    def hasIntoIntersectionPoint(self):
        returnValue = libpanda._inPHwcaf_Lr(self.this)
        return returnValue

    def getIntoIntersectionPoint(self):
        returnValue = libpanda._inPHwcawULe(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def hasFromIntersectionPoint(self):
        returnValue = libpanda._inPHwca4yGb(self.this)
        return returnValue

    def getFromIntersectionPoint(self):
        returnValue = libpanda._inPHwcaQUGO(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def setIntoSurfaceNormal(self, normal):
        returnValue = libpanda._inPHwca2aZL(self.this, normal.this)
        return returnValue

    def hasIntoSurfaceNormal(self):
        returnValue = libpanda._inPHwcadFZi(self.this)
        return returnValue

    def getIntoSurfaceNormal(self):
        returnValue = libpanda._inPHwcaq_WV(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setFromSurfaceNormal(self, normal):
        returnValue = libpanda._inPHwcaWPW7(self.this, normal.this)
        return returnValue

    def hasFromSurfaceNormal(self):
        returnValue = libpanda._inPHwcayPUS(self.this)
        return returnValue

    def getFromSurfaceNormal(self):
        returnValue = libpanda._inPHwcaqoVF(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setIntoDepth(self, depth):
        returnValue = libpanda._inPHwcaTUmw(self.this, depth)
        return returnValue

    def hasIntoDepth(self):
        returnValue = libpanda._inPHwcaT8Ls(self.this)
        return returnValue

    def getIntoDepth(self):
        returnValue = libpanda._inPHwcaqbLf(self.this)
        return returnValue

    def setFromDepth(self, depth):
        returnValue = libpanda._inPHwcazLjg(self.this, depth)
        return returnValue

    def hasFromDepth(self):
        returnValue = libpanda._inPHwcayjIc(self.this)
        return returnValue

    def getFromDepth(self):
        returnValue = libpanda._inPHwcaqGIP(self.this)
        return returnValue