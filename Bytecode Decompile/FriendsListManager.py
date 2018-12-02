from PandaModules import *
import FriendsListPanel, FriendInviter, FriendInvitee, TeleportPanel, FriendSecret, AvatarPanel, AvatarDetailPanel, ToontownGlobals

class FriendsListManager:
    __module__ = __name__

    def __init__(self):
        self.avatarPanel = None
        return None
        return

    def load(self):
        return None
        return

    def unload(self):
        if self.avatarPanel:
            del self.avatarPanel
        FriendInviter.unloadFriendInviter()
        AvatarDetailPanel.unloadAvatarDetail()
        TeleportPanel.unloadTeleportPanel()
        return None
        return

    def enter(self):
        self.accept('openFriendsList', self.__openFriendsList)
        self.accept('clickedNametag', self.__handleClickedNametag)
        toonbase.localToon.setFriendsListButtonActive(1)
        NametagGlobals.setMasterNametagsActive(1)
        self.accept('gotoAvatar', self.__handleGotoAvatar)
        self.accept('friendAvatar', self.__handleFriendAvatar)
        self.accept('avatarDetails', self.__handleAvatarDetails)
        self.accept('friendInvitation', self.__handleFriendInvitation)
        if toonbase.tcr.friendManager:
            toonbase.tcr.friendManager.setAvailable(1)
        return None
        return

    def exit(self):
        self.ignore('openFriendsList')
        self.ignore('clickedNametag')
        toonbase.localToon.setFriendsListButtonActive(0)
        NametagGlobals.setMasterNametagsActive(0)
        if self.avatarPanel:
            self.avatarPanel.cleanup()
            self.avatarPanel = None
        self.ignore('gotoAvatar')
        self.ignore('friendAvatar')
        self.ignore('avatarDetails')
        FriendsListPanel.hideFriendsList()
        FriendSecret.hideFriendSecret()
        if toonbase.tcr.friendManager:
            toonbase.tcr.friendManager.setAvailable(0)
        self.ignore('friendInvitation')
        FriendInviter.hideFriendInviter()
        AvatarDetailPanel.hideAvatarDetail()
        TeleportPanel.hideTeleportPanel()
        return None
        return

    def __openFriendsList(self):
        FriendsListPanel.showFriendsList()
        return None
        return

    def __handleClickedNametag(self, avatar):
        self.avatarPanel = AvatarPanel.AvatarPanel(avatar)

    def __handleGotoAvatar(self, avId, avName, avDisableName):
        TeleportPanel.showTeleportPanel(avId, avName, avDisableName)
        return None
        return

    def __handleFriendAvatar(self, avId, avName, avDisableName):
        FriendInviter.showFriendInviter(avId, avName, avDisableName)
        return None
        return

    def __handleFriendInvitation(self, avId, avName, dna, context):
        FriendInvitee.FriendInvitee(avId, avName, dna, context)
        return None
        return

    def __handleAvatarDetails(self, avId, avName):
        AvatarDetailPanel.showAvatarDetail(avId, avName)
        return None
        return