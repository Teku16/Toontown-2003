from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectObject import *
from DirectGui import *
from MultiPageTextFrame import *
import Localizer, ToontownDialog

class PrivacyPolicyPanel(ToontownDialog.GlobalDialog):
    __module__ = __name__

    def __init__(self, doneEvent, hidePageNum=0, pageChangeCallback=None):
        ToontownDialog.GlobalDialog.__init__(self, parent=aspect2d, dialogName='privacyPolicyDialog', doneEvent=doneEvent, okButtonText=Localizer.BillingScreenPrivacyPolicyClose, style=ToontownDialog.Acknowledge, text='', topPad=1.5, sidePad=1.2, pos=(0, 0, -0.55), scale=0.9)
        self.privacyPolicyText = MultiPageTextFrame(parent=self, textList=Localizer.BillingScreenPrivacyPolicyText, hidePageNum=hidePageNum, pageChangeCallback=pageChangeCallback, pos=(0, 0, 0.7), width=2.4, height=1.5)
        self['image'] = self['image']
        self['image_pos'] = (0, 0, 0.65)
        self['image_scale'] = (2.7, 1, 1.9)
        closeButton = self.getChild(0)
        closeButton.setZ(-0.13)