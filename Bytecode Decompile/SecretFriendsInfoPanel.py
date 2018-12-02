from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectObject import *
from DirectGui import *
from MultiPageTextFrame import *
import Localizer, ToontownDialog

class SecretFriendsInfoPanel(ToontownDialog.GlobalDialog):
    __module__ = __name__

    def __init__(self, doneEvent, hidePageNum=0, pageChangeCallback=None):
        ToontownDialog.GlobalDialog.__init__(self, parent=aspect2d, dialogName='secretFriendsInfoDialog', doneEvent=doneEvent, okButtonText=Localizer.BillingScreenPrivacyPolicyClose, style=ToontownDialog.Acknowledge, text='', topPad=1.5, sidePad=1.2, pos=(0, 0, 0.1), scale=0.9)
        self.textPanel = MultiPageTextFrame(parent=self, textList=Localizer.SecretFriendsInfoPanelText, hidePageNum=hidePageNum, pageChangeCallback=pageChangeCallback)
        self['image'] = self['image']
        self['image_pos'] = (0, 0, -0.1)
        self['image_scale'] = (2, 1, 1.3)
        closeButton = self.getChild(0)
        closeButton.setZ(-0.56)