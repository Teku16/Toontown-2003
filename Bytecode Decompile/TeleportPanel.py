from ShowBaseGlobal import *
from DirectGui import *
import ToontownGlobals, PandaObject, FSM, State, DirectNotifyGlobal, FriendInviter, AvatarDetailPanel, Localizer
globalTeleport = None

def showTeleportPanel(avId, avName, avDisableName):
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    globalTeleport = TeleportPanel(avId, avName, avDisableName)
    return


def hideTeleportPanel():
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    return


def unloadTeleportPanel():
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    return


class TeleportPanel(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TeleportPanel')

    def __init__(self, avId, avName, avDisableName):
        DirectFrame.__init__(self, pos=(0.3, 0.1, 0.65), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.0, 1.0, 0.6), text='', text_wordwrap=13.5, text_scale=0.06, text_pos=(0.0, 0.18))
        self['image'] = getDefaultDialogGeom()
        self.avId = avId
        self.avName = avName
        self.avDisableName = avDisableName
        self.fsm = FSM.FSM('TeleportPanel', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('begin', self.enterBegin, self.exitBegin),
         State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
         State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
         State.State('ignored', self.enterIgnored, self.exitIgnored),
         State.State('notOnline', self.enterNotOnline, self.exitNotOnline),
         State.State('wentAway', self.enterWentAway, self.exitWentAway),
         State.State('self', self.enterSelf, self.exitSelf),
         State.State('unknownHood', self.enterUnknownHood, self.exitUnknownHood),
         State.State('unavailableHood', self.enterUnavailableHood, self.exitUnavailableHood),
         State.State('otherShard', self.enterOtherShard, self.exitOtherShard),
         State.State('teleport', self.enterTeleport, self.exitTeleport)], 'off', 'off')
        FriendInviter.hideFriendInviter()
        AvatarDetailPanel.hideAvatarDetail()
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        self.bOk = DirectButton(self, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief=None, text='OK', text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.__handleOk)
        self.bOk.hide()
        self.bCancel = DirectButton(self, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text='Cancel', text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.__handleCancel)
        self.bCancel.hide()
        self.bYes = DirectButton(self, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief=None, text='Yes', text_scale=0.05, text_pos=(0.0, -0.1), pos=(-0.15, 0.0, -0.15), command=self.__handleYes)
        self.bYes.hide()
        self.bNo = DirectButton(self, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text='No', text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.15, 0.0, -0.15), command=self.__handleNo)
        self.bNo.hide()
        buttons.removeNode()
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.show()
        self.fsm.enterInitialState()
        self.fsm.request('begin')
        return

    def cleanup(self):
        self.fsm.request('off')
        del self.fsm
        self.ignore(self.avDisableName)
        self.destroy()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterBegin(self):
        myId = toonbase.localToon.doId
        if self.avId == myId:
            self.fsm.request('self')
        else:
            if toonbase.tcr.doId2do.has_key(self.avId):
                self.fsm.request('checkAvailability')
            else:
                if toonbase.tcr.isFriend(self.avId):
                    if toonbase.tcr.isFriendOnline(self.avId):
                        self.fsm.request('checkAvailability')
                    else:
                        self.fsm.request('notOnline')
                else:
                    self.fsm.request('wentAway')

    def exitBegin(self):
        pass

    def enterCheckAvailability(self):
        myId = toonbase.localToon.getDoId()
        toonbase.localToon.d_teleportQuery(myId, sendToId=self.avId)
        self['text'] = Localizer.TeleportPanelCheckAvailability % self.avName
        self.accept('teleportResponse', self.__teleportResponse)
        self.bCancel.show()

    def exitCheckAvailability(self):
        self.ignore('teleportResponse')
        self.bCancel.hide()

    def enterNotAvailable(self):
        self['text'] = Localizer.TeleportPanelNotAvailable % self.avName
        self.bOk.show()

    def exitNotAvailable(self):
        self.bOk.hide()

    def enterIgnored(self):
        self['text'] = Localizer.TeleportPanelIgnored % self.avName
        self.bOk.show()

    def exitIgnored(self):
        self.bOk.hide()

    def enterNotOnline(self):
        self['text'] = Localizer.TeleportPanelNotOnline % self.avName
        self.bOk.show()

    def exitNotOnline(self):
        self.bOk.hide()

    def enterWentAway(self):
        self['text'] = Localizer.TeleportPanelWentAway % self.avName
        self.bOk.show()

    def exitWentAway(self):
        self.bOk.hide()

    def enterUnknownHood(self, hoodId):
        self['text'] = Localizer.TeleportPanelUnknownHood % toonbase.tcr.hoodMgr.getFullnameFromId(hoodId)
        self.bOk.show()

    def exitUnknownHood(self):
        self.bOk.hide()

    def enterUnavailableHood(self, hoodId):
        self['text'] = Localizer.TeleportPanelUnavailableHood % toonbase.tcr.hoodMgr.getFullnameFromId(hoodId)
        self.bOk.show()

    def exitUnavailableHood(self):
        self.bOk.hide()

    def enterSelf(self):
        self['text'] = Localizer.TeleportPanelDenySelf
        self.bOk.show()

    def exitSelf(self):
        self.bOk.hide()

    def enterOtherShard(self, shardId, hoodId, zoneId):
        shardName = toonbase.tcr.getShardName(shardId)
        myShardName = toonbase.tcr.getShardName(toonbase.localToon.defaultShard)
        self['text'] = Localizer.TeleportPanelOtherShard % {'avName': self.avName, 'shardName': shardName, 'myShardName': myShardName}
        self.bYes.show()
        self.bNo.show()
        self.shardId = shardId
        self.hoodId = hoodId
        self.zoneId = zoneId

    def exitOtherShard(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterTeleport(self, shardId, hoodId, zoneId):
        if toonbase.localToon.teleportCheat:
            hoodsVisited = ToontownGlobals.Hoods
        else:
            hoodsVisited = toonbase.localToon.hoodsVisited
        if hoodId == ToontownGlobals.MyEstate:
            if shardId == toonbase.localToon.defaultShard:
                shardId = None
            place = toonbase.tcr.playGame.getPlace()
            place.requestTeleport(hoodId, zoneId, shardId, self.avId)
            unloadTeleportPanel()
        else:
            if hoodId not in hoodsVisited:
                self.fsm.request('unknownHood', [hoodId])
            else:
                if hoodId not in toonbase.tcr.hoodMgr.getAvailableZones():
                    print 'hoodId %d not ready' % hoodId
                    self.fsm.request('unavailableHood', [hoodId])
                else:
                    if shardId != toonbase.localToon.defaultShard:
                        toonbase.localToon.reparentTo(hidden)
                        toonbase.tcr.gameFSM.request('waitOnEnterResponses', [
                         shardId, hoodId, zoneId, self.avId])
                    else:
                        if shardId == toonbase.localToon.defaultShard:
                            shardId = None
                        place = toonbase.tcr.playGame.getPlace()
                        place.requestTeleport(hoodId, zoneId, shardId, self.avId)
                        unloadTeleportPanel()
        return
        return

    def exitTeleport(self):
        pass

    def __handleOk(self):
        unloadTeleportPanel()

    def __handleCancel(self):
        unloadTeleportPanel()

    def __handleYes(self):
        self.fsm.request('teleport', [self.shardId, self.hoodId, self.zoneId])

    def __handleNo(self):
        unloadTeleportPanel()

    def __teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        if avId != self.avId:
            return
        if available == 0:
            self.fsm.request('notAvailable')
        else:
            if available == 2:
                self.fsm.request('ignored')
            else:
                if shardId != toonbase.localToon.defaultShard:
                    self.fsm.request('otherShard', [shardId, hoodId, zoneId])
                else:
                    self.fsm.request('teleport', [shardId, hoodId, zoneId])

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')