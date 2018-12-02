from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectGui import *
import StateData, string, Localizer
globalFriendSecret = None

def showFriendSecret():
    global globalFriendSecret
    if not toonbase.tcr.isPaid():
        chatMgr = toonbase.localToon.chatMgr
        chatMgr.fsm.request('unpaidChatWarning')
    else:
        if not toonbase.tcr.allowSecretChat():
            chatMgr = toonbase.localToon.chatMgr
            chatMgr.fsm.request('noSecretChatWarning')
        else:
            if globalFriendSecret == None:
                globalFriendSecret = FriendSecret()
            globalFriendSecret.enter()
    return


def hideFriendSecret():
    if globalFriendSecret != None:
        globalFriendSecret.exit()
    return


def unloadFriendSecret():
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
        globalFriendSecret = None
    return


class FriendSecret(DirectFrame, StateData.StateData):
    __module__ = __name__

    def __init__(self):
        DirectFrame.__init__(self, pos=(0, 0, 0.3), relief=None, image=getDefaultDialogGeom(), image_scale=(1.6, 1, 1.2), image_pos=(0, 0, -0.05), image_color=GlobalDialogColor, borderWidth=(0.01, 0.01))
        StateData.StateData.__init__(self, 'friend-secret-done')
        self.initialiseoptions(FriendSecret)
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        del self.introText
        del self.getSecret
        del self.enterSecretText
        del self.enterSecret
        del self.ok1
        del self.ok2
        del self.cancel
        del self.secretText
        DirectFrame.destroy(self)
        return

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1
        self.introText = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.4), scale=0.05, text=Localizer.FriendSecretIntro, text_fg=(0, 0, 0, 1), text_wordwrap=30)
        self.introText.hide()
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.getSecret = DirectButton(parent=self, relief=None, pos=(0, 0, -0.11), image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 1, 1), text=Localizer.FriendSecretGetSecret, text_scale=0.06, text_pos=(0, -0.02), command=self.__getSecret)
        self.getSecret.hide()
        self.enterSecretText = DirectLabel(parent=self, relief=None, pos=(0, 0, -0.27), scale=0.05, text=Localizer.FriendSecretEnterSecret, text_fg=(0, 0, 0, 1), text_wordwrap=30)
        self.enterSecretText.hide()
        self.enterSecret = DirectEntry(parent=self, relief=SUNKEN, scale=0.06, pos=(-0.6, 0, -0.38), frameColor=(0.8, 0.8, 0.5, 1), borderWidth=(0.1, 0.1), numLines=1, width=20, frameSize=(-0.4, 20.4, -0.4, 1.1), command=self.__enterSecret)
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()
        self.ok1 = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.6, 1, 1), text=Localizer.FriendSecretOK, text_scale=0.06, text_pos=(0, -0.02), pos=(0, 0, -0.5), command=self.__ok1)
        self.ok1.hide()
        self.ok2 = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.6, 1, 1), text=Localizer.FriendSecretOK, text_scale=0.06, text_pos=(0, -0.02), pos=(0, 0, -0.57), command=self.__ok2)
        self.ok2.hide()
        self.cancel = DirectButton(parent=self, relief=None, text=Localizer.FriendSecretCancel, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.6, 1, 1), text_scale=0.06, text_pos=(0, -0.02), pos=(0, 0, -0.57), command=self.__cancel)
        self.cancel.hide()
        self.nextText = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.3), scale=0.06, text='', text_fg=(0, 0, 0, 1), text_wordwrap=22)
        self.nextText.hide()
        self.secretText = DirectLabel(parent=self, relief=None, pos=(0, 0, -0.42), scale=0.1, text='', text_fg=(0, 0, 0, 1), text_wordwrap=30)
        self.secretText.hide()
        guiButton.removeNode()
        return

    def enter(self):
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        self.show()
        self.introText.show()
        self.getSecret.show()
        self.enterSecretText.show()
        self.enterSecret.show()
        self.ok1.show()
        self.ok2.hide()
        self.cancel.hide()
        self.nextText.hide()
        self.secretText.hide()
        chatEntry = toonbase.localToon.chatMgr.chatInputNormal.chatEntry
        self.oldFocus = chatEntry['backgroundFocus']
        chatEntry['backgroundFocus'] = 0
        self.enterSecret['focus'] = 1
        NametagGlobals.setOnscreenChatForced(1)
        return
        return

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        NametagGlobals.setOnscreenChatForced(0)
        self.__cleanupFirstPage()
        self.ignoreAll()
        self.hide()
        return
        return

    def __getSecret(self):
        if not toonbase.tcr.friendManager:
            self.notify.warning('No FriendManager available.')
            self.exit()
            return
        self.__cleanupFirstPage()
        self.nextText['text'] = Localizer.FriendSecretGettingSecret
        self.nextText.setPos(0, 0, 0.3)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        self.accept('requestSecretResponse', self.__gotSecret)
        toonbase.tcr.friendManager.up_requestSecret()

    def __gotSecret(self, result, secret):
        self.ignore('requestSecretResponse')
        if result == 1:
            self.nextText['text'] = Localizer.FriendSecretGotSecret
            self.nextText.setPos(0, 0, 0.37)
            self.secretText['text'] = secret
        else:
            self.nextText['text'] = Localizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __enterSecret(self, secret):
        self.enterSecret.set('')
        secret = string.strip(secret)
        if not secret:
            self.exit()
            return
        if not toonbase.tcr.friendManager:
            self.notify.warning('No FriendManager available.')
            self.exit()
            return
        self.__cleanupFirstPage()
        self.nextText['text'] = Localizer.FriendSecretTryingSecret
        self.nextText.setPos(0, 0, 0.3)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        self.accept('submitSecretResponse', self.__enteredSecret)
        toonbase.tcr.friendManager.up_submitSecret(secret)

    def __enteredSecret(self, result, avId):
        self.ignore('submitSecretResponse')
        if result == 1:
            handle = toonbase.tcr.identifyAvatar(avId)
            if handle != None:
                self.nextText['text'] = Localizer.FriendSecretEnteredSecretSuccess % handle.getName()
            else:
                self.accept('friendsMapComplete', self.__nowFriends, [avId])
                ready = toonbase.tcr.fillUpFriendsMap()
                if ready:
                    self.__nowFriends(avId)
                return
        else:
            if result == 0:
                self.nextText['text'] = Localizer.FriendSecretEnteredSecretUnknown
            else:
                if result == 2:
                    handle = toonbase.tcr.identifyAvatar(avId)
                    if handle != None:
                        self.nextText['text'] = Localizer.FriendSecretEnteredSecretFull % handle.getName()
                    else:
                        self.nextText['text'] = Localizer.FriendSecretEnteredSecretFullNoName
                else:
                    if result == 3:
                        self.nextText['text'] = Localizer.FriendSecretEnteredSecretSelf
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()
        return

    def __nowFriends(self, avId):
        self.ignore('friendsMapComplete')
        handle = toonbase.tcr.identifyAvatar(avId)
        if handle != None:
            self.nextText['text'] = Localizer.FriendSecretNowFriends % handle.getName()
        else:
            self.nextText['text'] = Localizer.FriendSecretNowFriendsNoName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()
        return

    def __ok1(self):
        secret = self.enterSecret.get()
        self.__enterSecret(secret)

    def __ok2(self):
        self.exit()

    def __cancel(self):
        self.exit()

    def __cleanupFirstPage(self):
        self.introText.hide()
        self.getSecret.hide()
        self.enterSecretText.hide()
        self.enterSecret.hide()
        chatEntry = toonbase.localToon.chatMgr.chatInputNormal.chatEntry
        chatEntry['backgroundFocus'] = self.oldFocus