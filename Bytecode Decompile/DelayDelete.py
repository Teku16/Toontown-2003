

class DelayDelete:
    __module__ = __name__

    def __init__(self, distObj):
        self.distObj = distObj
        self.distObj.delayDelete(1)

    def __del__(self):
        self.distObj.delayDelete(0)