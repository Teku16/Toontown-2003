import types, libpanda, libpandaDowncasts, FFIExternalObject

class KeyboardButton(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

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
        if libpanda and libpanda._inPelbotf0c:
            libpanda._inPelbotf0c(self.this)

    def __overloaded_asciiKey_atomicstring(asciiEquivalent):
        returnValue = libpanda._inPelboubDB(asciiEquivalent)
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_asciiKey_atomicstring = staticmethod(__overloaded_asciiKey_atomicstring)

    def __overloaded_asciiKey_char(asciiEquivalent):
        returnValue = libpanda._inPelboc5oq(asciiEquivalent)
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    __overloaded_asciiKey_char = staticmethod(__overloaded_asciiKey_char)

    def space():
        returnValue = libpanda._inPelbowvOd()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    space = staticmethod(space)

    def backspace():
        returnValue = libpanda._inPelbo3Fyx()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    backspace = staticmethod(backspace)

    def tab():
        returnValue = libpanda._inPelboKuf_()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    tab = staticmethod(tab)

    def enter():
        returnValue = libpanda._inPelbogDap()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    enter = staticmethod(enter)

    def escape():
        returnValue = libpanda._inPelborLDY()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    escape = staticmethod(escape)

    def f1():
        returnValue = libpanda._inPelbo0OGt()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f1 = staticmethod(f1)

    def f2():
        returnValue = libpanda._inPelbo2OUJ()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f2 = staticmethod(f2)

    def f3():
        returnValue = libpanda._inPelbozOil()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f3 = staticmethod(f3)

    def f4():
        returnValue = libpanda._inPelbo9OwB()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f4 = staticmethod(f4)

    def f5():
        returnValue = libpanda._inPelbo_O_d()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f5 = staticmethod(f5)

    def f6():
        returnValue = libpanda._inPelbo4OM6()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f6 = staticmethod(f6)

    def f7():
        returnValue = libpanda._inPelbo6OaW()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f7 = staticmethod(f7)

    def f8():
        returnValue = libpanda._inPelbonOoy()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f8 = staticmethod(f8)

    def f9():
        returnValue = libpanda._inPelbohO2O()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f9 = staticmethod(f9)

    def f10():
        returnValue = libpanda._inPelboLFnR()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f10 = staticmethod(f10)

    def f11():
        returnValue = libpanda._inPelboZanY()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f11 = staticmethod(f11)

    def f12():
        returnValue = libpanda._inPelbovbnf()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    f12 = staticmethod(f12)

    def left():
        returnValue = libpanda._inPelbohrB1()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    left = staticmethod(left)

    def right():
        returnValue = libpanda._inPelboUHch()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    right = staticmethod(right)

    def up():
        returnValue = libpanda._inPelbopoHo()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    up = staticmethod(up)

    def down():
        returnValue = libpanda._inPelbof_Gf()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    down = staticmethod(down)

    def pageUp():
        returnValue = libpanda._inPelbo7XIX()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    pageUp = staticmethod(pageUp)

    def pageDown():
        returnValue = libpanda._inPelboQsHF()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    pageDown = staticmethod(pageDown)

    def home():
        returnValue = libpanda._inPelbor4iM()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    home = staticmethod(home)

    def end():
        returnValue = libpanda._inPelbo2_Fy()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    end = staticmethod(end)

    def insert():
        returnValue = libpanda._inPelboLmkh()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    insert = staticmethod(insert)

    def _del():
        returnValue = libpanda._inPelboZsPn()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    _del = staticmethod(_del)

    def shift():
        returnValue = libpanda._inPelbo0QFY()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    shift = staticmethod(shift)

    def control():
        returnValue = libpanda._inPelbon_Xd()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    control = staticmethod(control)

    def alt():
        returnValue = libpanda._inPelboaaIW()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    alt = staticmethod(alt)

    def meta():
        returnValue = libpanda._inPelbowAt7()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    meta = staticmethod(meta)

    def capsLock():
        returnValue = libpanda._inPelbomQ06()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    capsLock = staticmethod(capsLock)

    def shiftLock():
        returnValue = libpanda._inPelboJGms()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    shiftLock = staticmethod(shiftLock)

    def numLock():
        returnValue = libpanda._inPelboUJca()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    numLock = staticmethod(numLock)

    def scrollLock():
        returnValue = libpanda._inPelbok1PW()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    scrollLock = staticmethod(scrollLock)

    def printScreen():
        returnValue = libpanda._inPelboetDN()
        import ButtonHandle
        returnObject = ButtonHandle.ButtonHandle(None)
        returnObject.this = returnValue
        if returnObject.this == 0:
            return None
        returnObject.userManagesMemory = 1
        return returnObject
        return

    printScreen = staticmethod(printScreen)

    def asciiKey(*_args):
        numArgs = len(_args)
        if numArgs == 1:
            if isinstance(_args[0], types.IntType):
                return KeyboardButton.__overloaded_asciiKey_char(_args[0])
            else:
                if isinstance(_args[0], types.StringType):
                    return KeyboardButton.__overloaded_asciiKey_atomicstring(_args[0])
                else:
                    raise TypeError, 'Invalid argument 0, expected one of: <types.IntType> <types.StringType> '
        else:
            raise TypeError, 'Invalid number of arguments: ' + `numArgs` + ', expected one of: 1 '

    asciiKey = staticmethod(asciiKey)