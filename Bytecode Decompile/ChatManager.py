import Task, string, sys, PandaObject, ToontownGlobals, ChatInputNormal, ChatInputQuickTalker, LeaveToPayDialog, FSM, State, MagicWordManager, SecretFriendsInfoPanel, PrivacyPolicyPanel, Localizer
from DirectGui import *
CHAT_EVENT = 'ChatEvent'
NORMAL_CHAT_EVENT = 'NormalChatEvent'
QT_CHAT_EVENT = 'QTChatEvent'
NORMAL_QT_CHAT_EVENT = 'NormalQTChatEvent'
QUEST_QT_CHAT_EVENT = 'QuestQTChatEvent'
OnScreen = 0
OffScreen = 1
Thought = 2
ThoughtPrefix = '.'

def isThought(message):
    if len(message) == 0:
        return 0
    else:
        if string.find(message, ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
            return 1
        else:
            return 0


def removeThoughtPrefix(message):
    if isThought(message):
        return message[len(ThoughtPrefix):]
    else:
        return message


class ChatManager(PandaObject.PandaObject):
    __module__ = __name__
    execChat = base.config.GetBool('exec-chat', 0)

    def __init__(self):
        self.__qtObscured = 0
        self.__normalObscured = 0
        gui = loader.loadModelOnce('phase_3.5/models/gui/chat_input_gui')
        self.normalButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-1.2647, 0, 0.928), scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('', Localizer.ChatManagerChat, Localizer.ChatManagerChat), text_scale=0.06, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, sortOrder=FOREGROUND_SORT_INDEX, command=self.__normalButtonPressed)
        self.normalButton.hide()
        self.openQtSfx = loader.loadSfx('phase_3.5/audio/sfx/GUI_quicktalker.mp3')
        self.openQtSfx.setVolume(0.6)
        self.qtButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-1.129, 0, 0.928), scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('', Localizer.GlobalQuickTalkerName, Localizer.GlobalQuickTalkerName), text_scale=0.06, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, sortOrder=FOREGROUND_SORT_INDEX, command=self.__qtButtonPressed, clickSound=self.openQtSfx)
        self.qtButton.hide()
        self.whisperFrame = DirectFrame(relief=None, image=getDefaultDialogGeom(), image_scale=(0.45, 0.45, 0.45), image_color=ToontownGlobals.GlobalDialogColor, pos=(0.0, 0, 0.754), text=Localizer.ChatManagerWhisperTo, text_wordwrap=7.0, text_scale=0.06, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0.14), textMayChange=1, sortOrder=FOREGROUND_SORT_INDEX)
        self.whisperFrame.hide()
        self.whisperButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-0.125, 0, -0.1), scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('', Localizer.ChatManagerChat, Localizer.ChatManagerChat, ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=0.05, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperButtonPressed)
        self.whisperQtButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.0, 0, -0.1), scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('', Localizer.GlobalQuickTalkerName, Localizer.GlobalQuickTalkerName, ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=0.05, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperQtButtonPressed)
        self.whisperCancelButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr')), pos=(0.125, 0, -0.1), scale=1.179, relief=None, text=('', Localizer.ChatManagerCancel, Localizer.ChatManagerCancel), text_scale=0.05, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperCancelPressed)
        gui.removeNode()
        self.openChatWarning = None
        self.unpaidChatWarning = None
        self.noSecretChatAtAll = None
        self.noSecretChatWarning = None
        self.activateChat = None
        self.leaveToPayDialog = None
        self.chatMoreInfo = None
        self.chatPrivacyPolicy = None
        self.secretChatActivated = None
        self.problemActivatingChat = None
        self.fsm = FSM.FSM('chatManager', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('mainMenu', self.enterMainMenu, self.exitMainMenu),
         State.State('quickTalker', self.enterQuickTalker, self.exitQuickTalker),
         State.State('normalChat', self.enterNormalChat, self.exitNormalChat),
         State.State('whisper', self.enterWhisper, self.exitWhisper),
         State.State('whisperChat', self.enterWhisperChat, self.exitWhisperChat),
         State.State('whisperQuickTalker', self.enterWhisperQuickTalker, self.exitWhisperQuickTalker),
         State.State('openChatWarning', self.enterOpenChatWarning, self.exitOpenChatWarning),
         State.State('unpaidChatWarning', self.enterUnpaidChatWarning, self.exitUnpaidChatWarning),
         State.State('noSecretChatAtAll', self.enterNoSecretChatAtAll, self.exitNoSecretChatAtAll),
         State.State('noSecretChatWarning', self.enterNoSecretChatWarning, self.exitNoSecretChatWarning),
         State.State('activateChat', self.enterActivateChat, self.exitActivateChat),
         State.State('leaveToPayDialog', self.enterLeaveToPayDialog, self.exitLeaveToPayDialog),
         State.State('chatMoreInfo', self.enterChatMoreInfo, self.exitChatMoreInfo),
         State.State('chatPrivacyPolicy', self.enterChatPrivacyPolicy, self.exitChatPrivacyPolicy),
         State.State('secretChatActivated', self.enterSecretChatActivated, self.exitSecretChatActivated),
         State.State('problemActivatingChat', self.enterProblemActivatingChat, self.exitProblemActivatingChat)], 'off', 'off')
        self.fsm.enterInitialState()
        self.chatInputNormal = ChatInputNormal.ChatInputNormal(self)
        self.chatInputQuickTalker = ChatInputQuickTalker.ChatInputQuickTalker(self)
        return

    def delete(self):
        self.ignoreAll()
        del self.fsm
        self.chatInputNormal.delete()
        del self.chatInputNormal
        self.chatInputQuickTalker.delete()
        del self.chatInputQuickTalker
        if self.openChatWarning:
            self.openChatWarning.destroy()
            self.openChatWarning = None
        if self.unpaidChatWarning:
            self.payButton = None
            self.unpaidChatWarning.destroy()
            self.unpaidChatWarning = None
        if self.noSecretChatAtAll:
            self.noSecretChatAtAll.destroy()
            self.noSecretChatAtAll = None
        if self.noSecretChatWarning:
            self.noSecretChatWarning.destroy()
            self.noSecretChatWarning = None
        if self.activateChat:
            self.activateChat.destroy()
            self.activateChat = None
        if self.leaveToPayDialog:
            self.leaveToPayDialog.destroy()
            self.leaveToPayDialog = None
        if self.chatMoreInfo:
            self.chatMoreInfo.destroy()
            self.chatMoreInfo = None
        if self.chatPrivacyPolicy:
            self.chatPrivacyPolicy.destroy()
            self.chatPrivacyPolicy = None
        if self.secretChatActivated:
            self.secretChatActivated.destroy()
            self.secretChatActivated = None
        if self.problemActivatingChat:
            self.problemActivatingChat.destroy()
            self.problemActivatingChat = None
        loader.unloadModel('phase_3.5/models/gui/chat_input_gui')
        self.normalButton.destroy()
        del self.normalButton
        self.qtButton.destroy()
        del self.qtButton
        del self.openQtSfx
        self.whisperFrame.destroy()
        del self.whisperFrame
        del self.whisperButton
        del self.whisperQtButton
        del self.whisperCancelButton
        return

    def obscure(self, normal, qt):
        self.__qtObscured = qt
        if self.__qtObscured:
            self.qtButton.hide()
        self.__normalObscured = normal
        if self.__normalObscured:
            self.normalButton.hide()

    def isObscured(self):
        return (
         self.__normalObscured, self.__qtObscured)

    def stop(self):
        self.fsm.request('off')
        self.ignoreAll()

    def start(self):
        self.fsm.request('mainMenu')

    def __announceChat(self):
        messenger.send(CHAT_EVENT)

    def __announceQTChat(self):
        messenger.send(QT_CHAT_EVENT)
        self.__announceChat()

    def sendChatString(self, message):
        chatFlags = CFSpeech | CFTimeout
        if isThought(message):
            message = removeThoughtPrefix(message)
            chatFlags = CFThought
        messenger.send('chatUpdate', [message, chatFlags])
        messenger.send(NORMAL_CHAT_EVENT)
        self.__announceChat()

    def sendWhisperString(self, message, whisperAvatarId):
        messenger.send('whisperUpdate', [message, whisperAvatarId])

    def sendQTChatMessage(self, QTmessage):
        messenger.send('chatUpdateQT', [QTmessage])
        messenger.send(NORMAL_QT_CHAT_EVENT)
        self.__announceQTChat()

    def sendWhisperQTChatMessage(self, QTmessage, whisperAvatarId):
        messenger.send('whisperUpdateQT', [QTmessage, whisperAvatarId])

    def sendQTQuestChatMessage(self, QTmessage):
        messenger.send('chatUpdateQTQuest', [QTmessage])
        messenger.send(QUEST_QT_CHAT_EVENT)
        self.__announceQTChat()

    def sendWhisperQTQuestChatMessage(self, QTmessage, whisperAvatarId):
        messenger.send('whisperUpdateQTQuest', [QTmessage, whisperAvatarId])

    def sendQTCustomChatMessage(self, QTmessage):
        messenger.send('chatUpdateQTCustom', [QTmessage])
        self.__announceQTChat()

    def sendWhisperQTCustomChatMessage(self, QTmessage, whisperAvatarId):
        messenger.send('whisperUpdateQTCustom', [QTmessage, whisperAvatarId])

    def decodeQTMessage(self, msg):
        return self.chatInputQuickTalker.decodeQTMessage(msg)

    def enterOff(self):
        self.qtButton.hide()
        self.normalButton.hide()
        self.ignoreAll()

    def exitOff(self):
        pass

    def enterMainMenu(self):
        if not self.__qtObscured:
            self.qtButton.show()
        if not self.__normalObscured:
            self.normalButton.show()
        if toonbase.localToon.canChat() or MagicWordManager.MagicWordManager.wantMagicWords:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 1
            self.acceptOnce('enterNormalChat', self.fsm.request, ['normalChat'])

    def exitMainMenu(self):
        self.qtButton.hide()
        self.normalButton.hide()
        self.ignore('enterNormalChat')
        self.chatInputNormal.chatEntry['backgroundFocus'] = 0

    def whisperTo(self, avatarName, avatarId):
        self.fsm.request('whisper', [avatarName, avatarId])

    def noWhisper(self):
        self.fsm.request('mainMenu')

    def enterWhisper(self, avatarName, avatarId):
        self.whisperQtButton['extraArgs'] = [
         avatarId]
        self.whisperButton['extraArgs'] = [avatarName, avatarId]
        online = 0
        if toonbase.tcr.doId2do.has_key(avatarId):
            online = 1
        else:
            if toonbase.tcr.isFriend(avatarId):
                online = toonbase.tcr.isFriendOnline(avatarId)
        understandable = 0
        av = toonbase.tcr.identifyAvatar(avatarId)
        if av != None:
            understandable = av.isUnderstandable()
        if understandable and online:
            self.whisperButton['state'] = 'normal'
        else:
            self.whisperButton['state'] = 'inactive'
        if online:
            self.whisperQtButton['state'] = 'normal'
            self.whisperFrame['text'] = Localizer.ChatManagerWhisperToName % avatarName
        else:
            self.whisperQtButton['state'] = 'inactive'
            self.whisperFrame['text'] = Localizer.ChatManagerWhisperOffline % avatarName
        self.whisperFrame.show()
        if understandable and online:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 1
            self.acceptOnce('enterNormalChat', self.fsm.request, ['whisperChat', [avatarName, avatarId]])
        return

    def exitWhisper(self):
        self.whisperFrame.hide()
        self.ignore('enterNormalChat')
        self.chatInputNormal.chatEntry['backgroundFocus'] = 0

    def enterWhisperQuickTalker(self, avatarId):
        self.whisperFrame.show()
        self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        self.chatInputQuickTalker.show(avatarId)

    def exitWhisperQuickTalker(self):
        self.whisperFrame.hide()
        self.chatInputQuickTalker.hide()

    def enterWhisperChat(self, avatarName, avatarId):
        self.chatInputNormal.show(avatarName, avatarId)

    def exitWhisperChat(self):
        self.chatInputNormal.hide()

    def enterQuickTalker(self):
        messenger.send('enterQuickTalker')
        if not self.__qtObscured:
            self.qtButton.show()
        if not self.__normalObscured:
            self.normalButton.show()
        self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        self.chatInputQuickTalker.show()

    def exitQuickTalker(self):
        self.qtButton.hide()
        self.normalButton.hide()
        self.chatInputQuickTalker.hide()

    def enterNormalChat(self):
        self.chatInputNormal.show()

    def exitNormalChat(self):
        self.chatInputNormal.hide()

    def enterOpenChatWarning(self):
        if self.openChatWarning == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            buttonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.openChatWarning = DirectFrame(pos=(0.0, 0.1, 0.4), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.2, 1.0, 0.9), text=Localizer.OpenChatWarning, text_wordwrap=18, text_scale=0.06, text_pos=(0.0, 0.28), textMayChange=0)
            DirectButton(self.openChatWarning, image=buttonImage, relief=None, text=Localizer.OpenChatWarningOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.28), command=self.__handleOpenChatWarningOK)
            buttons.removeNode()
        self.openChatWarning.show()
        if not self.__qtObscured:
            self.qtButton.show()
        return

    def exitOpenChatWarning(self):
        self.openChatWarning.hide()
        self.qtButton.hide()

    def enterUnpaidChatWarning(self):
        if self.unpaidChatWarning == None:
            guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
            buttonImage = (
             guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
            self.unpaidChatWarning = DirectFrame(pos=(0.0, 0.1, 0.4), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.2, 1.0, 0.7), text=Localizer.UnpaidChatWarning, text_wordwrap=18, text_scale=0.06, text_pos=(0.0, 0.23), textMayChange=0)
            self.payButton = DirectButton(self.unpaidChatWarning, image=buttonImage, relief=None, text=Localizer.UnpaidChatWarningPay, image_scale=(1.75, 1, 1.15), text_scale=0.06, text_pos=(0, -0.02), textMayChange=0, pos=(0.0, 0.0, -0.08), command=self.__handleUnpaidChatWarningPay)
            DirectButton(self.unpaidChatWarning, image=buttonImage, relief=None, text=Localizer.UnpaidChatWarningContinue, textMayChange=0, image_scale=(1.75, 1, 1.15), text_scale=0.06, text_pos=(0, -0.02), pos=(0.0, 0.0, -0.23), command=self.__handleUnpaidChatWarningContinue)
            guiButton.removeNode()
        if toonbase.localToon.inTutorial:
            self.payButton.hide()
        else:
            self.payButton.show()
        self.unpaidChatWarning.show()
        if not self.__qtObscured:
            self.qtButton.show()
        return

    def exitUnpaidChatWarning(self):
        self.unpaidChatWarning.hide()
        self.qtButton.hide()

    def enterNoSecretChatAtAll(self):
        if self.noSecretChatAtAll == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.noSecretChatAtAll = DirectFrame(pos=(0.0, 0.1, 0.2), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.0), text=Localizer.NoSecretChatAtAll, text_wordwrap=20, textMayChange=0, text_scale=0.06, text_pos=(0, 0.25))
            DirectLabel(parent=self.noSecretChatAtAll, relief=None, pos=(0, 0, 0.35), text=Localizer.NoSecretChatAtAllTitle, textMayChange=0, text_scale=0.08)
            DirectButton(self.noSecretChatAtAll, image=okButtonImage, relief=None, text=Localizer.NoSecretChatAtAllOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.35), command=self.__handleNoSecretChatAtAllOK)
            buttons.removeNode()
        self.noSecretChatAtAll.show()
        return

    def exitNoSecretChatAtAll(self):
        self.noSecretChatAtAll.hide()

    def enterNoSecretChatWarning(self):
        if self.noSecretChatWarning == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (
             buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            self.noSecretChatWarning = DirectFrame(pos=(0.0, 0.1, 0.2), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.0), text=Localizer.NoSecretChatWarning, text_wordwrap=20, text_scale=0.055, text_pos=(0, 0.25), textMayChange=1)
            self.passwordLabel = DirectLabel(parent=self.noSecretChatWarning, relief=None, pos=(-0.07, 0.0, -0.2), text=Localizer.ParentPassword, text_scale=0.06, text_align=TextNode.ARight, textMayChange=0)
            self.passwordEntry = DirectEntry(parent=self.noSecretChatWarning, relief=None, image=nameBalloon, image1_color=(0.8, 0.8, 0.8, 1.0), scale=0.064, pos=(0.0, 0.0, -0.2), width=ToontownGlobals.maxLoginWidth, numLines=1, focus=1, cursorKeys=1, obscured=1, command=self.__handleNoSecretChatWarningOK)
            DirectLabel(parent=self.noSecretChatWarning, relief=None, pos=(0, 0, 0.35), text=Localizer.NoSecretChatWarningTitle, textMayChange=0, text_scale=0.08)
            DirectButton(self.noSecretChatWarning, image=okButtonImage, relief=None, text=Localizer.NoSecretChatWarningOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.22, 0.0, -0.35), command=self.__handleNoSecretChatWarningOK)
            DirectButton(self.noSecretChatWarning, image=cancelButtonImage, relief=None, text=Localizer.NoSecretChatWarningCancel, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=1, pos=(0.2, 0.0, -0.35), command=self.__handleNoSecretChatWarningCancel)
            buttons.removeNode()
            nameBalloon.removeNode()
        else:
            self.noSecretChatWarning['text'] = Localizer.NoSecretChatWarning
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        self.noSecretChatWarning.show()
        return

    def exitNoSecretChatWarning(self):
        self.noSecretChatWarning.hide()

    def enterActivateChat(self):
        if self.activateChat == None:
            guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (
             buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            moreButtonImage = (
             guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
            self.activateChat = DirectFrame(pos=(0.0, 0.1, 0.2), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.8, 1.0, 1.3), text=Localizer.ActivateChat, text_align=TextNode.ALeft, text_wordwrap=28, text_scale=0.06, text_pos=(-0.82, 0.5), textMayChange=0)
            DirectButton(self.activateChat, image=moreButtonImage, relief=None, text=Localizer.ActivateChatMoreInfo, text_scale=0.06, text_pos=(0, -0.02), textMayChange=0, pos=(0.0, 0.0, 0.3), command=self.__handleActivateChatMoreInfo)
            DirectButton(self.activateChat, image=okButtonImage, relief=None, text=Localizer.ActivateChatYes, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.5, 0.0, -0.5), command=self.__handleActivateChatYes)
            DirectButton(self.activateChat, image=cancelButtonImage, relief=None, text=Localizer.ActivateChatNo, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.5, 0.0, -0.5), command=self.__handleActivateChatNo)
            DirectButton(self.activateChat, image=moreButtonImage, relief=None, text=Localizer.ActivateChatPrivacyPolicy, text_scale=0.06, text_pos=(0, -0.02), textMayChange=0, pos=(0.0, 0.0, -0.5), command=self.__handleActivateChatPrivacyPolicy)
            guiButton.removeNode()
            buttons.removeNode()
        self.activateChat.show()
        return

    def exitActivateChat(self):
        self.activateChat.hide()

    def enterChatMoreInfo(self):
        if self.chatMoreInfo == None:
            self.chatMoreInfo = SecretFriendsInfoPanel.SecretFriendsInfoPanel('secretFriendsInfoDone')
        self.chatMoreInfo.show()
        self.accept('secretFriendsInfoDone', self.__secretFriendsInfoDone)
        return

    def exitChatMoreInfo(self):
        self.chatMoreInfo.hide()
        self.ignore('secretFriendsInfoDone')

    def enterChatPrivacyPolicy(self):
        if self.chatPrivacyPolicy == None:
            self.chatPrivacyPolicy = PrivacyPolicyPanel.PrivacyPolicyPanel('privacyPolicyDone')
        self.chatPrivacyPolicy.show()
        self.accept('privacyPolicyDone', self.__privacyPolicyDone)
        return

    def exitChatPrivacyPolicy(self):
        self.chatPrivacyPolicy.hide()
        self.ignore('privacyPolicyDone')

    def enterSecretChatActivated(self):
        if self.secretChatActivated == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            buttonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.secretChatActivated = DirectFrame(pos=(0.0, 0.1, 0.4), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.2, 1.0, 0.8), text=Localizer.SecretChatActivated, text_align=TextNode.ALeft, text_wordwrap=17.5, text_scale=0.06, text_pos=(-0.5, 0.25), textMayChange=0)
            DirectButton(self.secretChatActivated, image=buttonImage, relief=None, text=Localizer.SecretChatActivatedOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.22), command=self.__handleSecretChatActivatedOK)
            buttons.removeNode()
        self.secretChatActivated.show()
        return

    def exitSecretChatActivated(self):
        self.secretChatActivated.hide()

    def enterProblemActivatingChat(self):
        if self.problemActivatingChat == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            buttonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.problemActivatingChat = DirectFrame(pos=(0.0, 0.1, 0.4), relief=None, image=getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.2, 1.0, 0.9), text='', text_align=TextNode.ALeft, text_wordwrap=18, text_scale=0.06, text_pos=(-0.5, 0.28), textMayChange=1)
            DirectButton(self.problemActivatingChat, image=buttonImage, relief=None, text=Localizer.ProblemActivatingChatOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.28), command=self.__handleProblemActivatingChatOK)
            buttons.removeNode()
        self.problemActivatingChat.show()
        return

    def exitProblemActivatingChat(self):
        self.problemActivatingChat.hide()

    def enterLeaveToPayDialog(self):
        if self.leaveToPayDialog == None:
            self.leaveToPayDialog = LeaveToPayDialog.LeaveToPayDialog()
            self.leaveToPayDialog.setCancel(self.__handleLeaveToPayCancel)
        self.leaveToPayDialog.show()
        return

    def exitLeaveToPayDialog(self):
        if self.leaveToPayDialog:
            self.leaveToPayDialog.destroy()
            self.leaveToPayDialog = None
        return

    def __normalButtonPressed(self):
        if not toonbase.tcr.isPaid():
            self.fsm.request('unpaidChatWarning')
        else:
            if not toonbase.tcr.allowSecretChat():
                tt = toonbase.tcr.loginInterface
                if tt.supportsParentPassword():
                    self.fsm.request('noSecretChatWarning')
                else:
                    self.fsm.request('noSecretChatAtAll')
            else:
                if not toonbase.localToon.canChat():
                    self.fsm.request('openChatWarning')
                else:
                    self.fsm.request('normalChat')

    def __qtButtonPressed(self):
        self.fsm.request('quickTalker')

    def __whisperButtonPressed(self, avatarName, avatarId):
        self.fsm.request('whisperChat', [avatarName, avatarId])

    def __whisperQtButtonPressed(self, avatarId):
        self.fsm.request('whisperQuickTalker', [avatarId])

    def __whisperCancelPressed(self):
        self.fsm.request('mainMenu')

    def __handleOpenChatWarningOK(self):
        self.fsm.request('mainMenu')

    def __handleUnpaidChatWarningContinue(self):
        self.fsm.request('mainMenu')

    def __handleUnpaidChatWarningPay(self):
        if toonbase.tcr.isWebPlayToken():
            self.fsm.request('leaveToPayDialog')
        else:
            self.fsm.request('mainMenu')
            toonbase.localToon.b_setAnimState('TeleportOut', 1, self.__handleBookExitTeleport)

    def __handleBookExitTeleport(self):
        toonbase.tcr.loginFSM.request('memberAgreement')

    def __handleNoSecretChatAtAllOK(self):
        self.fsm.request('mainMenu')

    def __handleNoSecretChatWarningOK(self, *args):
        password = self.passwordEntry.get()
        tt = toonbase.tcr.loginInterface
        okflag, message = tt.authenticateParentPassword(toonbase.tcr.userName, toonbase.tcr.password, password)
        if okflag:
            self.fsm.request('activateChat')
        else:
            if message:
                self.fsm.request('problemActivatingChat')
                self.problemActivatingChat['text'] = Localizer.ProblemActivatingChat % message
            else:
                self.noSecretChatWarning['text'] = Localizer.NoSecretChatWarningWrongPassword
                self.passwordEntry['focus'] = 1
                self.passwordEntry.enterText('')

    def __handleNoSecretChatWarningCancel(self):
        self.fsm.request('mainMenu')

    def __handleActivateChatYes(self):
        password = self.passwordEntry.get()
        tt = toonbase.tcr.loginInterface
        okflag, message = tt.enableSecretFriends(toonbase.tcr.userName, toonbase.tcr.password, password)
        if okflag:
            tt.resendPlayToken()
            toonbase.tcr.secretChatAllowed = 1
            self.fsm.request('secretChatActivated')
        else:
            if message == None:
                message = 'Parent Password was invalid.'
            self.fsm.request('problemActivatingChat')
            self.problemActivatingChat['text'] = Localizer.ProblemActivatingChat % message
        return

    def __handleActivateChatMoreInfo(self):
        self.fsm.request('chatMoreInfo')

    def __handleActivateChatPrivacyPolicy(self):
        self.fsm.request('chatPrivacyPolicy')

    def __handleActivateChatNo(self):
        self.fsm.request('mainMenu')

    def __handleLeaveToPayCancel(self):
        self.fsm.request('mainMenu')

    def __secretFriendsInfoDone(self):
        self.fsm.request('activateChat')

    def __privacyPolicyDone(self):
        self.fsm.request('activateChat')

    def __handleSecretChatActivatedOK(self):
        self.fsm.request('mainMenu')

    def __handleProblemActivatingChatOK(self):
        self.fsm.request('mainMenu')