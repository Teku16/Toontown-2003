from ShowBase import *
ShowBase()
directNotify.setDconfigLevels()

def inspect(anObject):
    import Inspector
    return Inspector.inspect(anObject)


__builtins__['inspect'] = inspect