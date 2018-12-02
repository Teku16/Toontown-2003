import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, CollisionSolid

class CollisionSegment(CollisionSolid.CollisionSolid, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPHwcaH_0_()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3f_ptrConstLPoint3f(self, a, db):
        self.this = libpanda._inPHwcahcIM(a.this, db.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_float_float_float_float_float_float(self, ax, ay, az, bx, by, bz):
        self.this = libpanda._inPHwcaGSlK(ax, ay, az, bx, by, bz)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPHwcaXHZw:
            libpanda._inPHwcaXHZw(self.this)

    def getClassType():
        returnValue = libpanda._inPHwcakImW()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def __overloaded_setPointA_ptrCollisionSegment_ptrConstLPoint3f(self, a):
        returnValue = libpanda._inPHwca6ebw(self.this, a.this)
        return returnValue

    def __overloaded_setPointA_ptrCollisionSegment_float_float_float(self, x, y, z):
        returnValue = libpanda._inPHwca9ePy(self.this, x, y, z)
        return returnValue

    def getPointA(self):
        returnValue = libpanda._inPHwcaxXkX(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_setPointB_ptrCollisionSegment_ptrConstLPoint3f(self, b):
        returnValue = libpanda._inPHwcayVbM(self.this, b.this)
        return returnValue

    def __overloaded_setPointB_ptrCollisionSegment_float_float_float(self, x, y, z):
        returnValue = libpanda._inPHwca1bPO(self.this, x, y, z)
        return returnValue

    def getPointB(self):
        returnValue = libpanda._inPHwca2Kkz(self.this)
        import Point3
        returnObject = Point3.Point3(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_setFromLens_ptrCollisionSegment_ptrLensNode_ptrConstLPoint2f(self, camera, point):
        returnValue = libpanda._inPHwcakPim(self.this, camera.this, point.this)
        return returnValue

    def __overloaded_setFromLens_ptrCollisionSegment_ptrLensNode_float_float(self, camera, px, py):
        returnValue = libpanda._inPHwcat5Ut(self.this, camera.this, px, py)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 2:
                import Point3
                if isinstance(_args[0], Point3.Point3):
                    import Point3
                    if isinstance(_args[1], Point3.Point3):
                        return self.__overloaded_constructor_ptrConstLPoint3f_ptrConstLPoint3f(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Point3.Point3> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
            else:
                if numArgs == 6:
                    if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                    if isinstance(_args[4], types.FloatType) or isinstance(_args[4], types.IntType):
                                        if isinstance(_args[5], types.FloatType) or isinstance(_args[5], types.IntType):
                                            return self.__overloaded_constructor_float_float_float_float_float_float(_args[0], _args[1], _args[2], _args[3], _args[4], _args[5])
                                        else:
                                            raise TypeError, 'Invalid argument 5, expected one of: <types.FloatType> '
                                    else:
                                        raise TypeError, 'Invalid argument 4, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 2 6 '

    def setPointB(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Point3
            if isinstance(_args[0], Point3.Point3):
                return self.__overloaded_setPointB_ptrCollisionSegment_ptrConstLPoint3f(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
        else:
            if numArgs == 3:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            return self.__overloaded_setPointB_ptrCollisionSegment_float_float_float(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 3 '

    def setPointA(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Point3
            if isinstance(_args[0], Point3.Point3):
                return self.__overloaded_setPointA_ptrCollisionSegment_ptrConstLPoint3f(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Point3.Point3> '
        else:
            if numArgs == 3:
                if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            return self.__overloaded_setPointA_ptrCollisionSegment_float_float_float(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 3 '

    def setFromLens(self, *_args):
        numArgs = len(_args)
        if numArgs == 2:
            import LensNode
            if isinstance(_args[0], LensNode.LensNode):
                import Point2
                if isinstance(_args[1], Point2.Point2):
                    return self.__overloaded_setFromLens_ptrCollisionSegment_ptrLensNode_ptrConstLPoint2f(_args[0], _args[1])
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <Point2.Point2> '
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <LensNode.LensNode> '
        else:
            if numArgs == 3:
                import LensNode
                if isinstance(_args[0], LensNode.LensNode):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                            return self.__overloaded_setFromLens_ptrCollisionSegment_ptrLensNode_float_float(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <LensNode.LensNode> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 2 3 '