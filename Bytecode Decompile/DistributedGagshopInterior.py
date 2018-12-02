from ToonBaseGlobal import *
from ShowBaseGlobal import *
from ToontownGlobals import *
import random, DistributedObject, DirectNotifyGlobal, ToonInteriorColors, DNADoor, ZoneUtil

class DistributedGagshopInterior(DistributedObject.DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore = cr.playGame.dnaStore

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def replaceRandomInModel(self, model):
        baseTag = 'random_'
        npc = model.findAllMatches('**/' + baseTag + '???_*')
        for i in range(npc.getNumPaths()):
            np = npc.getPath(i)
            name = np.getName()
            b = len(baseTag)
            category = name[b + 4:]
            key1 = name[b]
            key2 = name[b + 1]
            if key1 == 'm':
                model = self.randomDNAItem(category, self.dnaStore.findNode)
                newNP = model.copyTo(np)
                if key2 == 'r':
                    self.replaceRandomInModel(newNP)
            else:
                if key1 == 't':
                    texture = self.randomDNAItem(category, self.dnaStore.findTexture)
                    np.setTexture(texture, 100)
                    newNP = np
            if key2 == 'c':
                newNP.setColorScale(self.randomGenerator.choice(self.colors[category]))

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def chooseDoor(self):
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        return door

    def setup(self):
        self.dnaStore = toonbase.tcr.playGame.dnaStore
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)
        self.interior = loader.loadModel('phase_4/models/modules/gagShop_interior')
        self.interior.reparentTo(render)
        hoodId = ZoneUtil.getHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)
        door = self.chooseDoor()
        doorOrigin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(doorOrigin)
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
        doorColor = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.DNADoor.setupDoor(doorNP, self.interior, doorOrigin, self.dnaStore, str(self.block), doorColor)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)
        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()

    def disable(self):
        self.interior.removeNode()
        del self.interior