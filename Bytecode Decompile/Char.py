import Avatar
from PandaModules import *
import Task, whrandom
from ShowBaseGlobal import *
MickeyDialogueArray = []
MinnieDialogueArray = []
GoofyDialogueArray = []
DonaldDialogueArray = []
PlutoDialogueArray = []
AnimDict = {'mk': (('walk', '-walk', 3), ('run', '-run', 3), ('neutral', '-wait', 3), ('left-point-start', '-left-start', 3.5), ('left-point', '-left', 3.5), ('right-point-start', '-right-start', 3.5), ('right-point', '-right', 3.5)), 'mn': (('walk', '-walk', 3), ('run', '-run', 3), ('neutral', '-wait', 3), ('left-point-start', '-start-Lpoint', 3.5), ('left-point', '-Lpoint', 3.5), ('right-point-start', '-start-Rpoint', 3.5), ('right-point', '-Rpoint', 3.5), ('up', '-up', 4), ('down', '-down', 4), ('left', '-left', 4), ('right', '-right', 4)), 'g': (('walk', 'Walk', 6), ('run', 'Run', 6), ('neutral', 'Wait', 6)), 'd': (('walk', '-walk', 6), ('trans', '-transition', 6), ('neutral', '-neutral', 6), ('trans-back', '-transBack', 6)), 'dw': (('wheel', '-wheel', 6),), 'p': (('walk', '-walk', 6), ('sit', '-sit', 6), ('neutral', '-neutral', 6), ('stand', '-stand', 6))}
ModelDict = {'mk': 'phase_3/models/char/mickey', 'mn': 'phase_3/models/char/minnie', 'g': 'phase_6/models/char/TT_G', 'd': 'phase_6/models/char/DL_donald', 'dw': 'phase_6/models/char/donald-wheel', 'p': 'phase_6/models/char/pluto'}
LODModelDict = {'mk': [1200, 800, 400], 'mn': [1200, 800, 400], 'g': [1500, 1000, 500], 'd': [1000, 500, 250], 'dw': [1000], 'p': [1000, 500, 300]}

def loadDialogue(char):
    global DonaldDialogueArray
    global GoofyDialogueArray
    global MickeyDialogueArray
    global MinnieDialogueArray
    global PlutoDialogueArray
    if char == 'mk':
        dialogueFile = base.loadSfx('phase_3/audio/dial/mickey.wav')
        for i in range(0, 6):
            MickeyDialogueArray.append(dialogueFile)

    else:
        if char == 'mn':
            dialogueFile = base.loadSfx('phase_3/audio/dial/minnie.wav')
            for i in range(0, 6):
                MinnieDialogueArray.append(dialogueFile)

        else:
            if char == 'g':
                dialogueFile = base.loadSfx('phase_6/audio/dial/goofy.wav')
                for i in range(0, 6):
                    GoofyDialogueArray.append(dialogueFile)

            else:
                if char == 'd' or char == 'dw':
                    dialogueFile = base.loadSfx('phase_6/audio/dial/donald.wav')
                    for i in range(0, 6):
                        DonaldDialogueArray.append(dialogueFile)

                else:
                    if char == 'p':
                        dialogueFile = base.loadSfx('phase_3.5/audio/dial/AV_dog_med.mp3')
                        for i in range(0, 6):
                            PlutoDialogueArray.append(dialogueFile)

                    else:
                        print 'Error: unknown character %s' % char


def unloadDialogue(char):
    global DonaldDialogueArray
    global GoofyDialogueArray
    global MickeyDialogueArray
    global MinnieDialogueArray
    global PlutoDialogueArray
    if char == 'mk':
        MickeyDialogueArray = []
    else:
        if char == 'mn':
            MinnieDialogueArray = []
        else:
            if char == 'g':
                GoofyDialogueArray = []
            else:
                if char == 'd' or char == 'dw':
                    DonaldDialogueArray = []
                else:
                    if char == 'p':
                        PlutoDialogueArray = []
                    else:
                        print 'Error: unknown character %s' % char


class Char(Avatar.Avatar):
    __module__ = __name__

    def __init__(self):
        try:
            self.Char_initialized
        except:
            self.Char_initialized = 1
            Avatar.Avatar.__init__(self)
            self.setPickable(0)
            self.setPlayerType(NametagGroup.CCNonPlayer)

        return None
        return

    def delete(self):
        try:
            self.Char_deleted
        except:
            self.Char_deleted = 1
            unloadDialogue(self.style.name)
            filePrefix = ModelDict[self.style.name]
            for lodStr in self.lodStrings:
                loader.unloadModel(filePrefix + '-' + lodStr)

            animList = AnimDict[self.style.name]
            for anim in animList:
                animFilePrefix = filePrefix[:6] + str(anim[2]) + filePrefix[7:]
                loader.unloadModel(animFilePrefix + anim[1])

            Avatar.Avatar.delete(self)

        return None
        return

    def updateCharDNA(self, newDNA):
        if newDNA.name != self.style.name:
            self.swapCharModel(newDNA)

    def setLODs(self):
        self.setLODNode()
        levelOneIn = base.config.GetInt('lod1-in', 50)
        levelOneOut = base.config.GetInt('lod1-out', 1)
        levelTwoIn = base.config.GetInt('lod2-in', 100)
        levelTwoOut = base.config.GetInt('lod2-out', 50)
        levelThreeIn = base.config.GetInt('lod3-in', 280)
        levelThreeOut = base.config.GetInt('lod3-out', 100)
        self.addLOD(LODModelDict[self.style.name][2], levelThreeIn, levelThreeOut)
        self.addLOD(LODModelDict[self.style.name][1], levelTwoIn, levelTwoOut)
        self.addLOD(LODModelDict[self.style.name][0], levelOneIn, levelOneOut)

    def generateChar(self):
        dna = self.style
        self.name = dna.getCharName()
        if len(LODModelDict[dna.name]) > 1:
            self.setLODs()
        filePrefix = ModelDict[dna.name]
        if self.name == 'mickey':
            height = 3.0
        else:
            if self.name == 'minnie':
                height = 3.0
            else:
                if self.name == 'goofy':
                    height = 4.8
                else:
                    if self.name == 'donald' or self.name == 'donald-wheel':
                        height = 4.5
                    else:
                        if self.name == 'pluto':
                            height = 3.0
        self.lodStrings = []
        for lod in LODModelDict[self.style.name]:
            self.lodStrings.append(str(lod))

        for lodStr in self.lodStrings:
            if len(self.lodStrings) > 1:
                lodName = lodStr
            else:
                lodName = 'lodRoot'
            self.loadModel(filePrefix + '-' + lodStr, lodName=lodName)

        animDict = {}
        animList = AnimDict[self.style.name]
        for anim in animList:
            animFilePrefix = filePrefix[:6] + str(anim[2]) + filePrefix[7:]
            animDict[anim[0]] = animFilePrefix + anim[1]

        for lodStr in self.lodStrings:
            if len(self.lodStrings) > 1:
                lodName = lodStr
            else:
                lodName = 'lodRoot'
            self.loadAnims(animDict, lodName=lodName)

        self.setHeight(height)
        loadDialogue(dna.name)
        self.ears = []
        if self.name == 'mickey' or self.name == 'minnie':
            for bundle in self.getPartBundleDict().values():
                charNodepath = bundle['modelRoot']
                char = charNodepath.node()
                earNull = char.getBundle().findChild('sphere3')
                earNull.clearNetTransforms()
                ears = charNodepath.find('**/sphere3')
                earRoot = charNodepath.attachNewNode('earRoot')
                earPitch = earRoot.attachNewNode('earPitch')
                earPitch.setP(40.0)
                ears.reparentTo(earPitch)
                earNull.addNetTransform(earRoot.node())
                ears.clearMat()
                ears.setP(-40.0)
                ears.flattenMedium()
                self.ears.append(ears)
                ears.setBillboardAxis()

        self.eyes = None
        self.lpupil = None
        self.rpupil = None
        self.eyesOpen = None
        self.eyesClosed = None
        if self.name == 'mickey' or self.name == 'minnie':
            self.eyesOpen = loader.loadTexture('phase_3/maps/eyes1.jpg', 'phase_3/maps/eyes1_a.rgb')
            self.eyesClosed = loader.loadTexture('phase_3/maps/mickey_eyes_closed.jpg', 'phase_3/maps/mickey_eyes_closed_a.rgb')
            self.eyes = self.find('**/1200/**/eyes')
            self.eyes.setBin('transparent', 0)
            self.lpupil = self.find('**/1200/**/joint-pupilL')
            self.rpupil = self.find('**/1200/**/joint-pupilR')
            for lodName in self.getLODNames():
                self.drawInFront('joint-pupil?', 'eyes*', -3, lodName=lodName)

        else:
            if self.name == 'pluto':
                self.eyesOpen = loader.loadTexture('phase_6/maps/plutoEyesOpen.jpg', 'phase_6/maps/plutoEyesOpen_a.rgb')
                self.eyesClosed = loader.loadTexture('phase_6/maps/plutoEyesClosed.jpg', 'phase_6/maps/plutoEyesClosed_a.rgb')
                self.eyes = self.find('**/1000/**/eyes')
                self.lpupil = self.find('**/1000/**/joint-pupilL')
                self.rpupil = self.find('**/1000/**/joint-pupilR')
                for lodName in self.getLODNames():
                    self.drawInFront('joint-pupil?', 'eyes*', -3, lodName=lodName)

            else:
                if self.name == 'donald-wheel':
                    self.eyes = self.find('**/eyes')
                    self.lpupil = self.find('**/joint-pupilL')
                    self.rpupil = self.find('**/joint-pupilR')
                    self.drawInFront('joint-pupil?', 'eyes*', -3)
        if self.lpupil != None:
            self.lpupil.adjustAllPriorities(1)
            self.rpupil.adjustAllPriorities(1)
        if self.eyesOpen:
            self.eyesOpen.setMinfilter(Texture.FTLinear)
            self.eyesOpen.setMagfilter(Texture.FTLinear)
        if self.eyesClosed:
            self.eyesClosed.setMinfilter(Texture.FTLinear)
            self.eyesClosed.setMagfilter(Texture.FTLinear)
        if self.name == 'mickey':
            pupilParent = self.rpupil.getParent()
            pupilOffsetNode = pupilParent.attachNewNode('pupilOffsetNode')
            pupilOffsetNode.setPos(0, 0.025, 0)
            self.rpupil.reparentTo(pupilOffsetNode)
        self.__blinkName = 'blink-' + self.name
        return

    def swapCharModel(self, charStyle):
        for lodStr in self.lodStrings:
            if len(self.lodStrings) > 1:
                lodName = lodStr
            else:
                lodName = 'lodRoot'
            self.removePart('modelRoot', lodName=lodName)

        self.setStyle(charStyle)
        self.generateChar()

    def playDialogue(self, type, length):
        animalType = self.style.getType()
        if animalType == 'mickey':
            dialogueArray = MickeyDialogueArray
        else:
            if animalType == 'minnie':
                dialogueArray = MinnieDialogueArray
            else:
                if animalType == 'goofy':
                    dialogueArray = GoofyDialogueArray
                else:
                    if animalType == 'donald' or animalType == 'donald-wheel':
                        dialogueArray = DonaldDialogueArray
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            else:
                if length == 2:
                    sfxIndex = 1
                else:
                    if length >= 3:
                        sfxIndex = 2
        else:
            if type == 'question':
                sfxIndex = 3
            else:
                if type == 'exclamation':
                    sfxIndex = 4
                else:
                    if type == 'special':
                        sfxIndex = 5
                    else:
                        notify.error('unrecognized dialogue type: ', type)
        if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
            base.playSfx(dialogueArray[sfxIndex])
        return

    def getShadowJoints(self):
        return [
         self.getGeomNode()]

    def getNametagJoints(self):
        return []

    def __blinkOpenEyes(self, task):
        self.openEyes()
        r = whrandom.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        self.closeEyes()
        taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def openEyes(self):
        self.eyes.setTexture(self.eyesOpen, 1)
        self.lpupil.show()
        self.rpupil.show()

    def closeEyes(self):
        self.eyes.setTexture(self.eyesClosed, 1)
        self.lpupil.hide()
        self.rpupil.hide()

    def startBlink(self):
        if self.eyesOpen:
            taskMgr.remove(self.__blinkName)
            taskMgr.doMethodLater(whrandom.random() * 4 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        if self.eyesOpen:
            taskMgr.remove(self.__blinkName)
            self.openEyes()

    def startEarTask(self):
        pass

    def stopEarTask(self):
        pass

    def uniqueName(self, idString):
        return idString + '-' + str(self.this)