import ShtikerPage, ToontownGlobals, PythonUtil, ZoneUtil
from DirectGui import *
import Localizer

class MapPage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        mapModel = loader.loadModel('phase_3.5/models/gui/toontown_map')
        self.map = DirectFrame(parent=self, relief=None, image=mapModel.find('**/toontown_map'), image_scale=(1.8, 1, 1.35), scale=0.97, pos=(0, 0, 0.0775))
        mapModel.removeNode()
        self.allZones = [
         ToontownGlobals.DonaldsDock, ToontownGlobals.ToontownCentral, ToontownGlobals.TheBrrrgh, ToontownGlobals.MinniesMelodyland, ToontownGlobals.DaisyGardens, ToontownGlobals.ConstructionZone, ToontownGlobals.FunnyFarm, ToontownGlobals.GoofyStadium, ToontownGlobals.DonaldsDreamland, ToontownGlobals.BossbotHQ, ToontownGlobals.SellbotHQ, ToontownGlobals.CashbotHQ, ToontownGlobals.LawbotHQ]
        self.cloudScaleList = (
         (
          -0.5,), (), (0.4, 0.5), (0.65,), (0.6, -0.45), (0.5, 0.4), (-0.45, -0.6), (0.55,), (0.6,), (0.4,), (0.4,), (-0.4,), (-0.45,))
        self.cloudSquishList = (
         (
          1,), (), (1, 1), (0.7,), (0.5, 0.8), (0.85, 0.8), (0.7, 0.85), (1,), (0.65,), (1,), (1,), (1,), (1,))
        self.cloudPosList = (
         (
          (
           0.47, 0.0, -0.07),), (), ((0.3, 0.0, 0.4), (0.45, 0.0, 0.3)), ((-0.05, 0.0, 0.23),), ((-0.25, 0.0, -0.5), (-0.33, 0.0, -0.4)), ((0.28, 0.0, -0.45), (0.15, 0.0, -0.45)), ((-0.5, 0.0, 0.15), (-0.45, 0.0, 0.32)), ((-0.45, 0.0, -0.1),), ((-0.1, 0.0, 0.5),), ((-0.55, 0.0, 0.5),), ((0.55, 0.0, 0.5),), ((-0.55, 0.0, -0.5),), ((0.55, 0.0, -0.43),))
        self.labelPosList = (
         (
          0.594, 0.0, -0.075), (0.0, 0.0, -0.2), (0.475, 0.0, 0.25), (0.063, 0.0, 0.15), (-0.25, 0.0, -0.475), (0.313, 0.0, -0.475), (-0.438, 0.0, 0.22), (-0.55, 0.0, -0.125), (-0.088, 0.0, 0.47), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
        self.labels = []
        self.clouds = []
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        buttonLoc = (
         0.45, 0, -0.74)
        if toonbase.housingEnabled:
            buttonLoc = (0.55, 0, -0.74)
        self.safeZoneButton = DirectButton(parent=self.map, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.3, 1.1, 1.1), pos=buttonLoc, text=Localizer.MapPageBackToPlayground, text_scale=0.055, text_pos=(0, -0.02), textMayChange=0, command=self.backToSafeZone)
        self.goHomeButton = DirectButton(parent=self.map, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.66, 1.1, 1.1), pos=(0.15, 0, -0.74), text=Localizer.MapPageGoHome, text_scale=0.055, text_pos=(0, -0.02), textMayChange=0, command=self.goHome)
        self.goHomeButton.hide()
        guiButton.removeNode()
        self.hoodLabel = DirectLabel(parent=self.map, relief=None, pos=(-0.43, 0, -0.726), text='', text_scale=0.06, text_pos=(0, 0), text_wordwrap=14)
        self.hoodLabel.hide()
        cloudModel = loader.loadModel('phase_3.5/models/gui/cloud')
        cloudImage = cloudModel.find('**/cloud')
        for hood in self.allZones:
            abbrev = toonbase.tcr.hoodMgr.getNameFromId(hood)
            fullname = toonbase.tcr.hoodMgr.getFullnameFromId(hood)
            hoodIndex = self.allZones.index(hood)
            label = DirectButton(parent=self.map, relief=None, pos=self.labelPosList[hoodIndex], pad=(0.2, 0.16), text=('', fullname, fullname), text_bg=Vec4(1, 1, 1, 0.4), text_scale=0.055, rolloverSound=None, clickSound=None, pressEffect=0, command=self.__buttonCallback, extraArgs=[hood])
            label.resetFrameSize()
            self.labels.append(label)
            hoodClouds = []
            for cloudScale, cloudPos, cloudSquish in zip(self.cloudScaleList[hoodIndex], self.cloudPosList[hoodIndex], self.cloudSquishList[hoodIndex]):
                cloud = DirectFrame(parent=self.map, relief=None, state=DISABLED, image=cloudImage, scale=(cloudScale * 1.333, abs(cloudScale), abs(cloudScale) * cloudSquish), pos=(cloudPos[0] * 1.25, cloudPos[1], cloudPos[2]))
                cloud.hide()
                hoodClouds.append(cloud)

            self.clouds.append(hoodClouds)

        cloudModel.removeNode()
        self.resetFrameSize()
        return
        return

    def unload(self):
        del self.labels
        del self.clouds
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        try:
            zone = toonbase.tcr.playGame.getPlace().getZoneId()
        except:
            zone = 0
        else:
            if zone and ZoneUtil.isPlayground(zone) or self.book.safeMode:
                self.safeZoneButton.hide()
            else:
                self.safeZoneButton.show()
            if toonbase.localToon.estate != None and toonbase.tcr.playGame.estateLoader.atMyEstate() or self.book.safeMode:
                self.goHomeButton.hide()
            else:
                if toonbase.housingEnabled:
                    self.goHomeButton.show()
            if toonbase.tcr.playGame.hood == None and toonbase.tcr.playGame.estateLoader != None:
                if toonbase.tcr.playGame.estateLoader.atMyEstate():
                    self.hoodLabel['text'] = Localizer.MapPageYouAreAtHome
                    self.hoodLabel.show()
                else:
                    avatar = toonbase.tcr.identifyAvatar(toonbase.tcr.playGame.estateLoader.estateOwnerId)
                    if avatar:
                        avName = avatar.getName()
                        self.hoodLabel['text'] = Localizer.MapPageYouAreAtSomeonesHome % Localizer.GetPossesive(avName)
                        self.hoodLabel.show()
            else:
                if zone:
                    hoodName = ToontownGlobals.hoodNameMap.get(ZoneUtil.getHoodId(zone), ('', ''))[1]
                    streetName = ToontownGlobals.StreetNames.get(ZoneUtil.getBranchZone(zone), ('', ''))[1]
                    if hoodName:
                        self.hoodLabel['text'] = Localizer.MapPageYouAreHere % (hoodName, streetName)
                        self.hoodLabel.show()
                    else:
                        self.hoodLabel.hide()
                else:
                    self.hoodLabel.hide()
            if toonbase.localToon.teleportCheat:
                safeZonesVisited = ToontownGlobals.Hoods
            else:
                safeZonesVisited = toonbase.localToon.safeZonesVisited
            hoodsAvailable = toonbase.tcr.hoodMgr.getAvailableZones()
            hoodVisibleList = PythonUtil.intersection(safeZonesVisited, hoodsAvailable)
            if toonbase.localToon.teleportCheat:
                hoodTeleportList = hoodVisibleList
            else:
                hoodTeleportList = toonbase.localToon.getTeleportAccess()
            for hood in self.allZones:
                label = self.labels[self.allZones.index(hood)]
                clouds = self.clouds[self.allZones.index(hood)]
                if not self.book.safeMode and hood in hoodVisibleList:
                    label.show()
                    for cloud in clouds:
                        cloud.hide()

                    fullname = toonbase.tcr.hoodMgr.getFullnameFromId(hood)
                    if hood in hoodTeleportList:
                        text = Localizer.MapPageGoTo % fullname
                        label['text'] = ('', text, text)
                    else:
                        label['text'] = (
                         '', fullname, fullname)
                label.hide()
                for cloud in clouds:
                    cloud.show()

        return
        return

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def backToSafeZone(self):
        self.doneStatus = {'mode': 'teleport', 'hood': toonbase.localToon.lastHood}
        messenger.send(self.doneEvent)

    def goHome(self):
        self.doneStatus = {'mode': 'gohome', 'hood': toonbase.localToon.lastHood}
        messenger.send(self.doneEvent)

    def __buttonCallback(self, hood):
        if toonbase.localToon.teleportCheat or hood in toonbase.localToon.getTeleportAccess():
            self.doneStatus = {'mode': 'teleport', 'hood': hood}
            messenger.send(self.doneEvent)