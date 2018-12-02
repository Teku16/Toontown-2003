from ShowBaseGlobal import *
from DirectGui import *
import StateData, AvatarPanel, FriendSecret, ToontownGlobals, Localizer
FLPOnline = 1
FLPAll = 2
FLPEnemies = 3
leftmostPanel = FLPOnline
rightmostPanel = FLPAll
globalFriendsList = None

def showFriendsList():
    global globalFriendsList
    if globalFriendsList == None:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    return


def hideFriendsList():
    if globalFriendsList != None:
        globalFriendsList.exit()
    return


def isFriendsListShown():
    if globalFriendsList != None:
        return globalFriendsList.isEntered
    return 0
    return


def unloadFriendsList():
    global globalFriendsList
    if globalFriendsList != None:
        globalFriendsList.unload()
        globalFriendsList = None
    return


class FriendsListPanel(DirectFrame, StateData.StateData):
    __module__ = __name__

    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(FriendsListPanel)
        StateData.StateData.__init__(self, 'friends-list-done')
        self.friends = {}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.panelType = FLPOnline
        return

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1
        gui = loader.loadModelOnce('phase_3.5/models/gui/friendslist_gui')
        auxGui = loader.loadModelOnce('phase_3.5/models/gui/avatar_panel_gui')
        self.title = DirectLabel(parent=self, relief=None, text='', text_scale=0.04, text_fg=(0, 0.1, 0.4, 1), pos=(0.007, 0.0, 0.2))
        background_image = gui.find('**/FriendsBox_Open')
        self['image'] = background_image
        self.setPos(1.1, 0, 0.54)
        self.scrollList = DirectScrolledList(parent=self, relief=None, incButton_image=(gui.find('**/FndsLst_ScrollUp'), gui.find('**/FndsLst_ScrollDN'), gui.find('**/FndsLst_ScrollUp_Rllvr'), gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_pos=(0.0, 0.0, -0.316), incButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), incButton_scale=(1.0, 1.0, -1.0), decButton_image=(gui.find('**/FndsLst_ScrollUp'), gui.find('**/FndsLst_ScrollDN'), gui.find('**/FndsLst_ScrollUp_Rllvr'), gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_pos=(0.0, 0.0, 0.117), decButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), itemFrame_pos=(-0.17, 0.0, 0.06), itemFrame_relief=None, numItemsVisible=8, items=[])
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.2, 0, 0)))
        self.scrollList.attachNewNode(clipper)
        cpa = ClipPlaneAttrib.make(ClipPlaneAttrib.OSet, clipper)
        self.scrollList.node().setAttrib(cpa)
        self.close = DirectButton(parent=self, relief=None, image=(auxGui.find('**/CloseBtn_UP'), auxGui.find('**/CloseBtn_DN'), auxGui.find('**/CloseBtn_Rllvr')), pos=(0.01, 0, -0.38), command=self.__close)
        self.left = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'), gui.find('**/Horiz_Arrow_DN'), gui.find('**/Horiz_Arrow_Rllvr'), gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(-0.15, 0.0, -0.38), scale=(-1.0, 1.0, 1.0), command=self.__left)
        self.right = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'), gui.find('**/Horiz_Arrow_DN'), gui.find('**/Horiz_Arrow_Rllvr'), gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(0.17, 0, -0.38), command=self.__right)
        self.newFriend = DirectButton(parent=self, relief=None, pos=(-0.14, 0.0, 0.14), image=(auxGui.find('**/Frnds_Btn_UP'), auxGui.find('**/Frnds_Btn_DN'), auxGui.find('**/Frnds_Btn_RLVR')), text=('', Localizer.FriendsListPanelNewFriend, Localizer.FriendsListPanelNewFriend), text_scale=0.045, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(0.1, -0.085), textMayChange=0, command=self.__newFriend)
        self.secrets = DirectButton(parent=self, relief=None, pos=(0.152, 0.0, 0.14), image=(auxGui.find('**/ChtBx_ChtBtn_UP'), auxGui.find('**/ChtBx_ChtBtn_DN'), auxGui.find('**/ChtBx_ChtBtn_RLVR')), text=('', Localizer.FriendsListPanelSecrets, Localizer.FriendsListPanelSecrets), text_scale=0.045, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(-0.04, -0.085), textMayChange=0, command=self.__secrets)
        gui.removeNode()
        auxGui.removeNode()
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        del self.title
        del self.scrollList
        del self.close
        del self.left
        del self.right
        del self.friends
        DirectFrame.destroy(self)
        return

    def makeFriendButton(self, friendPair):
        friendId, flags = friendPair
        handle = toonbase.tcr.identifyFriend(friendId)
        if handle == None:
            toonbase.tcr.fillUpFriendsMap()
            return None
        friendName = handle.getName()
        colorCode = NametagGroup.CCNoChat
        if flags & ToontownGlobals.FriendChat:
            colorCode = NametagGroup.CCNormal
        fg = NametagGlobals.getNameFg(colorCode, PGButton.SInactive)
        return DirectButton(relief=None, text=friendName, text_scale=0.04, text_align=TextNode.ALeft, text_fg=fg, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0, command=self.__choseFriend, extraArgs=[friendId])
        return

    def enter(self):
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        toonbase.localToon.obscureFriendsListButton(1)
        if AvatarPanel.AvatarPanel.currentAvatarPanel:
            AvatarPanel.AvatarPanel.currentAvatarPanel.cleanup()
            AvatarPanel.AvatarPanel.currentAvatarPanel = None
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()
        self.show()
        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendOffline', self.__friendOffline)
        self.accept('friendsListChanged', self.__friendsListChanged)
        self.accept('ignoreListChanged', self.__ignoreListChanged)
        self.accept('friendsMapComplete', self.__friendsListChanged)
        return
        return

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        self.hide()
        self.ignore('friendOnline')
        self.ignore('friendOffline')
        self.ignore('friendsListChanged')
        self.ignore('ignoreListChanged')
        self.ignore('friendsMapComplete')
        toonbase.localToon.obscureFriendsListButton(-1)
        messenger.send(self.doneEvent)
        return
        return

    def __close(self):
        messenger.send('wakeup')
        self.exit()

    def __left(self):
        messenger.send('wakeup')
        if self.panelType > leftmostPanel:
            self.panelType -= 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __right(self):
        messenger.send('wakeup')
        if self.panelType < rightmostPanel:
            self.panelType += 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __secrets(self):
        messenger.send('wakeup')
        FriendSecret.showFriendSecret()

    def __newFriend(self):
        messenger.send('wakeup')
        messenger.send('friendAvatar', [None, None, None])
        return

    def __choseFriend(self, friendId):
        messenger.send('wakeup')
        handle = toonbase.tcr.identifyFriend(friendId)
        if handle != None:
            messenger.send('clickedNametag', [handle])
        return

    def __updateScrollList(self):
        if self.panelType == FLPOnline:
            newFriends = []
            for friendPair in toonbase.localToon.friendsList:
                if toonbase.tcr.isFriendOnline(friendPair[0]):
                    newFriends.append(friendPair)

        if self.panelType == FLPAll:
            newFriends = toonbase.localToon.friendsList
        newFriends = []
        for ignored in toonbase.localToon.ignoreList:
            newFriends.append((ignored, 0))

        for friendPair in self.friends.keys():
            if friendPair not in newFriends:
                friendButton = self.friends[friendPair]
                self.scrollList.removeItem(friendButton, refresh=0)
                friendButton.destroy()
                del self.friends[friendPair]

        for friendPair in newFriends:
            if friendPair not in self.friends.keys():
                friendButton = self.makeFriendButton(friendPair)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        self.scrollList.refresh()
        return

    def __updateTitle(self):
        if self.panelType == FLPOnline:
            self.title['text'] = Localizer.FriendsListPanelOnlineFriends
        else:
            if self.panelType == FLPAll:
                self.title['text'] = Localizer.FriendsListPanelAllFriends
            else:
                self.title['text'] = Localizer.FriendsListPanelIgnoredFriends
        self.title.resetFrameSize()

    def __updateArrows(self):
        if self.panelType == leftmostPanel:
            self.left['state'] = 'inactive'
        else:
            self.left['state'] = 'normal'
        if self.panelType == rightmostPanel:
            self.right['state'] = 'inactive'
        else:
            self.right['state'] = 'normal'

    def __friendOnline(self, doId):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendOffline(self, doId):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendsListChanged(self):
        if self.panelType != FLPEnemies:
            self.__updateScrollList()

    def __ignoreListChanged(self):
        if self.panelType == FLPEnemies:
            self.__updateScrollList()