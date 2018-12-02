import types, libpanda, libpandaDowncasts, FFIExternalObject

class PStatClient(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

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
        if libpanda and libpanda._inPiqKx_6DX:
            libpanda._inPiqKx_6DX(self.this)

    def __overloaded_connect_atomicstring_int(parameter0, parameter1):
        returnValue = libpanda._inPiqKxcCtG(parameter0, parameter1)
        return returnValue

    __overloaded_connect_atomicstring_int = staticmethod(__overloaded_connect_atomicstring_int)

    def __overloaded_connect_atomicstring(parameter0):
        returnValue = libpanda._inPiqKxKb_Y(parameter0)
        return returnValue

    __overloaded_connect_atomicstring = staticmethod(__overloaded_connect_atomicstring)

    def __overloaded_connect():
        returnValue = libpanda._inPiqKxcnwA()
        return returnValue

    __overloaded_connect = staticmethod(__overloaded_connect)

    def disconnect():
        returnValue = libpanda._inPiqKxGM4i()
        return returnValue

    disconnect = staticmethod(disconnect)

    def isConnected():
        returnValue = libpanda._inPiqKxnHkh()
        return returnValue

    isConnected = staticmethod(isConnected)

    def resumeAfterPause():
        returnValue = libpanda._inPiqKx8MTf()
        return returnValue

    resumeAfterPause = staticmethod(resumeAfterPause)

    def connect(*_args):
        numArgs = len(_args)
        if numArgs == 0:
            return PStatClient.__overloaded_connect()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return PStatClient.__overloaded_connect_atomicstring(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                if numArgs == 2:
                    if isinstance(_args[0], types.StringType):
                        if isinstance(_args[1], types.IntType):
                            return PStatClient.__overloaded_connect_atomicstring_int(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '

    connect = staticmethod(connect)