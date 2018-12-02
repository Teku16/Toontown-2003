import types, libpandaphysics, libpandaphysicsDowncasts, FFIExternalObject, AngularIntegrator

class AngularEulerIntegrator(AngularIntegrator.AngularIntegrator, FFIExternalObject.FFIExternalObject):
    __module__ = __name__
    __CModuleDowncasts__ = [libpandaphysicsDowncasts]

    def __init__(self, *_args):
        FFIExternalObject.FFIExternalObject.__init__(self)
        if len(_args) == 1 and _args[0] == None:
            return
        apply(self.constructor, _args)
        return

    def constructor(self):
        self.this = libpandaphysics._inP9fJJ4P7V()
        self.userManagesMemory = 1

    def __del__(self):
        if self.userManagesMemory and self.this != 0:
            self.destructor()