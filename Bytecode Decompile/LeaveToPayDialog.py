import ToontownGlobals, Localizer
from DirectGui import *

class LeaveToPayDialog:
    __module__ = __name__

    def __init__(self, destructorHook=None):
        self.destructorHook = destructorHook
        self.dialog = None
        self.okHandler = self.__handleLeaveToPayOK
        self.cancelHandler = self.__handleLeaveToPayCancel
        return

    def setOK(self, handler):
        self.okHandler = handler

    def setCancel(self, handler):
        self.cancelHandler = handler

    def show(self):
        if self.dialog == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (
             buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            self.dialog = DirectFrame(pos=(0.0, 0.1, 0.2), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(0.9, 1.0, 0.5), text=Localizer.LeaveToPay, text_align=TextNode.ALeft, text_wordwrap=14, text_scale=0.06, text_pos=(-0.4, 0.15), textMayChange=0)
            DirectButton(self.dialog, image=okButtonImage, relief=None, text=Localizer.LeaveToPayYes, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.3, 0.0, -0.1), command=self.okHandler)
            DirectButton(self.dialog, image=cancelButtonImage, relief=None, text=Localizer.LeaveToPayNo, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.3, 0.0, -0.1), command=self.cancelHandler)
            buttons.removeNode()
        self.dialog.show()
        return

    def hide(self):
        self.dialog.hide()

    def destroy(self):
        if self.destructorHook:
            self.destructorHook()
        if self.dialog:
            self.dialog.hide()
            self.dialog.destroy()
        self.destructorHook
        self.dialog = None
        self.okHandler = None
        self.cancelHandler = None
        return

    def __handleLeaveToPayOK(self):
        self.destroy()
        if launcher:
            launcher.setRegistry('EXIT_PAGE', 'purchase')
        toonbase.tcr.loginFSM.request('shutdown')

    def __handleLeaveToPayCancel(self):
        self.destroy()