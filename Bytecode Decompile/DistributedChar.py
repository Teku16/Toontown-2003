import DistributedAvatar, Char

class DistributedChar(DistributedAvatar.DistributedAvatar, Char.Char):
    __module__ = __name__

    def __init__(self, cr):
        try:
            self.DistributedChar_initialized
        except:
            self.DistributedChar_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            Char.Char.__init__(self)

        return None
        return

    def playDialogue(self, *args):
        Char.Char.playDialogue(self, *args)

    def setHp(self, hp):
        self.hp = hp
        return None
        return