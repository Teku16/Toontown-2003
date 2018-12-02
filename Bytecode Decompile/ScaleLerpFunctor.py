import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, SimpleLerpFunctorLVecBase3f

class ScaleLerpFunctor(SimpleLerpFunctorLVecBase3f.SimpleLerpFunctorLVecBase3f, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrNodePath_ptrLVecBase3f_ptrLVecBase3f(self, np, start, end):
        self.this = libpanda._inPkJyoM7Ek(np.this, start.this, end.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_ptrLVecBase3f_ptrLVecBase3f_ptrNodePath(self, np, start, end, wrt):
        self.this = libpanda._inPkJyocsJY(np.this, start.this, end.this, wrt.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_float_float_float_float_float_float(self, np, sx, sy, sz, ex, ey, ez):
        self.this = libpanda._inPkJyooNcS(np.this, sx, sy, sz, ex, ey, ez)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_float_float_float_float_float_float_ptrNodePath(self, np, sx, sy, sz, ex, ey, ez, wrt):
        self.this = libpanda._inPkJyo3jPG(np.this, sx, sy, sz, ex, ey, ez, wrt.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpanda._inPkJyo_dcM()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 3:
            import NodePath
            if isinstance(_args[0], NodePath.NodePath):
                import VBase3
                if isinstance(_args[1], VBase3.VBase3):
                    import VBase3
                    if isinstance(_args[2], VBase3.VBase3):
                        return self.__overloaded_constructor_ptrNodePath_ptrLVecBase3f_ptrLVecBase3f(_args[0], _args[1], _args[2])
                    else:
                        raise TypeError, 'Invalid argument 2, expected one of: <VBase3.VBase3> '
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <VBase3.VBase3> '
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
        else:
            if numArgs == 4:
                import NodePath
                if isinstance(_args[0], NodePath.NodePath):
                    import VBase3
                    if isinstance(_args[1], VBase3.VBase3):
                        import VBase3
                        if isinstance(_args[2], VBase3.VBase3):
                            import NodePath
                            if isinstance(_args[3], NodePath.NodePath):
                                return self.__overloaded_constructor_ptrNodePath_ptrLVecBase3f_ptrLVecBase3f_ptrNodePath(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <NodePath.NodePath> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <VBase3.VBase3> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <VBase3.VBase3> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
            else:
                if numArgs == 7:
                    import NodePath
                    if isinstance(_args[0], NodePath.NodePath):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                    if isinstance(_args[4], types.FloatType) or isinstance(_args[4], types.IntType):
                                        if isinstance(_args[5], types.FloatType) or isinstance(_args[5], types.IntType):
                                            if isinstance(_args[6], types.FloatType) or isinstance(_args[6], types.IntType):
                                                return self.__overloaded_constructor_ptrNodePath_float_float_float_float_float_float(_args[0], _args[1], _args[2], _args[3], _args[4], _args[5], _args[6])
                                            else:
                                                raise TypeError, 'Invalid argument 6, expected one of: <types.FloatType> '
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
                        raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
                else:
                    if numArgs == 8:
                        import NodePath
                        if isinstance(_args[0], NodePath.NodePath):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                        if isinstance(_args[4], types.FloatType) or isinstance(_args[4], types.IntType):
                                            if isinstance(_args[5], types.FloatType) or isinstance(_args[5], types.IntType):
                                                if isinstance(_args[6], types.FloatType) or isinstance(_args[6], types.IntType):
                                                    import NodePath
                                                    if isinstance(_args[7], NodePath.NodePath):
                                                        return self.__overloaded_constructor_ptrNodePath_float_float_float_float_float_float_ptrNodePath(_args[0], _args[1], _args[2], _args[3], _args[4], _args[5], _args[6], _args[7])
                                                    else:
                                                        raise TypeError, 'Invalid argument 7, expected one of: <NodePath.NodePath> '
                                                else:
                                                    raise TypeError, 'Invalid argument 6, expected one of: <types.FloatType> '
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
                            raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
                    else:
                        raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 3 4 7 8 '