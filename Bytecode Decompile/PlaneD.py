import types, libpanda, libpandaDowncasts, FFIExternalObject

class PlaneD(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPSkjPnOXP()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLPoint3d_ptrConstLPoint3d_ptrConstLPoint3d(self, a, b, c):
        self.this = libpanda._inPSkjPhIG8(a.this, b.this, c.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstLVector3d_ptrConstLPoint3d(self, normal, point):
        self.this = libpanda._inPSkjPA10l(normal.this, point.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPlaned(self, copy):
        self.this = libpanda._inPSkjPWbjn(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_double_double_double_double(self, a, b, c, d):
        self.this = libpanda._inPSkjP6cFb(a, b, c, d)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPSkjPMvqr:
            libpanda._inPSkjPMvqr(self.this)

    def assign(self, copy):
        returnValue = libpanda._inPSkjPwCLO(self.this, copy.this)
        returnObject = PlaneD(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded___mul___ptrConstPlaned_ptrConstLMatrix3d(self, mat):
        returnValue = libpanda._inPSkjPUTn3(self.this, mat.this)
        returnObject = PlaneD(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded___mul___ptrConstPlaned_ptrConstLMatrix4d(self, mat):
        returnValue = libpanda._inPSkjPUDJL(self.this, mat.this)
        returnObject = PlaneD(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getReflectionMat(self):
        returnValue = libpanda._inPSkjPw5g3(self.this)
        import Mat4D
        returnObject = Mat4D.Mat4D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getNormal(self):
        returnValue = libpanda._inPSkjP4OIM(self.this)
        import Vec3D
        returnObject = Vec3D.Vec3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getPoint(self):
        returnValue = libpanda._inPSkjPNQrN(self.this)
        import Point3D
        returnObject = Point3D.Point3D(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def distToPlane(self, point):
        returnValue = libpanda._inPSkjPVgCi(self.this, point.this)
        return returnValue

    def intersectsLine(self, intersectionPoint, p1, p2):
        returnValue = libpanda._inPSkjP0f1l(self.this, intersectionPoint.this, p1.this, p2.this)
        return returnValue

    def getData(self):
        returnValue = libpanda._inPSkjPm3Is(self.this)
        return returnValue

    def getNumComponents(self):
        returnValue = libpanda._inPSkjP95bd(self.this)
        return returnValue

    def output(self, out):
        returnValue = libpanda._inPSkjPxytW(self.this, out.this)
        return returnValue

    def __overloaded_write_ptrConstPlaned_ptrOstream_int(self, out, indentLevel):
        returnValue = libpanda._inPSkjPkL9K(self.this, out.this, indentLevel)
        return returnValue

    def __overloaded_write_ptrConstPlaned_ptrOstream(self, out):
        returnValue = libpanda._inPSkjP8yXN(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], PlaneD):
                    return self.__overloaded_constructor_ptrConstPlaned(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <PlaneD> '
            else:
                if numArgs == 2:
                    import Vec3D
                    if isinstance(_args[0], Vec3D.Vec3D):
                        import Point3D
                        if isinstance(_args[1], Point3D.Point3D):
                            return self.__overloaded_constructor_ptrConstLVector3d_ptrConstLPoint3d(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <Point3D.Point3D> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Vec3D.Vec3D> '
                else:
                    if numArgs == 3:
                        import Point3D
                        if isinstance(_args[0], Point3D.Point3D):
                            import Point3D
                            if isinstance(_args[1], Point3D.Point3D):
                                import Point3D
                                if isinstance(_args[2], Point3D.Point3D):
                                    return self.__overloaded_constructor_ptrConstLPoint3d_ptrConstLPoint3d_ptrConstLPoint3d(_args[0], _args[1], _args[2])
                                else:
                                    raise TypeError, 'Invalid argument 2, expected one of: <Point3D.Point3D> '
                            else:
                                raise TypeError, 'Invalid argument 1, expected one of: <Point3D.Point3D> '
                        else:
                            raise TypeError, 'Invalid argument 0, expected one of: <Point3D.Point3D> '
                    else:
                        if numArgs == 4:
                            if isinstance(_args[0], types.FloatType) or isinstance(_args[0], types.IntType):
                                if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                    if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                        if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                            return self.__overloaded_constructor_double_double_double_double(_args[0], _args[1], _args[2], _args[3])
                                        else:
                                            raise TypeError, 'Invalid argument 3, expected one of: <types.FloatType> '
                                    else:
                                        raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                                else:
                                    raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                            else:
                                raise TypeError, 'Invalid argument 0, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 3 4 '

    def write(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Ostream
            if isinstance(_args[0], Ostream.Ostream):
                return self.__overloaded_write_ptrConstPlaned_ptrOstream(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
        else:
            if numArgs == 2:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    if isinstance(_args[1], types.IntType):
                        return self.__overloaded_write_ptrConstPlaned_ptrOstream_int(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def __mul__(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Mat4D, Mat3D
            if isinstance(_args[0], Mat4D.Mat4D):
                return self.__overloaded___mul___ptrConstPlaned_ptrConstLMatrix4d(_args[0])
            else:
                if isinstance(_args[0], Mat3D.Mat3D):
                    return self.__overloaded___mul___ptrConstPlaned_ptrConstLMatrix3d(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Mat4D.Mat4D> <Mat3D.Mat3D> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '