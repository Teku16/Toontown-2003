import types, libpandaexpress, Iostream, Ostream, TypedReferenceCount, ReferenceCount

def downcastToIostreamFromOstream(this):
    returnValue = libpandaexpress._inPJoxtAU9t(this.this)
    import Iostream
    returnObject = Iostream.Iostream(None)
    returnObject.this = returnValue
    if returnObject.this == 0:
        return None
    return returnObject
    return


def downcastToTypedReferenceCountFromReferenceCount(this):
    returnValue = libpandaexpress._inPJoxtvWXj(this.this)
    import TypedReferenceCount
    returnObject = TypedReferenceCount.TypedReferenceCount(None)
    returnObject.this = returnValue
    if returnObject.this == 0:
        return None
    returnObject.userManagesMemory = 1
    return returnObject
    return