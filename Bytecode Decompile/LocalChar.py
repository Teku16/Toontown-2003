from PandaObject import *
import DistributedChar, LocalAvatar, ChatManager, Char

class LocalChar(DistributedChar.DistributedChar, LocalAvatar.LocalAvatar):
    __module__ = __name__

    def __init__(self, cr):
        try:
            self.LocalChar_initialized
        except:
            self.LocalChar_initialized = 1
            DistributedChar.DistributedChar.__init__(self, cr)
            LocalAvatar.LocalAvatar.__init__(self, cr)
            self.setNameVisible(0)
            Char.initializeDialogue()

        return None
        return