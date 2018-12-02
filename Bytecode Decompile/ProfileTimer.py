import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class ProfileTimer(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstProfileTimer(self, other):
        self.this = libpandaexpress._inPJoxtvclK(other.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring_int(self, name, maxEntries):
        self.this = libpandaexpress._inPJoxtCJKJ(name, maxEntries)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, name):
        self.this = libpandaexpress._inPJoxt1b5J(name)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpandaexpress._inPJoxtzvu0()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxtP1oe:
            libpandaexpress._inPJoxtP1oe(self.this)

    def __overloaded_consolidateAllTo_ptrOstream(out):
        returnValue = libpandaexpress._inPJoxtq9_x(out.this)
        return returnValue

    __overloaded_consolidateAllTo_ptrOstream = staticmethod(__overloaded_consolidateAllTo_ptrOstream)

    def __overloaded_consolidateAllTo():
        returnValue = libpandaexpress._inPJoxtQiNX()
        return returnValue

    __overloaded_consolidateAllTo = staticmethod(__overloaded_consolidateAllTo)

    def __overloaded_printAllTo_ptrOstream(out):
        returnValue = libpandaexpress._inPJoxt1a5y(out.this)
        return returnValue

    __overloaded_printAllTo_ptrOstream = staticmethod(__overloaded_printAllTo_ptrOstream)

    def __overloaded_printAllTo():
        returnValue = libpandaexpress._inPJoxtR2g_()
        return returnValue

    __overloaded_printAllTo = staticmethod(__overloaded_printAllTo)

    def __overloaded_init_ptrProfileTimer_atomicstring_int(self, name, maxEntries):
        returnValue = libpandaexpress._inPJoxt98tX(self.this, name, maxEntries)
        return returnValue

    def __overloaded_init_ptrProfileTimer_atomicstring(self, name):
        returnValue = libpandaexpress._inPJoxti6RM(self.this, name)
        return returnValue

    def on(self):
        returnValue = libpandaexpress._inPJoxt9f04(self.this)
        return returnValue

    def mark(self, tag):
        returnValue = libpandaexpress._inPJoxtepR4(self.this, tag)
        return returnValue

    def __overloaded_off_ptrProfileTimer(self):
        returnValue = libpandaexpress._inPJoxtmqDp(self.this)
        return returnValue

    def __overloaded_off_ptrProfileTimer_atomicstring(self, tag):
        returnValue = libpandaexpress._inPJoxtez0S(self.this, tag)
        return returnValue

    def getTotalTime(self):
        returnValue = libpandaexpress._inPJoxtf1Vu(self.this)
        return returnValue

    def __overloaded_consolidateTo_ptrConstProfileTimer_ptrOstream(self, out):
        returnValue = libpandaexpress._inPJoxtLAMQ(self.this, out.this)
        return returnValue

    def __overloaded_consolidateTo_ptrConstProfileTimer(self):
        returnValue = libpandaexpress._inPJoxtENRS(self.this)
        return returnValue

    def __overloaded_printTo_ptrConstProfileTimer_ptrOstream(self, out):
        returnValue = libpandaexpress._inPJoxtUUXZ(self.this, out.this)
        return returnValue

    def __overloaded_printTo_ptrConstProfileTimer(self):
        returnValue = libpandaexpress._inPJoxtAgcv(self.this)
        return returnValue

    def consolidateAllTo(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return ProfileTimer.__overloaded_consolidateAllTo()
        else:
            if numArgs == 1:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    return ProfileTimer.__overloaded_consolidateAllTo_ptrOstream(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    consolidateAllTo = staticmethod(consolidateAllTo)

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], ProfileTimer):
                        return self.__overloaded_constructor_ptrConstProfileTimer(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <ProfileTimer> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.StringType):
                        if isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_atomicstring_int(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '

    def printAllTo(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return ProfileTimer.__overloaded_printAllTo()
        else:
            if numArgs == 1:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    return ProfileTimer.__overloaded_printAllTo_ptrOstream(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    printAllTo = staticmethod(printAllTo)

    def printTo(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_printTo_ptrConstProfileTimer()
        else:
            if numArgs == 1:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    return self.__overloaded_printTo_ptrConstProfileTimer_ptrOstream(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def init(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return self.__overloaded_init_ptrProfileTimer_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.IntType):
                        return self.__overloaded_init_ptrProfileTimer_atomicstring_int(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def off(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_off_ptrProfileTimer()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_off_ptrProfileTimer_atomicstring(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def consolidateTo(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_consolidateTo_ptrConstProfileTimer()
        else:
            if numArgs == 1:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    return self.__overloaded_consolidateTo_ptrConstProfileTimer_ptrOstream(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '