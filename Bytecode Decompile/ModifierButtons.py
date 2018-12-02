import types, libpanda, libpandaDowncasts, FFIExternalObject

class ModifierButtons(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def __overloaded_constructor(self):
        self.this = libpanda._inPelboTVR4()
        self.userManagesMemory = 1

    def __overloaded_constructor_ptrConstModifierButtons(self, copy):
        self.this = libpanda._inPelboPxfU(copy.this)
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPelboLQES:
            libpanda._inPelboLQES(self.this)

    def assign(self, copy):
        returnValue = libpanda._inPelbofwyS(self.this, copy.this)
        returnObject = ModifierButtons(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        return returnObject
        return

    def eq(self, other):
        returnValue = libpanda._inPelboVhow(self.this, other.this)
        return returnValue

    def ne(self, other):
        returnValue = libpanda._inPelboig3N(self.this, other.this)
        return returnValue

    def lessThan(self, other):
        returnValue = libpanda._inPelbozaOV(self.this, other.this)
        return returnValue

    def matches(self, other):
        returnValue = libpanda._inPelbowNfr(self.this, other.this)
        return returnValue

    def addButton(self, button):
        returnValue = libpanda._inPelboSLZg(self.this, button.this)
        return returnValue

    def hasButton(self, button):
        returnValue = libpanda._inPelboNHRl(self.this, button.this)
        return returnValue

    def removeButton(self, button):
        returnValue = libpanda._inPelboluBm(self.this, button.this)
        return returnValue

    def getNumButtons(self):
        returnValue = libpanda._inPelbox9C5(self.this)
        return returnValue

    def getButton(self, index):
        returnValue = libpanda._inPelboKJca(self.this, index)
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    def buttonDown(self, button):
        returnValue = libpanda._inPelbojgE5(self.this, button.this)
        return returnValue

    def buttonUp(self, button):
        returnValue = libpanda._inPelbo3WnW(self.this, button.this)
        return returnValue

    def addEvent(self, event):
        returnValue = libpanda._inPelboenMb(self.this, event.this)
        return returnValue

    def allButtonsUp(self):
        returnValue = libpanda._inPelbofJ_1(self.this)
        return returnValue

    def __overloaded_isDown_ptrConstModifierButtons_ptrButtonHandle(self, button):
        returnValue = libpanda._inPelbo9vCj(self.this, button.this)
        return returnValue

    def __overloaded_isDown_ptrConstModifierButtons_int(self, index):
        returnValue = libpanda._inPelboucQV(self.this, index)
        return returnValue

    def isAnyDown(self):
        returnValue = libpanda._inPelboS0db(self.this)
        return returnValue

    def getPrefix(self):
        returnValue = libpanda._inPelbo9FCN(self.this)
        return returnValue

    def output(self, out):
        returnValue = libpanda._inPelbobeaY(self.this, out.this)
        return returnValue

    def write(self, out):
        returnValue = libpanda._inPelboCRR3(self.this, out.this)
        return returnValue

    def constructor(self, *_args):
        numArgs = len(_args)
        if numArgs == 0:
            return self.__overloaded_constructor()
        else:
            if numArgs == 1:
                if isinstance(_args[0], ModifierButtons):
                    return self.__overloaded_constructor_ptrConstModifierButtons(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <ModifierButtons> '
            else:
                raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 0 1 '

    def isDown(self, *_args):
        numArgs = len(_args)
        if numArgs == 1:
            import ButtonHandle
            if isinstance(_args[0], types.IntType):
                return self.__overloaded_isDown_ptrConstModifierButtons_int(_args[0])
            else:
                if isinstance(_args[0], ButtonHandle.ButtonHandle):
                    return self.__overloaded_isDown_ptrConstModifierButtons_ptrButtonHandle(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> <ButtonHandle.ButtonHandle> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '