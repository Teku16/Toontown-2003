import types, libpandaexpress, libpandaexpressDowncasts, FFIExternalObject

class TypeRegistry(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaexpressDowncasts]

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
        if libpandaexpress and libpandaexpress._inPJoxtxkrK:
            libpandaexpress._inPJoxtxkrK(self.this)

    def reregisterTypes():
        returnValue = libpandaexpress._inPJoxt6_p8()
        return returnValue

    reregisterTypes = staticmethod(reregisterTypes)

    def ptr():
        returnValue = libpandaexpress._inPJoxtuwsa()
        returnObject = TypeRegistry(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    ptr = staticmethod(ptr)

    def findType(self, name):
        returnValue = libpandaexpress._inPJoxtw9n6(self.this, name)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getName(self, type, object):
        returnValue = libpandaexpress._inPJoxt5DEU(self.this, type.this, object.this)
        return returnValue

    def isDerivedFrom(self, child, base, childObject):
        returnValue = libpandaexpress._inPJoxtDBOu(self.this, child.this, base.this, childObject.this)
        return returnValue

    def getNumRootClasses(self):
        returnValue = libpandaexpress._inPJoxtOxO1(self.this)
        return returnValue

    def getRootClass(self, n):
        returnValue = libpandaexpress._inPJoxtLFNI(self.this, n)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getNumParentClasses(self, child, childObject):
        returnValue = libpandaexpress._inPJoxtlx7d(self.this, child.this, childObject.this)
        return returnValue

    def getParentClass(self, child, index):
        returnValue = libpandaexpress._inPJoxt4LWH(self.this, child.this, index)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getNumChildClasses(self, child, childObject):
        returnValue = libpandaexpress._inPJoxtmVbL(self.this, child.this, childObject.this)
        return returnValue

    def getChildClass(self, child, index):
        returnValue = libpandaexpress._inPJoxtfTRM(self.this, child.this, index)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def getParentTowards(self, child, base, childObject):
        returnValue = libpandaexpress._inPJoxt0YQ7(self.this, child.this, base.this, childObject.this)
        import TypeHandle
        returnObject = TypeHandle.TypeHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def write(self, out):
        returnValue = libpandaexpress._inPJoxteZEC(self.this, out.this)
        return returnValue