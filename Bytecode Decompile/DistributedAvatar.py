from PandaObject import *
import DistributedNode, DistributedActor, ToontownGlobals, Avatar, AvatarDNA, ChatGarbler, ChatManager, string, Task, InventoryNew, Experience, Localizer, QTQuestNode, QTCustomNode

class DistributedAvatar(DistributedActor.DistributedActor, Avatar.Avatar):
    __module__ = __name__
    LaffNumberGenerator = TextNode('LaffNumberGenerator')
    LaffNumberGenerator.freeze()
    LaffNumbersEnabled = 1
    TeleportFailureTimeout = 60.0

    def __init__(self, cr):
        try:
            self.DistributedAvatar_initialized
        except:
            self.DistributedAvatar_initialized = 1
            Avatar.Avatar.__init__(self)
            DistributedActor.DistributedActor.__init__(self, cr)
            self.__chatGarbler = ChatGarbler.ChatGarbler()
            self.__teleportAvailable = 0
            self.laffNumber = None
            self.inventory = None
            self.experience = None
            self.hp = None
            self.maxHp = None
            self.trophyScore = 0
            self.trophyStar = None
            self.trophyStarSpeed = 0
            self.maxMoney = 0
            self.maxBankMoney = 0
            self.lastFailedTeleportMessage = {}

        return None
        return

    def disable(self):
        self.reparentTo(hidden)
        self.removeActive()
        self.disableBodyCollisions()
        self.hideLaffNumber()
        self.hp = None
        self.setTrophyScore(0)
        DistributedActor.DistributedActor.disable(self)
        return

    def delete(self):
        try:
            self.DistributedAvatar_deleted
        except:
            self.DistributedAvatar_deleted = 1
            del self.experience
            if self.inventory:
                self.inventory.unload()
            del self.inventory
            del self.__chatGarbler
            DistributedActor.DistributedActor.delete(self)
            Avatar.Avatar.delete(self)

    def generate(self):
        DistributedActor.DistributedActor.generate(self)
        if not self.isLocal():
            self.addActive()
            self.initializeBodyCollisions('distAvatarCollNode-' + str(self.doId))
            self.considerUnderstandable()
        self.setParent(ToontownGlobals.SPHidden)

    def do_setParent(self, parentToken):
        if not self.isDisabled():
            if parentToken == ToontownGlobals.SPHidden:
                self.nametag2dDist &= ~Nametag.CName
            else:
                self.nametag2dDist |= Nametag.CName
            self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)
            DistributedActor.DistributedActor.do_setParent(self, parentToken)

    def b_setMaxMoney(self, maxMoney):
        self.setMaxMoney(maxMoney)
        self.d_setMaxMoney(maxMoney)

    def d_setMaxMoney(self, maxMoney):
        self.sendUpdate('setMaxMoney', [maxMoney])

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def b_setMoney(self, money):
        self.setMoney(money)
        self.d_setMoney(money)

    def d_setMoney(self, money):
        self.sendUpdate('setMoney', [money])

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def b_setMaxBankMoney(self, maxMoney):
        self.setMaxBankMoney(maxMoney)
        self.d_setMaxBankMoney(maxMoney)

    def d_setMaxBankMoney(self, maxMoney):
        self.sendUpdate('setMaxBankMoney', [maxMoney])

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney

    def b_setBankMoney(self, money):
        bankMoney = min(money, self.maxBankMoney)
        self.setBankMoney(bankMoney)
        self.d_setBankMoney(bankMoney)

    def d_setBankMoney(self, money):
        self.sendUpdate('setBankMoney', [money])

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def b_setHp(self, hitPoints):
        self.setHp(hitPoints)
        self.d_setHp(hitPoints)

    def d_setHp(self, hitPoints):
        self.sendUpdate('setHp', [hitPoints])

    def setHp(self, hitPoints):
        if self.hp != None:
            oldHp = max(self.hp, 0)
            newHp = max(hitPoints, 0)
            hpDisplayDelta = newHp - oldHp
            self.showLaffNumber(hpDisplayDelta)
        self.hp = hitPoints
        try:
            if self.hp != None and self.maxHp != None:
                messenger.send(self.uniqueName('hpChange'), [self.hp, self.maxHp])
            if oldHp <= 0 and newHp > 0:
                messenger.send(self.uniqueName('positiveHP'))
        except:
            pass

        return

    def getHp(self):
        return self.hp

    def b_setMaxHp(self, hitPoints):
        self.setMaxHp(hitPoints)
        self.d_setMaxHp(hitPoints)

    def d_setMaxHp(self, hitPoints):
        self.sendUpdate('setMaxHp', [hitPoints])

    def setMaxHp(self, hitPoints):
        self.maxHp = hitPoints
        try:
            if self.hp != None and self.maxHp != None:
                messenger.send(self.uniqueName('hpChange'), [self.hp, self.maxHp])
        except AttributeError:
            pass
        else:
            if self.inventory:
                self.inventory.updateGUI()

        return

    def getMaxHp(self):
        return self.maxHp

    def b_setExperience(self, experience):
        self.setExperience(experience)
        self.d_setExperience(experience)

    def d_setExperience(self, experience):
        self.sendUpdate('setExperience', [experience.makeNetString()])

    def setExperience(self, experience):
        self.experience = Experience.Experience(experience)
        if self.inventory:
            self.inventory.updateGUI()
        return None
        return

    def setInventory(self, inventoryNetString):
        if not self.inventory:
            self.inventory = InventoryNew.InventoryNew(self, inventoryNetString)
        self.inventory.updateInvString(inventoryNetString)
        return None
        return

    def setAccountName(self, accountName):
        self.accountName = accountName

    def setLastHood(self, lastHood):
        self.lastHood = lastHood

    def whisperTo(self, chatString, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperFrom', [self.doId, chatString], sendToId)
        return None
        return

    def setWhisperFrom(self, fromId, chatString):
        if fromId == 0:
            return
        if fromId == self.doId:
            return
        sender = toonbase.tcr.identifyAvatar(fromId)
        if sender == None:
            return
        if fromId in self.ignoreList:
            sender.d_setWhisperIgnored(self.doId)
            return
        if toonbase.localToon.garbleChat and not sender.isUnderstandable():
            chatString = self.__chatGarbler.garble(self, chatString)
        self.displayWhisper(fromId, chatString, WhisperPopup.WTNormal)
        return None
        return

    def setSystemMessage(self, aboutId, chatString, whisperType=WhisperPopup.WTSystem):
        self.displayWhisper(aboutId, chatString, whisperType)
        return None
        return

    def displayWhisper(self, fromId, chatString, whisperType):
        print 'Whisper type %d from %d: %s' % (whisperType, fromId, chatString)

    def whisperQTTo(self, qtSequence, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperQTFrom', [self.doId, qtSequence], sendToId)

    def setWhisperQTFrom(self, fromId, qtSequence):
        sender = toonbase.tcr.identifyAvatar(fromId)
        if sender == None:
            return
        if fromId in self.ignoreList:
            sender.d_setWhisperIgnored(self.doId)
            return
        chatString = toonbase.localToon.chatMgr.decodeQTMessage(qtSequence)
        self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
        return

    def whisperQTQuestTo(self, qtSequence, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperQTQuestFrom', [self.doId, qtSequence], sendToId)

    def setWhisperQTQuestFrom(self, fromId, qtSequence):
        sender = toonbase.tcr.identifyAvatar(fromId)
        if sender == None:
            return
        if fromId in self.ignoreList:
            sender.d_setWhisperIgnored(self.doId)
            return
        chatString = QTQuestNode.decodeQTQuestMsg(qtSequence)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
        return

    def whisperQTCustomTo(self, qtSequence, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperQTCustomFrom', [self.doId, qtSequence], sendToId)

    def setWhisperQTCustomFrom(self, fromId, qtSequence):
        sender = toonbase.tcr.identifyAvatar(fromId)
        if sender == None:
            return
        if fromId in self.ignoreList:
            sender.d_setWhisperIgnored(self.doId)
            return
        chatString = QTCustomNode.decodeQTCustomMsg(qtSequence)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
        return

    def d_setWhisperIgnored(self, fromId):
        self.sendUpdate('setWhisperIgnored', [fromId])

    def setWhisperIgnored(self, fromId):
        if fromId in self.ignoreList:
            return
        sender = toonbase.tcr.identifyAvatar(fromId)
        if sender == None:
            return
        chatString = Localizer.WhisperIgnored % sender.getName()
        self.displayWhisper(0, chatString, WhisperPopup.WTSystem)
        return

    def b_setChat(self, chatString, chatFlags):
        if len(chatString) > 0 and chatString[0] == '~':
            messenger.send('magicWord', [chatString])
        else:
            messenger.send('wakeup')
            self.setChatAbsolute(chatString, chatFlags)
            self.d_setChat(chatString, chatFlags)
        return None
        return

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setChat(self, chatString, chatFlags):
        if self.doId in toonbase.localToon.ignoreList:
            return
        if toonbase.localToon.garbleChat and not self.isUnderstandable():
            chatString = self.__chatGarbler.garble(self, chatString)
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        self.setChatAbsolute(chatString, chatFlags)

    def b_setQT(self, qtSequence):
        self.setQT(qtSequence)
        self.d_setQT(qtSequence)
        return None
        return

    def d_setQT(self, qtSequence):
        messenger.send('wakeup')
        self.sendUpdate('setQT', [qtSequence])

    def setQT(self, qtSequence):
        if self.doId in toonbase.localToon.ignoreList:
            return
        chatString = toonbase.localToon.chatMgr.decodeQTMessage(qtSequence)
        self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)

    def b_setQTQuest(self, qtSequence):
        self.setQTQuest(qtSequence)
        self.d_setQTQuest(qtSequence)
        return None
        return

    def d_setQTQuest(self, qtSequence):
        messenger.send('wakeup')
        self.sendUpdate('setQTQuest', [qtSequence])

    def setQTQuest(self, qtSequence):
        chatString = QTQuestNode.decodeQTQuestMsg(qtSequence)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)

    def b_setQTCustom(self, qtSequence):
        self.setQTCustom(qtSequence)
        self.d_setQTCustom(qtSequence)
        return None
        return

    def d_setQTCustom(self, qtSequence):
        messenger.send('wakeup')
        self.sendUpdate('setQTCustom', [qtSequence])

    def setQTCustom(self, qtSequence):
        chatString = QTCustomNode.decodeQTCustomMsg(qtSequence)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)

    def setTrophyScore(self, score):
        self.trophyScore = score
        if self.trophyStar != None:
            self.trophyStar.removeNode()
            self.trophyStar = None
        if self.trophyStarSpeed != 0:
            taskMgr.remove(self.uniqueName('starSpin'))
            self.trophyStarSpeed = 0
        if self.trophyScore >= ToontownGlobals.TrophyStarLevels[4]:
            self.trophyStar = loader.loadModelCopy('phase_3.5/models/gui/name_star')
            self.trophyStar.reparentTo(self.nametag.getNameIcon())
            self.trophyStar.setScale(2)
            self.trophyStar.setZ(2)
            self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[4])
            self.trophyStarSpeed = 15
            if self.trophyScore >= ToontownGlobals.TrophyStarLevels[5]:
                taskMgr.add(self.__starSpin, self.uniqueName('starSpin'))
        else:
            if self.trophyScore >= ToontownGlobals.TrophyStarLevels[2]:
                self.trophyStar = loader.loadModelCopy('phase_3.5/models/gui/name_star')
                self.trophyStar.reparentTo(self.nametag.getNameIcon())
                self.trophyStar.setScale(1.5)
                self.trophyStar.setZ(1.6)
                self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[2])
                self.trophyStarSpeed = 10
                if self.trophyScore >= ToontownGlobals.TrophyStarLevels[3]:
                    taskMgr.add(self.__starSpin, self.uniqueName('starSpin'))
            else:
                if self.trophyScore >= ToontownGlobals.TrophyStarLevels[0]:
                    self.trophyStar = loader.loadModelCopy('phase_3.5/models/gui/name_star')
                    self.trophyStar.reparentTo(self.nametag.getNameIcon())
                    self.trophyStar.setScale(1.5)
                    self.trophyStar.setZ(1.6)
                    self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[0])
                    self.trophyStarSpeed = 8
                    if self.trophyScore >= ToontownGlobals.TrophyStarLevels[1]:
                        taskMgr.add(self.__starSpin, self.uniqueName('starSpin'))
        return

    def __starSpin(self, task):
        now = globalClock.getFrameTime()
        r = now * -self.trophyStarSpeed % 360.0
        self.trophyStar.setR(r)
        return Task.cont

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        avatar = toonbase.tcr.identifyFriend(avId)
        if avatar != None:
            if status == 1:
                self.setSystemMessage(avId, Localizer.WhisperNoLongerFriend % avatar.getName())
            else:
                if status == 2:
                    self.setSystemMessage(avId, Localizer.WhisperNowSpecialFriend % avatar.getName())
        return

    def d_battleSOS(self, requesterId, sendToId=None):
        self.sendUpdate('battleSOS', [requesterId], sendToId)

    def battleSOS(self, requesterId):
        avatar = toonbase.tcr.identifyAvatar(requesterId)
        if avatar != None:
            self.setSystemMessage(requesterId, Localizer.MovieSOSWhisperHelp % avatar.getName(), whisperType=WhisperPopup.WTBattleSOS)
        return

    def d_teleportQuery(self, requesterId, sendToId=None):
        self.sendUpdate('teleportQuery', [requesterId], sendToId)

    def teleportQuery(self, requesterId):
        avatar = toonbase.tcr.identifyAvatar(requesterId)
        if avatar != None:
            if requesterId in self.ignoreList:
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId=requesterId)
                return
            if self.__teleportAvailable:
                self.setSystemMessage(requesterId, Localizer.WhisperComingToVisit % avatar.getName())
                messenger.send('teleportQuery', [avatar, self])
                return
            if self.failedTeleportMessageOk(requesterId):
                self.setSystemMessage(requesterId, Localizer.WhisperFailedVisit % avatar.getName())
        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId=requesterId)
        return

    def failedTeleportMessageOk(self, fromId):
        now = globalClock.getFrameTime()
        lastTime = self.lastFailedTeleportMessage.get(fromId, None)
        if lastTime != None:
            elapsed = now - lastTime
            if elapsed < self.TeleportFailureTimeout:
                return 0
        self.lastFailedTeleportMessage[fromId] = now
        return 1
        return

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId, sendToId=None):
        self.sendUpdate('teleportResponse', [avId, available, shardId, hoodId, zoneId], sendToId)

    def teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        messenger.send('teleportResponse', [avId, available, shardId, hoodId, zoneId])

    def d_teleportGiveup(self, requesterId, sendToId=None):
        self.sendUpdate('teleportGiveup', [requesterId], sendToId)

    def teleportGiveup(self, requesterId):
        avatar = toonbase.tcr.identifyAvatar(requesterId)
        if avatar != None:
            self.setSystemMessage(requesterId, Localizer.WhisperGiveupVisit % avatar.getName())
        return

    def b_teleportGreeting(self, avId):
        self.d_teleportGreeting(avId)
        self.teleportGreeting(avId)

    def d_teleportGreeting(self, avId):
        self.sendUpdate('teleportGreeting', [avId])

    def teleportGreeting(self, avId):
        if toonbase.tcr.doId2do.has_key(avId):
            avatar = toonbase.tcr.doId2do[avId]
            self.setChatAbsolute(Localizer.TeleportGreeting % avatar.getName(), CFSpeech | CFTimeout)

    def setTeleportAvailable(self, available):
        self.__teleportAvailable = available

    def getTeleportAvailable(self):
        return self.__teleportAvailable

    def d_suggestResync(self, avId):
        self.sendUpdate('suggestResync', [avId])

    def suggestResync(self, avId):
        if toonbase.tcr.timeManager != None:
            toonbase.tcr.timeManager.synchronize('suggested by %d' % avId)
        return

    def getName(self):
        return Avatar.Avatar.getName(self)

    def setName(self, name):
        try:
            self.node().setName('%s-%d' % (name, self.doId))
            self.gotName = 1
        except:
            pass

        return Avatar.Avatar.setName(self, name)

    def showLaffNumber(self, number, bonus=0):
        if self.LaffNumbersEnabled:
            if number != 0:
                if self.laffNumber:
                    self.hideLaffNumber()
                self.LaffNumberGenerator.setFont(ToontownGlobals.getSignFont())
                if number < 0:
                    self.LaffNumberGenerator.setText(str(number))
                else:
                    self.LaffNumberGenerator.setText('+' + str(number))
                self.LaffNumberGenerator.clearShadow()
                self.LaffNumberGenerator.setAlign(TextNode.ACenter)
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                else:
                    if bonus == 2:
                        r = 1.0
                        g = 0.5
                        b = 0
                        a = 1
                    else:
                        if number < 0:
                            r = 0.9
                            g = 0
                            b = 0
                            a = 1
                        else:
                            r = 0
                            g = 0.9
                            b = 0
                            a = 1
                self.LaffNumberGenerator.setTextColor(r, g, b, a)
                self.laffNumberNode = self.LaffNumberGenerator.generate()
                self.laffNumber = self.attachNewNode(self.laffNumberNode)
                self.laffNumber.setBillboardAxis()
                self.laffNumber.setBin('fixed', 100)
                self.laffNumber.setPos(0, 0, self.height / 2)
                seq = Task.sequence(self.laffNumber.lerpPos(Point3(0, 0, self.height + 1.5), 1.0, blendType='easeOut'), Task.pause(0.85), self.laffNumber.lerpColor(Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.1), Task.Task(self.hideLaffNumberTask))
                taskMgr.add(seq, self.uniqueName('laffNumber'))
        return None
        return

    def showLaffString(self, text, duration=0.85, scale=0.7):
        if self.LaffNumbersEnabled:
            if text != '':
                if self.laffNumber:
                    self.hideLaffNumber()
                self.LaffNumberGenerator.setFont(ToontownGlobals.getSignFont())
                self.LaffNumberGenerator.setText(text)
                self.LaffNumberGenerator.clearShadow()
                self.LaffNumberGenerator.setAlign(TextNode.ACenter)
                r = a = 1.0
                g = b = 0.0
                self.LaffNumberGenerator.setTextColor(r, g, b, a)
                self.laffNumberNode = self.LaffNumberGenerator.generate()
                self.laffNumber = self.attachNewNode(self.laffNumberNode)
                self.laffNumber.setScale(scale)
                self.laffNumber.setBillboardAxis()
                self.laffNumber.setPos(0, 0, self.height / 2)
                seq = Task.sequence(self.laffNumber.lerpPos(Point3(0, 0, self.height + 1.5), 1.0, blendType='easeOut'), Task.pause(duration), self.laffNumber.lerpColor(Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.1), Task.Task(self.hideLaffNumberTask))
                taskMgr.add(seq, self.uniqueName('laffNumber'))
        return None
        return

    def hideLaffNumberTask(self, task):
        self.hideLaffNumber()
        return Task.done

    def hideLaffNumber(self):
        if self.laffNumber:
            taskMgr.remove(self.uniqueName('laffNumber'))
            self.laffNumber.removeNode()
            self.laffNumber = None
        return None
        return

    def getStareAtNodeAndOffset(self):
        return (
         self, Point3(0, 0, self.height))