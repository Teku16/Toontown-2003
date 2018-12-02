import types, libpanda, libpandaDowncasts, FFIExternalObject, ConnectionReader

class RecentConnectionReader(ConnectionReader.ConnectionReader, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, manager):
        self.this = libpanda._inP9ImMA_Qe(manager.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inP9ImMGUzi:
            libpanda._inP9ImMGUzi(self.this)

    def dataAvailable(self):
        returnValue = libpanda._inP9ImMmPBT(self.this)
        return returnValue

    def __overloaded_getData_ptrRecentConnectionReader_ptrDatagram(self, result):
        returnValue = libpanda._inP9ImMjnmx(self.this, result.this)
        return returnValue

    def __overloaded_getData_ptrRecentConnectionReader_ptrNetDatagram(self, result):
        returnValue = libpanda._inP9ImMeb0k(self.this, result.this)
        return returnValue

    def getData(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Datagram, NetDatagram
            if isinstance(_args[0], Datagram.Datagram):
                return self.__overloaded_getData_ptrRecentConnectionReader_ptrDatagram(_args[0])
            else:
                if isinstance(_args[0], NetDatagram.NetDatagram):
                    return self.__overloaded_getData_ptrRecentConnectionReader_ptrNetDatagram(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Datagram.Datagram> <NetDatagram.NetDatagram> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '