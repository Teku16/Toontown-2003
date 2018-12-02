import types, libtoontown, libtoontownDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, DNAGroup

class DNAData(DNAGroup.DNAGroup, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libtoontownDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstDNAData(self, copy):
        self.this = libtoontown._inPet4yeOgM(copy.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, initialName):
        self.this = libtoontown._inPet4ykx_q(initialName)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libtoontown._inPet4ycMjm()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libtoontown and libtoontown._inPet4yxcrx:
            libtoontown._inPet4yxcrx(self.this)

    def __overloaded_resolveDnaFilename_ptrFilename_ptrConstDSearchPath(dnaFilename, searchpath):
        returnValue = libtoontown._inPet4yZPNG(dnaFilename.this, searchpath.this)
        return returnValue

    __overloaded_resolveDnaFilename_ptrFilename_ptrConstDSearchPath = staticmethod(__overloaded_resolveDnaFilename_ptrFilename_ptrConstDSearchPath)

    def __overloaded_resolveDnaFilename_ptrFilename(dnaFilename):
        returnValue = libtoontown._inPet4yAR01(dnaFilename.this)
        return returnValue

    __overloaded_resolveDnaFilename_ptrFilename = staticmethod(__overloaded_resolveDnaFilename_ptrFilename)

    def getClassType():
        returnValue = libtoontown._inPet4yllrg()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def assign(self, copy):
        returnValue = libtoontown._inPet4y8Iao(self.this, copy.this)
        returnObject = DNAData(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def __overloaded_read_ptrDNAData_ptrFilename_ptrOstream(self, filename, error):
        returnValue = libtoontown._inPet4ybqn0(self.this, filename.this, error.this)
        return returnValue

    def __overloaded_read_ptrDNAData_ptrFilename(self, filename):
        returnValue = libtoontown._inPet4yIS50(self.this, filename.this)
        return returnValue

    def __overloaded_read_ptrDNAData_ptrIstream_ptrOstream(self, _in, error):
        returnValue = libtoontown._inPet4yWygI(self.this, _in.this, error.this)
        return returnValue

    def __overloaded_read_ptrDNAData_ptrIstream(self, _in):
        returnValue = libtoontown._inPet4yWofQ(self.this, _in.this)
        return returnValue

    def __overloaded_resolveExternals_ptrDNAData_atomicstring_ptrOstream(self, searchpath, error):
        returnValue = libtoontown._inPet4yebLE(self.this, searchpath, error.this)
        return returnValue

    def __overloaded_resolveExternals_ptrDNAData_atomicstring(self, searchpath):
        returnValue = libtoontown._inPet4yXVKM(self.this, searchpath)
        return returnValue

    def __overloaded_writeDna_ptrDNAData_ptrFilename_ptrOstream_ptrDNAStorage(self, filename, error, store):
        returnValue = libtoontown._inPet4yrDGG(self.this, filename.this, error.this, store.this)
        return returnValue

    def __overloaded_writeDna_ptrDNAData_ptrOstream_ptrOstream_ptrDNAStorage(self, out, error, store):
        returnValue = libtoontown._inPet4yMyKP(self.this, out.this, error.this, store.this)
        return returnValue

    def setCoordinateSystem(self, coordsys):
        returnValue = libtoontown._inPet4yUJA5(self.this, coordsys)
        return returnValue

    def getCoordinateSystem(self):
        returnValue = libtoontown._inPet4y2_2I(self.this)
        return returnValue

    def setDnaFilename(self, directory):
        returnValue = libtoontown._inPet4y1wSB(self.this, directory.this)
        return returnValue

    def getDnaFilename(self):
        returnValue = libtoontown._inPet4yjqWP(self.this)
        import Filename
        returnObject = Filename.Filename(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def setDnaStorage(self, store):
        returnValue = libtoontown._inPet4yemc5(self.this, store.this)
        return returnValue

    def getDnaStorage(self):
        returnValue = libtoontown._inPet4ysnzg(self.this)
        import DNAStorage
        returnObject = DNAStorage.DNAStorage(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def resolveDnaFilename(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Filename
            if isinstance(_args[0], Filename.Filename):
                return DNAData.__overloaded_resolveDnaFilename_ptrFilename(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Filename.Filename> '
        else:
            if numArgs == 2:
                import Filename
                if isinstance(_args[0], Filename.Filename):
                    import DSearchPath
                    if isinstance(_args[1], DSearchPath.DSearchPath):
                        return DNAData.__overloaded_resolveDnaFilename_ptrFilename_ptrConstDSearchPath(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <DSearchPath.DSearchPath> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Filename.Filename> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    resolveDnaFilename = staticmethod(resolveDnaFilename)

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], DNAData):
                        return self.__overloaded_constructor_ptrConstDNAData(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <DNAData> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def resolveExternals(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.StringType):
                return self.__overloaded_resolveExternals_ptrDNAData_atomicstring(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
        else:
            if numArgs == 2:
                if isinstance(_args[0], types.StringType):
                    import Ostream
                    if isinstance(_args[1], Ostream.Ostream):
                        return self.__overloaded_resolveExternals_ptrDNAData_atomicstring_ptrOstream(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Ostream.Ostream> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def read(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Istream, Filename
            if isinstance(_args[0], Istream.Istream):
                return self.__overloaded_read_ptrDNAData_ptrIstream(_args[0])
            else:
                if isinstance(_args[0], Filename.Filename):
                    return self.__overloaded_read_ptrDNAData_ptrFilename(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Istream.Istream> <Filename.Filename> '
        else:
            if numArgs == 2:
                import Istream, Filename
                if isinstance(_args[0], Istream.Istream):
                    import Ostream
                    if isinstance(_args[1], Ostream.Ostream):
                        return self.__overloaded_read_ptrDNAData_ptrIstream_ptrOstream(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Ostream.Ostream> '
                else:
                    if isinstance(_args[0], Filename.Filename):
                        import Ostream
                        if isinstance(_args[1], Ostream.Ostream):
                            return self.__overloaded_read_ptrDNAData_ptrFilename_ptrOstream(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <Ostream.Ostream> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Istream.Istream> <Filename.Filename> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def writeDna(self, *_args):
        numArgs = len(_args)
        if numArgs == 3:
            import Ostream, Filename
            if isinstance(_args[0], Ostream.Ostream):
                import Ostream
                if isinstance(_args[1], Ostream.Ostream):
                    import DNAStorage
                    if isinstance(_args[2], DNAStorage.DNAStorage):
                        return self.__overloaded_writeDna_ptrDNAData_ptrOstream_ptrOstream_ptrDNAStorage(_args[0], _args[1], _args[2])
                    else:
                        raise TypeError, 'Invalid argument 2, expected one of: <DNAStorage.DNAStorage> '
                else:
                    raise TypeError, 'Invalid argument 1, expected one of: <Ostream.Ostream> '
            else:
                if isinstance(_args[0], Filename.Filename):
                    import Ostream
                    if isinstance(_args[1], Ostream.Ostream):
                        import DNAStorage
                        if isinstance(_args[2], DNAStorage.DNAStorage):
                            return self.__overloaded_writeDna_ptrDNAData_ptrFilename_ptrOstream_ptrDNAStorage(_args[0], _args[1], _args[2])
                        else:
                            raise TypeError, 'Invalid argument 2, expected one of: <DNAStorage.DNAStorage> '
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Ostream.Ostream> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ostream.Ostream> <Filename.Filename> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 3 '