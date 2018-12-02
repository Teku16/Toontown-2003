import types, libtoontown, libtoontownDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, TypedReferenceCount

class DNASuitEdge(TypedReferenceCount.TypedReferenceCount, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libtoontownDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self, startPoint, endPoint, zoneId):
        self.this = libtoontown._inPet4yL1XC(startPoint.this, endPoint.this, zoneId)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libtoontown and libtoontown._inPet4yazsM:
            libtoontown._inPet4yazsM(self.this)

    def getClassType():
        returnValue = libtoontown._inPet4yOVpE()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def getStartPoint(self):
        returnValue = libtoontown._inPet4ym728(self.this)
        import DNASuitPoint
        returnObject = DNASuitPoint.DNASuitPoint(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getEndPoint(self):
        returnValue = libtoontown._inPet4y8Cdh(self.this)
        import DNASuitPoint
        returnObject = DNASuitPoint.DNASuitPoint(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def getZoneId(self):
        returnValue = libtoontown._inPet4yex_N(self.this)
        return returnValue

    def setZoneId(self, zoneId):
        returnValue = libtoontown._inPet4ywx8C(self.this, zoneId)
        return returnValue

    def output(self, out):
        returnValue = libtoontown._inPet4ysQOc(self.this, out.this)
        return returnValue

    def __overloaded_write_ptrConstDNASuitEdge_ptrOstream_ptrDNAStorage_int(self, out, store, indentLevel):
        returnValue = libtoontown._inPet4yjMts(self.this, out.this, store.this, indentLevel)
        return returnValue

    def __overloaded_write_ptrConstDNASuitEdge_ptrOstream_ptrDNAStorage(self, out, store):
        returnValue = libtoontown._inPet4ygV5N(self.this, out.this, store.this)
        return returnValue

    def write(self, *_args):
        numArgs = len(_args)
        if numArgs == 2:
            import Ostream
            if isinstance(_args[0], Ostream.Ostream):
                import DNAStorage
                if isinstance(_args[1], DNAStorage.DNAStorage):
                    return self.__overloaded_write_ptrConstDNASuitEdge_ptrOstream_ptrDNAStorage(_args[0], _args[1])
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <DNAStorage.DNAStorage> '
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
        else:
            if numArgs == 3:
                import Ostream
                if isinstance(_args[0], Ostream.Ostream):
                    import DNAStorage
                    if isinstance(_args[1], DNAStorage.DNAStorage):
                        if isinstance(_args[2], types.IntType):
                            return self.__overloaded_write_ptrConstDNASuitEdge_ptrOstream_ptrDNAStorage_int(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <DNAStorage.DNAStorage> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 2 3 '