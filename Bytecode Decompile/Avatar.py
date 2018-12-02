from ShowBaseGlobal import *
from PandaObject import *
from PandaModules import *
import ToontownGlobals, Actor, AvatarDNA, ClockDelta, Localizer

def reconsiderAllUnderstandable():
    for av in Avatar.ActiveAvatars:
        av.considerUnderstandable()


class Avatar(Actor.Actor):
    __module__ = __name__
    notify = Actor.directNotify.newCategory('Avatar')
    ActiveAvatars = []

    def __init__(self):
        try:
            self.Avatar_initialized
        except:
            self.Avatar_initialized = 1
            Actor.Actor.__init__(self)
            self.__font = ToontownGlobals.getToonFont()
            self.soundChatBubble = base.loadSfx('phase_3/audio/sfx/GUI_balloon_popup.mp3')
            self.__nameVisible = 1
            self.nametag = NametagGroup()
            self.nametag.setAvatar(self)
            self.nametag.setFont(ToontownGlobals.getInterfaceFont())
            self.nametag2dContents = Nametag.CName | Nametag.CSpeech
            self.nametag2dDist = Nametag.CName | Nametag.CSpeech
            self.nametag3d = self.attachNewNode('nametag3d')
            self.dropShadows = []
            self.scale = 1.0
            self.nametagScale = 1.0
            self.height = 0.0
            self.name = ''
            self.style = None
            self.commonChatFlags = 0
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCNormal)
            self.__chatParagraph = None
            self.__chatMessage = None
            self.__chatFlags = 0
            self.__chatPageNumber = None
            self.__chatAddressee = None
            self.__chatSet = 0
            self.__chatLocal = 0

        return None
        return

    def delete(self):
        try:
            self.Avatar_deleted
        except:
            self.Avatar_deleted = 1
            del self.__font
            del self.style
            self.deleteNametag3d()
            del self.soundChatBubble
            del self.nametag
            self.nametag3d.removeNode()
            self.deleteDropShadow()
            Actor.Actor.delete(self)

    def setPlayerType(self, playerType):
        self.playerType = playerType
        if self.isUnderstandable():
            self.nametag.setColorCode(self.playerType)
        else:
            self.nametag.setColorCode(NametagGroup.CCNoChat)

    def setCommonChatFlags(self, commonChatFlags):
        self.commonChatFlags = commonChatFlags
        self.considerUnderstandable()
        if self == toonbase.localToon:
            reconsiderAllUnderstandable()

    def considerUnderstandable(self):
        if self == toonbase.localToon:
            self.understandable = 1
        else:
            if self.playerType != NametagGroup.CCNormal:
                self.understandable = 1
            else:
                if self.commonChatFlags & toonbase.localToon.commonChatFlags & ToontownGlobals.CommonChat:
                    self.understandable = 1
                else:
                    if self.commonChatFlags & ToontownGlobals.SuperChat:
                        self.understandable = 1
                    else:
                        if toonbase.localToon.commonChatFlags & ToontownGlobals.SuperChat:
                            self.understandable = 1
                        else:
                            if toonbase.tcr.getFriendFlags(self.doId) & ToontownGlobals.FriendChat:
                                self.understandable = 1
                            else:
                                self.understandable = 0
        if self.understandable:
            self.nametag.setColorCode(self.playerType)
        else:
            self.nametag.setColorCode(NametagGroup.CCNoChat)

    def isUnderstandable(self):
        return self.understandable

    def setDNAString(self, dnaString):
        newDNA = AvatarDNA.AvatarDNA()
        newDNA.makeFromNetString(dnaString)
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.style:
            type = dna.type
            if type == AvatarDNA.toonType:
                self.updateToonDNA(dna)
            else:
                if type == AvatarDNA.charType:
                    self.updateCharDNA(dna)
        else:
            self.style = dna
            type = dna.type
            if type == AvatarDNA.toonType:
                self.generateToon()
            else:
                if type == AvatarDNA.suitType:
                    self.generateSuit()
                else:
                    if type == AvatarDNA.charType:
                        self.generateChar()
                    else:
                        Avatar.notify.error('unknown DNA type: %s' % type)
            self.initializeDropShadow()
            self.initializeNametag3d()
        return None
        return

    def getAvatarScale(self):
        return self.scale

    def setAvatarScale(self, scale):
        if self.scale != scale:
            self.scale = scale
            self.getGeomNode().setScale(scale)
            self.setHeight(self.height)

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height
        self.nametag3d.setPos(0, 0, height + 0.5)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.nametag.setName(name)

    def getFont(self):
        return self.__font

    def setFont(self, font):
        self.__font = font
        self.nametag.setFont(font)

    def getStyle(self):
        return self.style

    def setStyle(self, style):
        self.style = style

    def playDialogue(self, type, length):
        pass

    def playDialogueForString(self, chatString):
        searchString = string.lower(chatString)
        if string.find(searchString, Localizer.DialogSpecial) >= 0:
            type = 'special'
        else:
            if string.find(searchString, Localizer.DialogExclamation) >= 0:
                type = 'exclamation'
            else:
                if string.find(searchString, Localizer.DialogQuestion) >= 0:
                    type = 'question'
                else:
                    animal = self.getStyle().getType()
                    if animal == 'dog' or animal == 'horse' or animal == 'duck':
                        type = 'statementA'
                    else:
                        type = 'statementB'
        stringLength = len(chatString)
        if stringLength <= Localizer.DialogLength1:
            length = 1
        else:
            if stringLength <= Localizer.DialogLength2:
                length = 2
            else:
                if stringLength <= Localizer.DialogLength3:
                    length = 3
                else:
                    length = 4
        self.playDialogue(type, length)
        return None
        return

    def setChatAbsolute(self, chatString, chatFlags):
        self.nametag.setChat(chatString, chatFlags)
        if chatFlags & CFSpeech != 0 and self.nametag.getNumChatPages() > 0:
            if self.getDistance(camera) < 100.0:
                self.playDialogueForString(self.nametag.getChat())
                base.playSfx(self.soundChatBubble, node=self)

    def clearChat(self):
        self.nametag.clearChat()

    def isInView(self):
        pos = self.getPos(camera)
        eyePos = Point3(pos[0], pos[1], pos[2] + self.getHeight())
        return base.camNode.isInView(eyePos)

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        self.nametag2dContents = Nametag.CName | Nametag.CSpeech
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def setPickable(self, flag):
        self.nametag.setActive(flag)

    def clickedNametag(self):
        if self.nametag.hasButton():
            self.advancePageNumber()
        else:
            messenger.send('clickedNametag', [self])

    def setPageChat(self, addressee, paragraph, message, quitButton, extraChatFlags=None):
        self.__chatAddressee = addressee
        self.__chatPageNumber = None
        self.__chatParagraph = paragraph
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__updatePageChat()
        if addressee == toonbase.localToon.doId:
            self.__chatFlags |= CFPageButton
            if quitButton:
                self.__chatFlags |= CFQuitButton
            self.b_setPageNumber(self.__chatParagraph, 0)
        return

    def setLocalPageChat(self, message, quitButton, extraChatFlags=None):
        self.__chatAddressee = toonbase.localToon.doId
        self.__chatPageNumber = None
        self.__chatParagraph = None
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatSet = 1
        self.__chatLocal = 1
        self.__chatFlags |= CFPageButton
        if quitButton:
            self.__chatFlags |= CFQuitButton
        self.setChatAbsolute(message, self.__chatFlags)
        self.setPageNumber(None, 0)
        return

    def setPageNumber(self, paragraph, pageNumber, timestamp=None):
        if timestamp == None:
            elapsed = 0.0
        else:
            elapsed = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.__chatPageNumber = [paragraph, pageNumber]
        self.__updatePageChat()
        if hasattr(self, 'uniqueName'):
            if pageNumber >= 0:
                messenger.send(self.uniqueName('nextChatPage'), [
                 pageNumber, elapsed])
            else:
                messenger.send(self.uniqueName('doneChatPage'), [
                 elapsed])
        return

    def advancePageNumber(self):
        if self.__chatAddressee == toonbase.localToon.doId and self.__chatPageNumber != None and self.__chatPageNumber[0] == self.__chatParagraph:
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                pageNumber += 1
                if pageNumber >= self.nametag.getNumChatPages():
                    pageNumber = -1
                if self.__chatLocal:
                    self.setPageNumber(self.__chatParagraph, pageNumber)
                else:
                    self.b_setPageNumber(self.__chatParagraph, pageNumber)
        return

    def __updatePageChat(self):
        if self.__chatPageNumber != None and self.__chatPageNumber[0] == self.__chatParagraph:
            if self.__chatPageNumber[1] >= 0:
                if not self.__chatSet:
                    self.setChatAbsolute(self.__chatMessage, self.__chatFlags)
                    self.__chatSet = 1
                if self.__chatPageNumber[1] < self.nametag.getNumChatPages():
                    self.nametag.setPageNumber(self.__chatPageNumber[1])
                else:
                    self.clearChat()
            else:
                self.clearChat()
        return

    def initializeDropShadow(self):
        self.deleteDropShadow()
        self.getGeomNode().setZ(0.025)
        dropShadow = loader.loadModelCopy('phase_3/models/props/drop_shadow')
        dropShadow.setScale(0.4)
        self.dropShadows = []
        for shadowJoint in self.getShadowJoints():
            copy = dropShadow.copyTo(shadowJoint)
            copy.flattenMedium()
            copy.setBillboardAxis(2)
            copy.setColor(0.0, 0.0, 0.0, 0.5, 1)
            self.dropShadows.append(copy)

        dropShadow.removeNode()

    def deleteDropShadow(self):
        for shadow in self.dropShadows:
            shadow.removeNode()

        self.dropShadows = []

    def initializeNametag3d(self):
        self.deleteNametag3d()
        nametagNode = self.nametag.getNametag3d().upcastToPandaNode()
        self.nametag3d.attachNewNode(nametagNode)
        iconNodePath = self.nametag.getNameIcon()
        for cJoint in self.getNametagJoints():
            cJoint.clearNetTransforms()
            cJoint.addNetTransform(nametagNode)

    def deleteNametag3d(self):
        children = self.nametag3d.getChildren()
        for i in range(children.getNumPaths()):
            children[i].removeNode()

    def initializeBodyCollisions(self, collIdStr):
        self.collSphere = CollisionSphere(0, 0, 0.5, 1.0)
        self.collNode = CollisionNode(collIdStr)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.attachNewNode(self.collNode)
        self.collNodePath.hide()
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        return None
        return

    def disableBodyCollisions(self):
        self.collNodePath.removeNode()
        del self.collNodePath
        del self.collNode
        del self.collSphere

    def addActive(self):
        self.notify.debug('Adding avatar %s' % self.getName())
        try:
            Avatar.ActiveAvatars.remove(self)
        except ValueError:
            pass

        Avatar.ActiveAvatars.append(self)
        self.nametag.manage(toonbase.marginManager)
        self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        self.notify.debug('Removing avatar %s' % self.getName())
        try:
            Avatar.ActiveAvatars.remove(self)
        except ValueError:
            self.notify.warning('%s was not present...' % self.getName())

        self.nametag.unmanage(toonbase.marginManager)
        self.ignore(self.nametag.getUniqueId())