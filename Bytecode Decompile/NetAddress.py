import types, libpanda, libpandaDowncasts, FFIExternalObject

class NetAddress(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inP9ImM_XOH()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstPRNetAddr(self, addr):
        self.this = libpanda._inP9ImM7tFa(addr.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inP9ImMbYRe:
            libpanda._inP9ImMbYRe(self.this)

    def setAny(self, port):
        returnValue = libpanda._inP9ImMCqM_(self.this, port)
        return returnValue

    def setLocalhost(self, port):
        returnValue = libpanda._inP9ImMPoxe(self.this, port)
        return returnValue

    def setHost(self, hostname, port):
        returnValue = libpanda._inP9ImMhU_T(self.this, hostname, port)
        return returnValue

    def clear(self):
        returnValue = libpanda._inP9ImMNfpu(self.this)
        return returnValue

    def getPort(self):
        returnValue = libpanda._inP9ImMiHNt(self.this)
        return returnValue

    def setPort(self, port):
        returnValue = libpanda._inP9ImMwG63(self.this, port)
        return returnValue

    def getIpString(self):
        returnValue = libpanda._inP9ImMP3mv(self.this)
        return returnValue

    def getIp(self):
        returnValue = libpanda._inP9ImMAxhR(self.this)
        return returnValue

    def getIpComponent(self, n):
        returnValue = libpanda._inP9ImMD_kR(self.this, n)
        return returnValue

    def getAddr(self):
        returnValue = libpanda._inP9ImMJjjL(self.this)
        import PRNetAddr
        returnObject = PRNetAddr.PRNetAddr(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def output(self, out):
        returnValue = libpanda._inP9ImMBvAY(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                import PRNetAddr
                if isinstance(_args[0], PRNetAddr.PRNetAddr):
                    return self.__overloaded_constructor_ptrConstPRNetAddr(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <PRNetAddr.PRNetAddr> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '