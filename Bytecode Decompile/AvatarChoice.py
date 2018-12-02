from ShowBaseGlobal import *
import ToontownGlobals, PandaObject, AvatarDNA, ToonHead, ToontownDialog
from DirectGui import *
import Localizer, DirectNotifyGlobal

class AvatarChoice(DirectButton):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarChoice')

    def __init__(self, av=None, position=0, paid=0):
        DirectButton.__init__(self, relief=None, text='', text_font=ToontownGlobals.getSignFont())
        self.initialiseoptions(AvatarChoice)
        self.hasPaid = paid
        if not av:
            self.create = 1
            self.name = ''
            self.dna = None
        else:
            self.create = 0
            self.name = av.name
            self.dna = AvatarDNA.AvatarDNA(av.dna)
            self.wantName = av.wantName
            self.approvedName = av.approvedName
            self.rejectedName = av.rejectedName
            self.allowedName = av.allowedName
        self.position = position
        self.doneEvent = 'avChoicePanel-' + str(self.position)
        self.deleteWithPasswordFrame = None
        self.pickAToonGui = loader.loadModelOnce('phase_3/models/gui/pick_a_toon_gui')
        self['image'] = self.pickAToonGui.find('**/av-chooser_Square_UP')
        self.setScale(1.01)
        if self.create:
            self['command'] = self.__handleCreate
            self['text'] = (Localizer.AvatarChoiceMakeAToon,)
            self['text_pos'] = (0, 0)
            self['text0_scale'] = 0.1
            self['text1_scale'] = 0.12
            self['text2_scale'] = 0.12
            self['text0_fg'] = (0, 1, 0.8, 0.5)
            self['text1_fg'] = (0, 1, 0.8, 1)
            self['text2_fg'] = (0.3, 1, 0.9, 1)
        else:
            self['command'] = self.__handleChoice
            self['text'] = ('', Localizer.AvatarChoicePlayThisToon, Localizer.AvatarChoicePlayThisToon)
            self['text_scale'] = 0.12
            self['text_fg'] = (1, 0.9, 0.1, 1)
            self.nameText = DirectLabel(parent=self, relief=None, scale=0.09, pos=(0, 0, 0.27), text=self.name, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_wordwrap=7.5, text_font=ToontownGlobals.getToonFont(), state=DISABLED)
            if self.approvedName != '':
                self.nameText['text'] = self.approvedName
            guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
            self.nameYourToonButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=(Localizer.AvatarChoiceNameYourToon, Localizer.AvatarChoiceNameYourToon, Localizer.AvatarChoiceNameYourToon), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.15, text_pos=(0, 0.03), text_font=ToontownGlobals.getInterfaceFont(), pos=(-0.2, 0, -0.3), scale=0.45, image_scale=(2, 1, 3), command=self.__handleNameYourToon)
            guiButton.removeNode()
            self.statusText = DirectLabel(parent=self, relief=None, scale=0.09, pos=(0, 0, -0.24), text='', text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_wordwrap=7.5, text_font=ToontownGlobals.getToonFont(), state=DISABLED)
            if self.wantName != '':
                self.nameYourToonButton.hide()
                self.statusText['text'] = Localizer.AvatarChoiceNameReview
            else:
                if self.approvedName != '':
                    self.nameYourToonButton.hide()
                    self.statusText['text'] = Localizer.AvatarChoiceNameApproved
                else:
                    if self.rejectedName != '':
                        self.nameYourToonButton.hide()
                        self.statusText['text'] = Localizer.AvatarChoiceNameRejected
                    else:
                        if self.allowedName == 1 and (toonbase.tcr.allowFreeNames() or self.hasPaid):
                            self.nameYourToonButton.show()
                            self.statusText['text'] = ''
                        else:
                            self.nameYourToonButton.hide()
                            self.statusText['text'] = ''
            self.head = hidden.attachNewNode('head')
            self.head.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
            self.head.reparentTo(self.stateNodePath[0], 20)
            self.head.instanceTo(self.stateNodePath[1], 20)
            self.head.instanceTo(self.stateNodePath[2], 20)
            self.headModel = ToonHead.ToonHead()
            self.headModel.setupHead(self.dna, forGui=1)
            self.headModel.reparentTo(self.head)
            self.headModel.startBlink()
            self.headModel.startLookAround()
            trashcanGui = loader.loadModelOnce('phase_3/models/gui/trashcan_gui')
            self.deleteButton = DirectButton(parent=self, image=(trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR')), text=('', Localizer.AvatarChoiceDelete, Localizer.AvatarChoiceDelete), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.15, text_pos=(0, -0.1), text_font=ToontownGlobals.getInterfaceFont(), relief=None, pos=(0.27, 0, -0.25), scale=0.45, command=self.__handleDelete)
            trashcanGui.removeNode()
        self.resetFrameSize()
        return None
        return

    def destroy(self):
        loader.unloadModel('phase_3/models/gui/pick_a_toon_gui')
        self.pickAToonGui.removeNode()
        del self.pickAToonGui
        del self.dna
        if self.create:
            pass
        else:
            self.headModel.stopBlink()
            self.headModel.stopLookAroundNow()
            self.headModel.delete()
            self.head.removeNode()
            del self.head
            del self.headModel
            del self.nameText
            del self.statusText
            del self.deleteButton
            del self.nameYourToonButton
            loader.unloadModel('phase_3/models/gui/trashcan_gui')
            loader.unloadModel('phase_3/models/gui/quit_button')
        DirectFrame.destroy(self)
        if self.deleteWithPasswordFrame:
            self.deleteWithPasswordFrame.destroy()

    def __handleChoice(self):
        cleanupDialog('globalDialog')
        messenger.send(self.doneEvent, ['chose', self.position])

    def __handleCreate(self):
        cleanupDialog('globalDialog')
        messenger.send(self.doneEvent, ['create', self.position])

    def __handleDelete(self):
        cleanupDialog('globalDialog')
        self.verify = ToontownDialog.GlobalDialog(doneEvent='verifyDone', message=Localizer.AvatarChoiceDeleteConfirm % self.name, style=ToontownDialog.TwoChoice)
        self.verify.show()
        self.accept('verifyDone', self.__handleVerifyDelete)

    def __handleNameYourToon(self):
        messenger.send(self.doneEvent, ['nameIt', self.position])

    def __handleVerifyDelete(self):
        status = self.verify.doneStatus
        self.ignore('verifyDone')
        self.verify.cleanup()
        del self.verify
        if status == 'ok':
            self.verifyDeleteWithPassword()

    def verifyDeleteWithPassword(self):
        tt = toonbase.tcr.loginInterface
        if tt.supportsAuthenticateDelete():
            self.deleteWithPassword = 1
            deleteText = Localizer.AvatarChoiceDeletePasswordText % self.name
        else:
            self.deleteWithPassword = 0
            deleteText = Localizer.AvatarChoiceDeleteConfirmText % {'name': self.name, 'confirm': Localizer.AvatarChoiceDeleteConfirmUserTypes}
        if self.deleteWithPasswordFrame == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (
             buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            self.deleteWithPasswordFrame = DirectFrame(pos=(0.0, 0.1, 0.2), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.0), text=deleteText, text_wordwrap=19, text_scale=0.06, text_pos=(0, 0.25), textMayChange=1, sortOrder=NO_FADE_SORT_INDEX)
            if self.deleteWithPassword:
                self.passwordLabel = DirectLabel(parent=self.deleteWithPasswordFrame, relief=None, pos=(-0.07, 0.0, -0.2), text=Localizer.AvatarChoicePassword, text_scale=0.08, text_align=TextNode.ARight, textMayChange=0)
                self.passwordEntry = DirectEntry(parent=self.deleteWithPasswordFrame, relief=None, image=nameBalloon, image1_color=(0.8, 0.8, 0.8, 1.0), scale=0.064, pos=(0.0, 0.0, -0.2), width=ToontownGlobals.maxLoginWidth, numLines=1, focus=1, cursorKeys=1, obscured=1, command=self.__handleDeleteWithPasswordOK)
                DirectButton(parent=self.deleteWithPasswordFrame, image=okButtonImage, relief=None, text=Localizer.AvatarChoiceDeletePasswordOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.22, 0.0, -0.35), command=self.__handleDeleteWithPasswordOK)
            else:
                self.passwordEntry = DirectEntry(parent=self.deleteWithPasswordFrame, relief=None, image=nameBalloon, image1_color=(0.8, 0.8, 0.8, 1.0), scale=0.064, pos=(-0.3, 0.0, -0.2), width=10, numLines=1, focus=1, cursorKeys=1, command=self.__handleDeleteWithConfirmOK)
                DirectButton(parent=self.deleteWithPasswordFrame, image=okButtonImage, relief=None, text=Localizer.AvatarChoiceDeletePasswordOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.22, 0.0, -0.35), command=self.__handleDeleteWithConfirmOK)
            DirectLabel(parent=self.deleteWithPasswordFrame, relief=None, pos=(0, 0, 0.35), text=Localizer.AvatarChoiceDeletePasswordTitle, textMayChange=0, text_scale=0.08)
            DirectButton(parent=self.deleteWithPasswordFrame, image=cancelButtonImage, relief=None, text=Localizer.AvatarChoiceDeletePasswordCancel, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=1, pos=(0.2, 0.0, -0.35), command=self.__handleDeleteWithPasswordCancel)
            buttons.removeNode()
            nameBalloon.removeNode()
        else:
            self.deleteWithPasswordFrame['text'] = deleteText
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        base.transitions.fadeScreen(0.5)
        self.deleteWithPasswordFrame.show()
        return

    def __handleDeleteWithPasswordOK(self, *args):
        password = self.passwordEntry.get()
        tt = toonbase.tcr.loginInterface
        okFlag, errorMsg = tt.authenticateDelete(toonbase.tcr.userName, password)
        if okFlag:
            self.deleteWithPasswordFrame.hide()
            base.transitions.noTransitions()
            messenger.send(self.doneEvent, ['delete', self.position])
        else:
            if errorMsg is not None:
                self.notify.warning('authenticateDelete returned unexpected error: %s' % errorMsg)
            self.deleteWithPasswordFrame['text'] = Localizer.AvatarChoiceDeleteWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        return

    def __handleDeleteWithConfirmOK(self, *args):
        password = self.passwordEntry.get()
        passwordMatch = Localizer.AvatarChoiceDeleteConfirmUserTypes
        password = TextEncoder.lower(password)
        passwordMatch = TextEncoder.lower(passwordMatch)
        if password == passwordMatch:
            self.deleteWithPasswordFrame.hide()
            base.transitions.noTransitions()
            messenger.send(self.doneEvent, ['delete', self.position])
        else:
            self.deleteWithPasswordFrame['text'] = Localizer.AvatarChoiceDeleteWrongConfirm % {'name': self.name, 'confirm': Localizer.AvatarChoiceDeleteConfirmUserTypes}
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    def __handleDeleteWithPasswordCancel(self):
        self.deleteWithPasswordFrame.hide()
        base.transitions.noTransitions()