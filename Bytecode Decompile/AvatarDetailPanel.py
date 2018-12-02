from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectGui import *
import PandaObject, FSM, State, DirectNotifyGlobal, DistributedToon, FriendInviter, TeleportPanel, Localizer
from ToontownBattleGlobals import Tracks, Levels
globalAvatarDetail = None

def showAvatarDetail(avId, avName):
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    globalAvatarDetail = AvatarDetailPanel(avId, avName)
    return


def hideAvatarDetail():
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    return


def unloadAvatarDetail():
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    return


class AvatarDetailPanel(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarDetailPanel')

    def __init__(self, avId, avName, parent=aspect2d, **kw):
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModelOnce('phase_3.5/models/gui/avatar_panel_gui')
        detailPanel = gui.find('**/avatarInfoPanel')
        optiondefs = (
         (
          'pos', (0.525, 0.0, 0.525), None), ('scale', 0.5, None), ('relief', None, None), ('image', detailPanel, None), ('image_color', GlobalDialogColor, None), ('text', '', None), ('text_wordwrap', 10.4, None), ('text_scale', 0.132, None), ('text_pos', (0.0, 0.75), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.dataText = DirectLabel(self, text='', text_scale=0.09, text_align=TextNode.ALeft, text_wordwrap=15, relief=None, pos=(-0.7, 0.0, 0.5))
        self.avId = avId
        self.avName = avName
        self.avatar = None
        self.createdAvatar = None
        self.fsm = FSM.FSM('AvatarDetailPanel', [
         State.State('off', self.enterOff, self.exitOff, [
          'begin']),
         State.State('begin', self.enterBegin, self.exitBegin, [
          'query', 'data', 'off']),
         State.State('query', self.enterQuery, self.exitQuery, [
          'data', 'invalid', 'off']),
         State.State('data', self.enterData, self.exitData, [
          'off']),
         State.State('invalid', self.enterInvalid, self.exitInvalid, [
          'off'])], 'off', 'off')
        TeleportPanel.hideTeleportPanel()
        FriendInviter.hideFriendInviter()
        self.bCancel = DirectButton(self, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text=Localizer.AvatarDetailPanelCancel, text_scale=0.05, text_pos=(0.12, -0.01), pos=(-0.68, 0.0, -0.76), scale=2.0, command=self.__handleCancel)
        self.bCancel.hide()
        self.initialiseoptions(AvatarDetailPanel)
        self.fsm.enterInitialState()
        self.fsm.request('begin')
        buttons.removeNode()
        gui.removeNode()
        return

    def cleanup(self):
        if self.fsm:
            self.fsm.request('off')
            self.fsm = None
            toonbase.tcr.cancelAvatarDetailsRequest(self.avatar)
        if self.createdAvatar:
            self.avatar.delete()
            self.createdAvatar = None
        self.destroy()
        return

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterBegin(self):
        myId = toonbase.localToon.doId
        self['text'] = self.avName
        if self.avId == myId:
            self.avatar = toonbase.localToon
            self.createdAvatar = 0
            self.fsm.request('data')
        else:
            self.fsm.request('query')

    def exitBegin(self):
        pass

    def enterQuery(self):
        self.dataText['text'] = Localizer.AvatarDetailPanelLookup % self.avName
        self.bCancel.show()
        if toonbase.tcr.doId2do.has_key(self.avId):
            self.avatar = toonbase.tcr.doId2do[self.avId]
            self.createdAvatar = 0
        else:
            self.avatar = DistributedToon.DistributedToon(toonbase.tcr)
            self.createdAvatar = 1
            self.avatar.doId = self.avId
        toonbase.tcr.getAvatarDetails(self.avatar, self.__handleAvatarDetails)

    def exitQuery(self):
        self.bCancel.hide()

    def enterData(self):
        self.bCancel['text'] = Localizer.AvatarDetailPanelClose
        self.bCancel.show()
        self.__showData()

    def exitData(self):
        self.bCancel.hide()

    def enterInvalid(self):
        self.dataText['text'] = Localizer.AvatarDetailPanelFailedLookup % self.avName

    def exitInvalid(self):
        self.bCancel.hide()

    def __handleCancel(self):
        unloadAvatarDetail()

    def __handleAvatarDetails(self, gotData, avatar):
        if not self.fsm or avatar != self.avatar:
            self.notify.warning('Ignoring unexpected request for avatar %s' % avatar.doId)
            return
        if gotData:
            self.fsm.request('data')
        else:
            self.fsm.request('invalid')

    def __showData(self):
        av = self.avatar
        online = 1
        if toonbase.tcr.isFriend(self.avId):
            online = toonbase.tcr.isFriendOnline(self.avId)
        if online:
            text = Localizer.AvatarDetailPanelOnline % {'district': toonbase.tcr.getShardName(av.defaultShard), 'location': toonbase.tcr.hoodMgr.getFullnameFromId(av.lastHood)}
        else:
            text = Localizer.AvatarDetailPanelOffline
        self.dataText['text'] = text
        self.__updateTrackInfo()
        self.__updateTrophyInfo()
        self.__updateLaffInfo()

    def __updateLaffInfo(self):
        avatar = self.avatar
        messenger.send('updateLaffMeter', [
         avatar, avatar.hp, avatar.maxHp])

    def __updateTrackInfo(self):
        xOffset = -0.321814
        xSpacing = 0.18636280298233032
        yOffset = 0.19352
        ySpacing = -0.12625433504581451
        inventory = self.avatar.inventory
        inventoryModels = loader.loadModelOnce('phase_3.5/models/gui/inventory_gui')
        buttonModel = inventoryModels.find('**/InventoryButtonUp')
        for track in range(0, len(Tracks)):
            DirectLabel(parent=self, relief=None, text=string.upper(Localizer.BattleGlobalTracks[track]), text_scale=0.066, text_align=TextNode.ALeft, pos=(-0.71, 0, 0.17 + track * ySpacing))
            if self.avatar.hasTrackAccess(track):
                curExp, nextExp = inventory.getCurAndNextExpValues(track)
                for item in range(0, len(Levels[track])):
                    level = Levels[track][item]
                    if curExp >= level:
                        numItems = inventory.numItem(track, item)
                        if numItems == 0:
                            image_color = Vec4(0.5, 0.5, 0.5, 1)
                            geom_color = Vec4(0.2, 0.2, 0.2, 0.5)
                        else:
                            image_color = Vec4(0, 0.6, 1, 1)
                            geom_color = None
                        DirectLabel(parent=self, image=buttonModel, image_scale=(0.92, 1, 1), image_color=image_color, geom=inventory.invModels[track][item], geom_color=geom_color, geom_scale=0.6, relief=None, pos=(xOffset + item * xSpacing, 0, yOffset + track * ySpacing))
                    else:
                        break

        return

    def __updateTrophyInfo(self):
        if self.createdAvatar:
            return
        if self.avatar.trophyScore >= TrophyStarLevels[2]:
            color = TrophyStarColors[2]
        else:
            if self.avatar.trophyScore >= TrophyStarLevels[1]:
                color = TrophyStarColors[1]
            else:
                if self.avatar.trophyScore >= TrophyStarLevels[0]:
                    color = TrophyStarColors[0]
                else:
                    color = None
        if color:
            gui = loader.loadModelOnce('phase_3.5/models/gui/avatar_panel_gui')
            star = gui.find('**/avatarStar')
            self.star = DirectLabel(parent=self, image=star, image_color=color, pos=(0.610165, 0, -0.760678), scale=0.9, relief=None)
            gui.removeNode()
        return