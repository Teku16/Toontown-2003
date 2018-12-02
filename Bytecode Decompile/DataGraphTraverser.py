import types, libpanda, libpandaDowncasts, FFIExternalObject

class DataGraphTraverser(FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpanda._inPSLSe6KPF()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()

    def destructor(self):
        if libpanda and libpanda._inPSLSelC6u:
            libpanda._inPSLSelC6u(self.this)

    def traverse(self, node):
        returnValue = libpanda._inPSLSePaYd(self.this, node.this)
        return returnValue

    def traverseBelow(self, node, output):
        returnValue = libpanda._inPSLSekThv(self.this, node.this, output.this)
        return returnValue

    def collectLeftovers(self):
        returnValue = libpanda._inPSLSe8nIW(self.this)
        return returnValue