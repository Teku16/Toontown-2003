from ShowBaseGlobal import *
from ToontownGlobals import *
import PandaObject, DirectNotifyGlobal, ToontownDialog, Localizer, ToonHeadDialog

class FriendInvitee(ToonHeadDialog.ToonHeadDialog):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInvitee')

    def __init__(self, avId, avName, avDNA, context, **kw):
        self.avId = avId
        self.avName = avName
        self.avDNA = avDNA
        self.context = context
        if len(toonbase.localToon.friendsList) >= MaxFriends:
            toonbase.tcr.friendManager.up_inviteeFriendResponse(3, self.context)
            self.context = None
            text = Localizer.FriendInviteeTooManyFriends % self.avName
            style = ToontownDialog.Acknowledge
            buttonTextList = [Localizer.FriendInviteeOK]
            command = self.__handleOhWell
        else:
            text = Localizer.FriendInviteeInvitation % self.avName
            style = ToontownDialog.TwoChoice
            buttonTextList = [Localizer.FriendInviteeOK, Localizer.FriendInviteeNo]
            command = self.__handleButton
        optiondefs = (('dialogName', 'FriendInvitee', None), ('text', text, None), ('style', style, None), ('buttonTextList', buttonTextList, None), ('command', command, None), ('image_color', (1.0, 0.89, 0.77, 1.0), None), ('geom_scale', 0.2, None), ('geom_pos', (-0.1, 0, -0.025), None), ('pad', (0.075, 0.075), None), ('topPad', 0, None), ('midPad', 0, None), ('pos', (0.45, 0, 0.75), None), ('scale', 0.75, None))
        self.defineoptions(kw, optiondefs)
        ToonHeadDialog.ToonHeadDialog.__init__(self, self.avDNA)
        self.accept('cancelFriendInvitation', self.__handleCancelFromAbove)
        self.initialiseoptions(FriendInvitee)
        self.show()
        return

    def cleanup(self):
        ToonHeadDialog.ToonHeadDialog.cleanup(self)
        self.ignore('cancelFriendInvitation')
        if self.context != None:
            toonbase.tcr.friendManager.up_inviteeFriendResponse(2, self.context)
            self.context = None
        return

    def __handleButton(self, value):
        if value == ToontownDialog.DIALOG_OK:
            toonbase.tcr.friendManager.up_inviteeFriendResponse(1, self.context)
        else:
            toonbase.tcr.friendManager.up_inviteeFriendResponse(0, self.context)
        self.context = None
        self.cleanup()
        return

    def __handleOhWell(self, value):
        self.cleanup()

    def __handleCancelFromAbove(self, context=None):
        if context == None or context == self.context:
            self.context = None
            self.cleanup()
        return