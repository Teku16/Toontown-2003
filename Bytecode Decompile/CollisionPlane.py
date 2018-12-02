import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, CollisionSolid

class CollisionPlane(CollisionSolid.CollisionSolid, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstCollisionPlane(self, copy):
        self.this = libpanda._inPHwcap1w1(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPlanef(self, planeBase):
        self.this = libpanda._inPHwcalkhc(planeBase.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPHwcau0SK:
            libpanda._inPHwcau0SK(self.this)

    def getClassType():
        returnValue = libpanda._inPHwca8byU()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getNormal(self):
        returnValue = libpanda._inPHwcalYK9(self.this)
        import Vec3
        returnObject = Vec3.Vec3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def distToPlane(self, point):
        returnValue = libpanda._inPHwcaOb8M(self.this, point.this)
        return returnValue

    def setPlane(self, planeBase):
        returnValue = libpanda._inPHwcaAQAO(self.this, planeBase.this)
        return returnValue

    def getPlane(self):
        returnValue = libpanda._inPHwcaq8W5(self.this)
        import Plane
        returnObject = Plane.Plane(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Plane
            if isinstance(_args[0], Plane.Plane):
                return self.__overloaded_constructor_ptrConstPlanef(_args[0])
            else:
                if isinstance(_args[0], CollisionPlane):
                    return self.__overloaded_constructor_ptrConstCollisionPlane(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Plane.Plane> <CollisionPlane> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '