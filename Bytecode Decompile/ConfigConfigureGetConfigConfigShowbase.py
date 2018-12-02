import types, libdirect, libdirectDowncasts, FFIExternalObject

class ConfigConfigureGetConfigConfigShowbase(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libdirectDowncasts]

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
        if libdirect and libdirect._inPL4GTSvPT:
            libdirect._inPL4GTSvPT(self.this)

    def __overloaded_GetBool_atomicstring_bool(sym, _def):
        returnValue = libdirect._inPL4GTpkh_(sym, _def)
        return returnValue

    __overloaded_GetBool_atomicstring_bool = staticmethod(__overloaded_GetBool_atomicstring_bool)

    def __overloaded_GetBool_atomicstring(sym):
        returnValue = libdirect._inPL4GTFBgQ(sym)
        return returnValue

    __overloaded_GetBool_atomicstring = staticmethod(__overloaded_GetBool_atomicstring)

    def __overloaded_GetInt_atomicstring_int(sym, _def):
        returnValue = libdirect._inPL4GTvpTV(sym, _def)
        return returnValue

    __overloaded_GetInt_atomicstring_int = staticmethod(__overloaded_GetInt_atomicstring_int)

    def __overloaded_GetInt_atomicstring(sym):
        returnValue = libdirect._inPL4GTO3AW(sym)
        return returnValue

    __overloaded_GetInt_atomicstring = staticmethod(__overloaded_GetInt_atomicstring)

    def __overloaded_GetFloat_atomicstring_float(sym, _def):
        returnValue = libdirect._inPL4GTMv9T(sym, _def)
        return returnValue

    __overloaded_GetFloat_atomicstring_float = staticmethod(__overloaded_GetFloat_atomicstring_float)

    def __overloaded_GetFloat_atomicstring(sym):
        returnValue = libdirect._inPL4GTK7VG(sym)
        return returnValue

    __overloaded_GetFloat_atomicstring = staticmethod(__overloaded_GetFloat_atomicstring)

    def __overloaded_GetDouble_atomicstring_double(sym, _def):
        returnValue = libdirect._inPL4GTGCam(sym, _def)
        return returnValue

    __overloaded_GetDouble_atomicstring_double = staticmethod(__overloaded_GetDouble_atomicstring_double)

    def __overloaded_GetDouble_atomicstring(sym):
        returnValue = libdirect._inPL4GT_PRv(sym)
        return returnValue

    __overloaded_GetDouble_atomicstring = staticmethod(__overloaded_GetDouble_atomicstring)

    def __overloaded_GetString_atomicstring_atomicstring(sym, _def):
        returnValue = libdirect._inPL4GTjFEi(sym, _def)
        return returnValue

    __overloaded_GetString_atomicstring_atomicstring = staticmethod(__overloaded_GetString_atomicstring_atomicstring)

    def __overloaded_GetString_atomicstring(sym):
        returnValue = libdirect._inPL4GTz6I6(sym)
        return returnValue

    __overloaded_GetString_atomicstring = staticmethod(__overloaded_GetString_atomicstring)

    def GetInt(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetInt_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.IntType):
                        return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetInt_atomicstring_int(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    GetInt = staticmethod(GetInt)

    def GetFloat(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetFloat_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetFloat_atomicstring_float(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    GetFloat = staticmethod(GetFloat)

    def GetBool(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetBool_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.IntType):
                        return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetBool_atomicstring_bool(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    GetBool = staticmethod(GetBool)

    def GetDouble(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetDouble_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.FloatType) or isinstance(_args[1], types.IntType):
                        return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetDouble_atomicstring_double(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.FloatType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    GetDouble = staticmethod(GetDouble)

    def GetString(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetString_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    if isinstance(_args[1], types.StringType):
                        return ConfigConfigureGetConfigConfigShowbase.__overloaded_GetString_atomicstring_atomicstring(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <types.StringType> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    GetString = staticmethod(GetString)