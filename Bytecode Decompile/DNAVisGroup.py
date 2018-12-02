import types, libtoontown, libtoontownDowncasts, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject, DNAGroup

class DNAVisGroup(DNAGroup.DNAGroup, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libtoontownDowncasts, libpandaexpressDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConstDNAVisGroup(self, group):
        self.this = libtoontown._inPet4yKYfu(group.this)
        self.userManagesMemory = 1

    def __overloaded_constructor_atomicstring(self, initialName):
        self.this = libtoontown._inPet4y2lmR(initialName)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libtoontown._inPet4yesJI()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libtoontown and libtoontown._inPet4yfswV:
            libtoontown._inPet4yfswV(self.this)

    def getClassType():
        returnValue = libtoontown._inPet4y2LTy()
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    getClassType = staticmethod(getClassType)

    def addVisible(self, visGroupName):
        returnValue = libtoontown._inPet4yrAIa(self.this, visGroupName)
        return returnValue

    def removeVisible(self, visGroupName):
        returnValue = libtoontown._inPet4y4V81(self.this, visGroupName)
        return returnValue

    def getNumVisibles(self):
        returnValue = libtoontown._inPet4yqnTT(self.this)
        return returnValue

    def getVisibleName(self, i):
        returnValue = libtoontown._inPet4yDJX6(self.this, i)
        return returnValue

    def addSuitEdge(self, edge):
        returnValue = libtoontown._inPet4y52Hm(self.this, edge.this)
        return returnValue

    def removeSuitEdge(self, edge):
        returnValue = libtoontown._inPet4ysL9U(self.this, edge.this)
        return returnValue

    def getNumSuitEdges(self):
        returnValue = libtoontown._inPet4yDKQf(self.this)
        return returnValue

    def getSuitEdge(self, i):
        returnValue = libtoontown._inPet4yGgTQ(self.this, i)
        import DNASuitEdge
        returnObject = DNASuitEdge.DNASuitEdge(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def addBattleCell(self, cell):
        returnValue = libtoontown._inPet4yKPzx(self.this, cell.this)
        return returnValue

    def removeBattleCell(self, cell):
        returnValue = libtoontown._inPet4ynwfH(self.this, cell.this)
        return returnValue

    def getNumBattleCells(self):
        returnValue = libtoontown._inPet4yCFHg(self.this)
        return returnValue

    def getBattleCell(self, i):
        returnValue = libtoontown._inPet4ykfde(self.this, i)
        import DNABattleCell
        returnObject = DNABattleCell.DNABattleCell(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject.setPointer()
        return

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], types.StringType):
                    return self.__overloaded_constructor_atomicstring(_args[0])
                else:
                    if isinstance(_args[0], DNAVisGroup):
                        return self.__overloaded_constructor_ptrConstDNAVisGroup(_args[0])
                    else:
                        raise TypeError, 'Invalid argument 0, expected one of: <types.StringType> <DNAVisGroup> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '