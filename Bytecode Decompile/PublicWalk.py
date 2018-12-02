from ShowBaseGlobal import *
from ToontownGlobals import *
import DirectNotifyGlobal, Walk, FriendsListManager

class PublicWalk(Walk.Walk, FriendsListManager.FriendsListManager):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PublicWalk')

    def __init__(self, parentFSM, doneEvent):
        Walk.Walk.__init__(self, doneEvent)
        FriendsListManager.FriendsListManager.__init__(self)
        self.parentFSM = parentFSM

    def load(self):
        Walk.Walk.load(self)
        FriendsListManager.FriendsListManager.load(self)

    def unload(self):
        Walk.Walk.unload(self)
        FriendsListManager.FriendsListManager.unload(self)
        del self.parentFSM

    def enter(self, slowWalk=0):
        Walk.Walk.enter(self, slowWalk)
        FriendsListManager.FriendsListManager.enter(self)
        toonbase.localToon.book.showButton()
        self.accept(StickerBookHotkey, self.__handleStickerBookEntry)
        self.accept('enterStickerBook', self.__handleStickerBookEntry)
        self.accept(OptionsPageHotkey, self.__handleOptionsEntry)
        toonbase.localToon.laffMeter.start()

    def exit(self):
        Walk.Walk.exit(self)
        FriendsListManager.FriendsListManager.exit(self)
        toonbase.localToon.book.hideButton()
        self.ignore(StickerBookHotkey)
        self.ignore('enterStickerBook')
        self.ignore(OptionsPageHotkey)
        toonbase.localToon.laffMeter.stop()

    def __handleStickerBookEntry(self):
        if toonbase.localToon.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'StickerBook'
            messenger.send(self.doneEvent, [doneStatus])
            return

    def __handleOptionsEntry(self):
        if toonbase.localToon.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'Options'
            messenger.send(self.doneEvent, [doneStatus])
            return