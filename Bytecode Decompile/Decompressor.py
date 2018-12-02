import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class Decompressor(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpandaexpress._inP2KOdB4PE()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inP2KOdJ0Mb:
            libpandaexpress._inP2KOdJ0Mb(self.this)

    def __overloaded_initiate_ptrDecompressor_ptrConstFilename(self, sourceFile):
        returnValue = libpandaexpress._inP2KOdw6VS(self.this, sourceFile.this)
        return returnValue

    def __overloaded_initiate_ptrDecompressor_ptrConstFilename_ptrConstFilename(self, sourceFile, destFile):
        returnValue = libpandaexpress._inP2KOdM1ck(self.this, sourceFile.this, destFile.this)
        return returnValue

    def run(self):
        returnValue = libpandaexpress._inP2KOd5YBi(self.this)
        return returnValue

    def __overloaded_decompress_ptrDecompressor_ptrConstFilename(self, sourceFile):
        returnValue = libpandaexpress._inP2KOdHZkY(self.this, sourceFile.this)
        return returnValue

    def __overloaded_decompress_ptrDecompressor_ptrRamfile(self, sourceAndDestFile):
        returnValue = libpandaexpress._inP2KOdCUun(self.this, sourceAndDestFile.this)
        return returnValue

    def getProgress(self):
        returnValue = libpandaexpress._inP2KOdpjks(self.this)
        return returnValue

    def initiate(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Filename
            if isinstance(_args[0], Filename.Filename):
                return self.__overloaded_initiate_ptrDecompressor_ptrConstFilename(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Filename.Filename> '
        else:
            if numArgs == 2:
                import Filename
                if isinstance(_args[0], Filename.Filename):
                    import Filename
                    if isinstance(_args[1], Filename.Filename):
                        return self.__overloaded_initiate_ptrDecompressor_ptrConstFilename_ptrConstFilename(_args[0], _args[1])
                    else:
                        raise TypeError, 'Invalid argument 1, expected one of: <Filename.Filename> '
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Filename.Filename> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 2 '

    def decompress(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Ramfile, Filename
            if isinstance(_args[0], Ramfile.Ramfile):
                return self.__overloaded_decompress_ptrDecompressor_ptrRamfile(_args[0])
            else:
                if isinstance(_args[0], Filename.Filename):
                    return self.__overloaded_decompress_ptrDecompressor_ptrConstFilename(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Ramfile.Ramfile> <Filename.Filename> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '