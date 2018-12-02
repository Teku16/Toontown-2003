import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class DatagramIterator(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpandaexpress._inPJoxtlJZb()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstDatagram_unsignedint(self, datagram, offset):
        self.this = libpandaexpress._inPJoxtEwZZ(datagram.this, offset)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstDatagram(self, datagram):
        self.this = libpandaexpress._inPJoxtz_OF(datagram.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstDatagramIterator(self, copy):
        self.this = libpandaexpress._inPJoxtZg7_(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpandaexpress and libpandaexpress._inPJoxt_5Oz:
            libpandaexpress._inPJoxt_5Oz(self.this)

    def assign(self, copy):
        returnValue = libpandaexpress._inPJoxtnHKF(self.this, copy.this)
        returnObject = DatagramIterator(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def getBool(self):
        returnValue = libpandaexpress._inPJoxthFgv(self.this)
        return returnValue

    def getInt8(self):
        returnValue = libpandaexpress._inPJoxtFX9M(self.this)
        return returnValue

    def getUint8(self):
        returnValue = libpandaexpress._inPJoxtD6SU(self.this)
        return returnValue

    def getInt16(self):
        returnValue = libpandaexpress._inPJoxtHVNl(self.this)
        return returnValue

    def getInt32(self):
        returnValue = libpandaexpress._inPJoxtFcUY(self.this)
        return returnValue

    def getInt64(self):
        returnValue = libpandaexpress._inPJoxtkKNB(self.this)
        return returnValue

    def getUint16(self):
        returnValue = libpandaexpress._inPJoxtX2ad(self.this)
        return returnValue

    def getUint32(self):
        returnValue = libpandaexpress._inPJoxtpR_A(self.this)
        return returnValue

    def getUint64(self):
        returnValue = libpandaexpress._inPJoxtFGTd(self.this)
        return returnValue

    def getFloat32(self):
        returnValue = libpandaexpress._inPJoxtvFBB(self.this)
        return returnValue

    def getFloat64(self):
        returnValue = libpandaexpress._inPJoxt0JoL(self.this)
        return returnValue

    def getBeInt16(self):
        returnValue = libpandaexpress._inPJoxtzzGa(self.this)
        return returnValue

    def getBeInt32(self):
        returnValue = libpandaexpress._inPJoxt6U9R(self.this)
        return returnValue

    def getBeInt64(self):
        returnValue = libpandaexpress._inPJoxtDdBm(self.this)
        return returnValue

    def getBeUint16(self):
        returnValue = libpandaexpress._inPJoxte_MA(self.this)
        return returnValue

    def getBeUint32(self):
        returnValue = libpandaexpress._inPJoxt6bZ7(self.this)
        return returnValue

    def getBeUint64(self):
        returnValue = libpandaexpress._inPJoxtE489(self.this)
        return returnValue

    def getBeFloat32(self):
        returnValue = libpandaexpress._inPJoxtjTRq(self.this)
        return returnValue

    def getBeFloat64(self):
        returnValue = libpandaexpress._inPJoxtisC8(self.this)
        return returnValue

    def getString(self):
        returnValue = libpandaexpress._inPJoxtxS8B(self.this)
        return returnValue

    def getZString(self):
        returnValue = libpandaexpress._inPJoxtiyF6(self.this)
        return returnValue

    def getFixedString(self, size):
        returnValue = libpandaexpress._inPJoxtnT0q(self.this, size)
        return returnValue

    def skipBytes(self, size):
        returnValue = libpandaexpress._inPJoxtTwSY(self.this, size)
        return returnValue

    def extractBytes(self, size):
        returnValue = libpandaexpress._inPJoxt3j8S(self.this, size)
        return returnValue

    def getRemainingBytes(self):
        returnValue = libpandaexpress._inPJoxt9Khi(self.this)
        return returnValue

    def getRemainingSize(self):
        returnValue = libpandaexpress._inPJoxtOxKa(self.this)
        return returnValue

    def getDatagram(self):
        returnValue = libpandaexpress._inPJoxtdg_H(self.this)
        import Datagram
        returnObject = Datagram.Datagram(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject.setPointer()
        return

    def getCurrentIndex(self):
        returnValue = libpandaexpress._inPJoxt_KNH(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                import Datagram
                if isinstance(_args[0], DatagramIterator):
                    return self.__overloaded_constructor_ptrConstDatagramIterator(_args[0])
                else:
                    if isinstance(_args[0], Datagram.Datagram):
                        return self.__overloaded_constructor_ptrConstDatagram(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <DatagramIterator> <Datagram.Datagram> '
            else:
                if numArgs == 2:
                    import Datagram
                    if isinstance(_args[0], Datagram.Datagram):
                        if isinstance(_args[1], types.IntType):
                            return self.__overloaded_constructor_ptrConstDatagram_unsignedint(_args[0], _args[1])
                        else:
                            raise TypeError, 'Invalid argument 1, expected one of: <types.IntType> '
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <Datagram.Datagram> '
                else:
                    raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 2 '

    def getArg(self, subatomicType, divisor=1):
        import DCSubatomicType
        if divisor == 1:
            if subatomicType == DCSubatomicType.STInt8:
                retVal = self.getInt8()
            else:
                if subatomicType == DCSubatomicType.STInt16:
                    retVal = self.getInt16()
                else:
                    if subatomicType == DCSubatomicType.STInt32:
                        retVal = self.getInt32()
                    else:
                        if subatomicType == DCSubatomicType.STInt64:
                            retVal = self.getInt64()
                        else:
                            if subatomicType == DCSubatomicType.STUint8:
                                retVal = self.getUint8()
                            else:
                                if subatomicType == DCSubatomicType.STUint16:
                                    retVal = self.getUint16()
                                else:
                                    if subatomicType == DCSubatomicType.STUint32:
                                        retVal = self.getUint32()
                                    else:
                                        if subatomicType == DCSubatomicType.STUint64:
                                            retVal = self.getUint64()
                                        else:
                                            if subatomicType == DCSubatomicType.STFloat64:
                                                retVal = self.getFloat64()
                                            else:
                                                if subatomicType == DCSubatomicType.STString:
                                                    retVal = self.getString()
                                                else:
                                                    if subatomicType == DCSubatomicType.STBlob:
                                                        retVal = self.getString()
                                                    else:
                                                        if subatomicType == DCSubatomicType.STInt8array:
                                                            len = self.getUint16()
                                                            retVal = []
                                                            for i in range(len):
                                                                retVal.append(self.getInt8())

                                                        else:
                                                            if subatomicType == DCSubatomicType.STInt16array:
                                                                len = self.getUint16() >> 1
                                                                retVal = []
                                                                for i in range(len):
                                                                    retVal.append(self.getInt16())

                                                            else:
                                                                if subatomicType == DCSubatomicType.STInt32array:
                                                                    len = self.getUint16() >> 2
                                                                    retVal = []
                                                                    for i in range(len):
                                                                        retVal.append(self.getInt32())

                                                                else:
                                                                    if subatomicType == DCSubatomicType.STUint8array:
                                                                        len = self.getUint16()
                                                                        retVal = []
                                                                        for i in range(len):
                                                                            retVal.append(self.getUint8())

                                                                    else:
                                                                        if subatomicType == DCSubatomicType.STUint16array:
                                                                            len = self.getUint16() >> 1
                                                                            retVal = []
                                                                            for i in range(len):
                                                                                retVal.append(self.getUint16())

                                                                        else:
                                                                            if subatomicType == DCSubatomicType.STUint32array:
                                                                                len = self.getUint16() >> 2
                                                                                retVal = []
                                                                                for i in range(len):
                                                                                    retVal.append(self.getUint32())

                                                                            else:
                                                                                if subatomicType == DCSubatomicType.STUint32uint8array:
                                                                                    len = self.getUint16() / 5
                                                                                    retVal = []
                                                                                    for i in range(len):
                                                                                        a = self.getUint32()
                                                                                        b = self.getUint8()
                                                                                        retVal.append((a, b))

                                                                                else:
                                                                                    raise Exception('Error: No such type as: ' + str(subAtomicType))
        else:
            if subatomicType == DCSubatomicType.STInt8:
                retVal = self.getInt8() / float(divisor)
            else:
                if subatomicType == DCSubatomicType.STInt16:
                    retVal = self.getInt16() / float(divisor)
                else:
                    if subatomicType == DCSubatomicType.STInt32:
                        retVal = self.getInt32() / float(divisor)
                    else:
                        if subatomicType == DCSubatomicType.STInt64:
                            retVal = self.getInt64() / float(divisor)
                        else:
                            if subatomicType == DCSubatomicType.STUint8:
                                retVal = self.getUint8() / float(divisor)
                            else:
                                if subatomicType == DCSubatomicType.STUint16:
                                    retVal = self.getUint16() / float(divisor)
                                else:
                                    if subatomicType == DCSubatomicType.STUint32:
                                        retVal = self.getUint32() / float(divisor)
                                    else:
                                        if subatomicType == DCSubatomicType.STUint64:
                                            retVal = self.getUint64() / float(divisor)
                                        else:
                                            if subatomicType == DCSubatomicType.STFloat64:
                                                retVal = self.getFloat64()
                                            else:
                                                if subatomicType == DCSubatomicType.STString:
                                                    retVal = self.getString()
                                                else:
                                                    if subatomicType == DCSubatomicType.STBlob:
                                                        retVal = self.getString()
                                                    else:
                                                        if subatomicType == DCSubatomicType.STInt8array:
                                                            len = self.getUint8() >> 1
                                                            retVal = []
                                                            for i in range(len):
                                                                retVal.append(self.getInt8() / float(divisor))

                                                        else:
                                                            if subatomicType == DCSubatomicType.STInt16array:
                                                                len = self.getUint16() >> 1
                                                                retVal = []
                                                                for i in range(len):
                                                                    retVal.append(self.getInt16() / float(divisor))

                                                            else:
                                                                if subatomicType == DCSubatomicType.STInt32array:
                                                                    len = self.getUint16() >> 2
                                                                    retVal = []
                                                                    for i in range(len):
                                                                        retVal.append(self.getInt32() / float(divisor))

                                                                else:
                                                                    if subatomicType == DCSubatomicType.STUint8array:
                                                                        len = self.getUint8() >> 1
                                                                        retVal = []
                                                                        for i in range(len):
                                                                            retVal.append(self.getUint8() / float(divisor))

                                                                    else:
                                                                        if subatomicType == DCSubatomicType.STUint16array:
                                                                            len = self.getUint16() >> 1
                                                                            retVal = []
                                                                            for i in range(len):
                                                                                retVal.append(self.getUint16() / float(divisor))

                                                                        else:
                                                                            if subatomicType == DCSubatomicType.STUint32array:
                                                                                len = self.getUint16() >> 2
                                                                                retVal = []
                                                                                for i in range(len):
                                                                                    retVal.append(self.getUint32() / float(divisor))

                                                                            else:
                                                                                if subatomicType == DCSubatomicType.STUint32uint8array:
                                                                                    len = self.getUint16() / 5
                                                                                    retVal = []
                                                                                    for i in range(len):
                                                                                        a = self.getUint32()
                                                                                        b = self.getUint8()
                                                                                        retVal.append((a / float(divisor), b / float(divisor)))

                                                                                else:
                                                                                    raise Exception('Error: No such type as: ' + str(subatomicType))
        return retVal