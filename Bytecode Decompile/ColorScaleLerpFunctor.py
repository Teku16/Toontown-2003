import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, SimpleLerpFunctorLVecBase4f

class ColorScaleLerpFunctor(SimpleLerpFunctorLVecBase4f.SimpleLerpFunctorLVecBase4f, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrNodePath_ptrLVecBase4f_ptrLVecBase4f(self, np, start, end):
        self.this = libpanda._inPkJyoLC1H(np.this, start.this, end.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_ptrLVecBase4f_ptrLVecBase4f_ptrNodePath(self, np, start, end, wrt):
        self.this = libpanda._inPkJyoqMFY(np.this, start.this, end.this, wrt.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_float_float_float_float_float_float_float_float(self, np, sr, sg, sb, sa, er, eg, eb, ea):
        self.this = libpanda._inPkJyojybb(np.this, sr, sg, sb, sa, er, eg, eb, ea)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrNodePath_float_float_float_float_float_float_float_float_ptrNodePath(self, np, sr, sg, sb, sa, er, eg, eb, ea, wrt):
        self.this = libpanda._inPkJyoCjMP(np.this, sr, sg, sb, sa, er, eg, eb, ea, wrt.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpanda._inPkJyotvME()
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
                import VBase4
                if isinstance(_args[1], VBase4.VBase4):
                    import VBase4
                    if isinstance(_args[2], VBase4.VBase4):
                        return self.__overloaded_constructor_ptrNodePath_ptrLVecBase4f_ptrLVecBase4f(_args[0], _args[1], _args[2])
                    else:
                        raise TypeError, 'Invalid argument 2, expected one of: <VBase4.VBase4> '
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <VBase4.VBase4> '
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
        else:
            if numArgs == 4:
                import NodePath
                if isinstance(_args[0], NodePath.NodePath):
                    import VBase4
                    if isinstance(_args[1], VBase4.VBase4):
                        import VBase4
                        if isinstance(_args[2], VBase4.VBase4):
                            import NodePath
                            if isinstance(_args[3], NodePath.NodePath):
                                return self.__overloaded_constructor_ptrNodePath_ptrLVecBase4f_ptrLVecBase4f_ptrNodePath(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <NodePath.NodePath> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <VBase4.VBase4> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <VBase4.VBase4> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <NodePath.NodePath> '
            else:
                if numArgs == 9:
                    import NodePath
                    if isinstance(_args[0], NodePath.NodePath):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                    if isinstance(_args[4], types.FloatType) or isinstance(_args[4], types.IntType):
                                        if isinstance(_args[5], types.FloatType) or isinstance(_args[5], types.IntType):
                                            if isinstance(_args[6], types.FloatType) or isinstance(_args[6], types.IntType):
                                                if isinstance(_args[7], types.FloatType) or isinstance(_args[7], types.IntType):
                                                    if isinstance(_args[8], types.FloatType) or isinstance(_args[8], types.IntType):
                                                        return self.__overloaded_constructor_ptrNodePath_float_float_float_float_float_float_float_float(_args[0], _args[1], _args[2], _args[3], _args[4], _args[5], _args[6], _args[7], _args[8])
                                                    else:
                                                        raise TypeError, 'Invalid argument 8, expected one of: <types.FloatType> '
                                                else:
                                                    raise TypeError, 'Invalid argument 7, expected one of: <types.FloatType> '
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
                    if numArgs == 10:
                        import NodePath
                        if isinstance(_args[0], NodePath.NodePath):
                            if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                                if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                    if isinstance(_args[3], types.FloatType) or isinstance(_args[3], types.IntType):
                                        if isinstance(_args[4], types.FloatType) or isinstance(_args[4], types.IntType):
                                            if isinstance(_args[5], types.FloatType) or isinstance(_args[5], types.IntType):
                                                if isinstance(_args[6], types.FloatType) or isinstance(_args[6], types.IntType):
                                                    if isinstance(_args[7], types.FloatType) or isinstance(_args[7], types.IntType):
                                                        if isinstance(_args[8], types.FloatType) or isinstance(_args[8], types.IntType):
                                                            import NodePath
                                                            if isinstance(_args[9], NodePath.NodePath):
                                                                return self.__overloaded_constructor_ptrNodePath_float_float_float_float_float_float_float_float_ptrNodePath(_args[0], _args[1], _args[2], _args[3], _args[4], _args[5], _args[6], _args[7], _args[8], _args[9])
                                                            else:
                                                                raise TypeError, 'Invalid argument 9, expected one of: <NodePath.NodePath> '
                                                        else:
                                                            raise TypeError, 'Invalid argument 8, expected one of: <types.FloatType> '
                                                    else:
                                                        raise TypeError, 'Invalid argument 7, expected one of: <types.FloatType> '
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
                        raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 3 4 9 10 '