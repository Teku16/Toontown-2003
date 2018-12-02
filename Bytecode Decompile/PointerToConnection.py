import types, libpanda, libpandaDowncasts, FFIExternalObject, PointerToBaseConnection

class PointerToConnection(PointerToBaseConnection.PointerToBaseConnection, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor_ptrConnection(self, ptr):
        self.this = libpanda._inP9ImMOLs6(ptr.this)
        self.userManagesMemory = 1

    def __overloaded_constructor(self):
        self.this = libpanda._inP9ImM_abX()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConnection(self, copy):
        self.this = libpanda._inP9ImMZI1Q(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inP9ImM0UfE:
            libpanda._inP9ImM0UfE(self.this)

    def p(self):
        returnValue = libpanda._inP9ImMAt8x(self.this)
        import Connection
        returnObject = Connection.Connection(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def __overloaded_assign_ptrPointerToConnection_ptrConnection(self, ptr):
        returnValue = libpanda._inP9ImMKFDQ(self.this, ptr.this)
        returnObject = PointerToConnection(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def __overloaded_assign_ptrPointerToConnection_ptrConnection(self, copy):
        returnValue = libpanda._inP9ImMvpYV(self.this, copy.this)
        returnObject = PointerToConnection(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def isNull(self):
        returnValue = libpanda._inP9ImMiZMY(self.this)
        return returnValue

    def clear(self):
        returnValue = libpanda._inP9ImMZ1xp(self.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                import Connection
                if isinstance(_args[0], Connection.Connection):
                    return self.__overloaded_constructor_ptrConnection(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <Connection.Connection> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def assign(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import Connection
            if isinstance(_args[0], Connection.Connection):
                return self.__overloaded_assign_ptrPointerToConnection_ptrConnection(_args[0])
            else:
                raise TypeError, 'Invalid argument 0, expected one of: <Connection.Connection> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '