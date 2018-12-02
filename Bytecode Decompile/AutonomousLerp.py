import types, libpanda, libpandaDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class AutonomousLerp(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstAutonomousLerp(self, parameter0):
        self.this = libpanda._inPgRdzm1mi(parameter0.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrLerpFunctor_float_ptrLerpBlendType_ptrEventHandler(self, func, endt, blend, handler):
        self.this = libpanda._inPgRdzxGSy(func.this, endt, blend.this, handler.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrLerpFunctor_float_float_ptrLerpBlendType_ptrEventHandler(self, func, startt, endt, blend, handler):
        self.this = libpanda._inPgRdzJqNi(func.this, startt, endt, blend.this, handler.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def getClassType():
        returnValue = libpanda._inPgRdznSlS()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def assign(self, parameter1):
        returnValue = libpanda._inPgRdzn3L_(self.this, parameter1.this)
        returnObject = AutonomousLerp(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def start(self):
        returnValue = libpanda._inPgRdzpbE1(self.this)
        return returnValue

    def stop(self):
        returnValue = libpanda._inPgRdz8_s_(self.this)
        return returnValue

    def resume(self):
        returnValue = libpanda._inPgRdze999(self.this)
        return returnValue

    def isDone(self):
        returnValue = libpanda._inPgRdzch0a(self.this)
        return returnValue

    def getFunctor(self):
        returnValue = libpanda._inPgRdzlqo1(self.this)
        import LerpFunctor
        returnObject = LerpFunctor.LerpFunctor(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def setT(self, parameter1):
        returnValue = libpanda._inPgRdzXKt3(self.this, parameter1)
        return returnValue

    def getT(self):
        returnValue = libpanda._inPgRdzTsbG(self.this)
        return returnValue

    def setEndEvent(self, parameter1):
        returnValue = libpanda._inPgRdzkmdC(self.this, parameter1)
        return returnValue

    def getEndEvent(self):
        returnValue = libpanda._inPgRdzJF7x(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], AutonomousLerp):
                return self.__overloaded_constructor_ptrConstAutonomousLerp(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <AutonomousLerp> '
        else:
            if numArgs == 4:
                import LerpFunctor
                if isinstance(_args[0], LerpFunctor.LerpFunctor):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        import LerpBlendType
                        if isinstance(_args[2], LerpBlendType.LerpBlendType):
                            import EventHandler
                            if isinstance(_args[3], EventHandler.EventHandler):
                                return self.__overloaded_constructor_ptrLerpFunctor_float_ptrLerpBlendType_ptrEventHandler(_args[0], _args[1], _args[2], _args[3])
                            else:
                                raise TypeError, 'Invalid argument 3, expected one of: <EventHandler.EventHandler> '
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <LerpBlendType.LerpBlendType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <LerpFunctor.LerpFunctor> '
            else:
                if numArgs == 5:
                    import LerpFunctor
                    if isinstance(_args[0], LerpFunctor.LerpFunctor):
                        if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                            if isinstance(_args[2], types.FloatType) or isinstance(_args[2], types.IntType):
                                import LerpBlendType
                                if isinstance(_args[3], LerpBlendType.LerpBlendType):
                                    import EventHandler
                                    if isinstance(_args[4], EventHandler.EventHandler):
                                        return self.__overloaded_constructor_ptrLerpFunctor_float_float_ptrLerpBlendType_ptrEventHandler(_args[0], _args[1], _args[2], _args[3], _args[4])
                                    else:
                                        raise TypeError, 'Invalid argument 4, expected one of: <EventHandler.EventHandler> '
                                else:
                                    raise TypeError, 'Invalid argument 3, expected one of: <LerpBlendType.LerpBlendType> '
                            else:
                                raise TypeError, 'Invalid argument 2, expected one of: <types.FloatType> '
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <LerpFunctor.LerpFunctor> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 4 5 '