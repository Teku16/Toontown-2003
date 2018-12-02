import ClothesGUI, AvatarDNA

class MakeClothesGUI(ClothesGUI.ClothesGUI):
    __module__ = __name__
    notify = directNotify.newCategory('MakeClothesGUI')

    def __init__(self, doneEvent):
        ClothesGUI.ClothesGUI.__init__(self, ClothesGUI.CLOTHES_MAKETOON, doneEvent)

    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        gender = self.dna.getGender()
        if gender != self.gender:
            self.tops = AvatarDNA.getRandomizedTops(gender, tailorId=AvatarDNA.MAKE_A_TOON)
            self.bottoms = AvatarDNA.getRandomizedBottoms(gender, tailorId=AvatarDNA.MAKE_A_TOON)
            self.gender = gender
            self.topChoice = 0
            self.bottomChoice = 0
        self.setupButtons()

    def setupButtons(self):
        ClothesGUI.ClothesGUI.setupButtons(self)
        if len(self.dna.torso) == 1:
            if self.gender == 'm':
                torsoStyle = 's'
            else:
                if self.girlInShorts == 1:
                    torsoStyle = 's'
                else:
                    torsoStyle = 'd'
            self.toon.swapToonTorso(self.dna.torso[0] + torsoStyle)
            self.toon.loop('neutral', 0)
            self.toon.swapToonColor(self.dna)
            self.swapTop(0)
            self.swapBottom(0)
        return None
        return