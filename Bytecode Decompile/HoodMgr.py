from ShowBaseGlobal import *
import DirectObject, DirectNotifyGlobal, DownloadForceAcknowledge, string, whrandom
from ToontownGlobals import *
import ZoneUtil

class HoodMgr(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('HoodMgr')
    DonaldsDock_drop_points = (
     [
      -28.0, -2.5, 5.8, 120.0, 0.0, 0.0], [-22, 13, 5.8, 155.6, 0.0, 0.0], [67, 47, 5.7, 134.7, 0.0, 0.0], [62, 19, 5.7, 97.0, 0.0, 0.0], [66, -27, 5.7, 80.5, 0.0, 0.0], [-114, -7, 5.7, -97.0, -0.0, 0.0], [-108, 36, 5.7, -153.8, -0.0, 0.0], [-116, -46, 5.7, -70.1, -0.0, 0.0], [-63, -79, 5.7, -41.2, -0.0, 0.0], [-2, -79, 5.7, 57.4, -0.0, 0.0], [-38, -78, 5.7, 9.1, -0.0, 0.0])
    ToontownCentral_drop_points = (
     [
      -60, -8, 1.3, -90, 0, 0], [-66, -9, 1.3, -274, 0, 0], [17, -28, 4.1, -44, 0, 0], [87.7, -22, 4, 66, 0, 0], [-9.6, 61.1, 0, 132, 0, 0], [-109.0, -2.5, -1.656, -90, 0, 0], [-35.4, -81.3, 0.5, -4, 0, 0], [-103, 72, 0, -141, 0, 0], [95.5, -147.4, 2.5, 43, 0, 0], [25, 123.4, 2.55, 272, 0, 0], [48, 39, 4, 201, 0, 0], [-80, -61, 0.1, -265, 0, 0], [-46.875, 43.68, -1.05, 124, 0, 0])
    ToontownCentral_initial_drop_points = (
     [
      -90.7, -60.0, 0.025, 102.575, 0, 0], [-91.4, -40.5, -3.948, 125.763, 0, 0], [-107.8, -17.8, -1.937, 149.456, 0, 0], [-108.7, 12.8, -1.767, 158.756, 0, 0], [-42.1, -22.8, -1.328, -248.1, 0, 0], [-35.2, -60.2, 0.025, -265.639, 0, 0])
    ToontownCentral_hq_drop_points = (
     [
      -43.5, 42.6, -0.55, -100.454, 0, 0], [-53.0, 12.5, -2.948, 281.502, 0, 0], [-40.3, -18.5, -0.913, -56.674, 0, 0], [-1.9, -37.0, 0.025, -23.43, 0, 0], [1.9, -5.9, 4.0, -37.941, 0, 0])
    Brggh_drop_points = (
     [
      35, -32, 6.2, 138, 0.0, 0.0], [26, -105, 6.2, -339, 0.0, 0.0], [-29, -139, 6.2, -385, 0.0, 0.0], [-79, -123, 6.2, -369, 0.0, 0.0], [-114, -86, 3, -54, 0.0, 0.0], [-136, 9, 6.2, -125, 0.0, 0.0], [-75, 92, 6.2, -187, 0.0, 0.0], [-7, 75, 6.2, -187, 0.0, 0.0], [-106, -42, 8.6, -111, 0.0, 0.0], [-116, -44, 8.3, -20, 0.0, 0.0])
    MelodyLand_drop_points = (
     [
      86, 44, -13.5, 121.1, 0.0, 0.0], [88, -16, -13.5, 91.3, 0.0, 0.0], [92, -76, -13.5, 62.5, 0.0, 0.0], [53, -112, 6.5, 65.8, 0.0, 0.0], [-69, -71, 6.5, -67.2, 0.0, 0.0], [-75, 21, 6.5, -100.9, 0.0, 0.0], [-21, 72, 6.5, -129.5, 0.0, 0.0], [56, 72, 6.5, 138.2, 0.0, 0.0], [-41, 47, 6.5, -98.9, 0.0, 0.0])
    DaisyGardens_drop_points = (
     [
      0, 0, 0, -10.5, 0, 0], [76, 35, 1.1, -30.2, 0.0, 0.0], [97, 106, 0.0, 51.4, 0.0, 0.0], [51, 180, 10.0, 22.6, 0.0, 0.0], [-14, 203, 10.0, 85.6, 0.0, 0.0], [-58, 158, 10.0, -146.9, 0.0, 0.0], [-86, 128, 0.0, -178.9, 0.0, 0.0], [-64, 65, 0.0, 17.7, 0.0, 0.0], [-13, 39, 0.0, -15.7, 0.0, 0.0], [-12, 193, 0.0, -112.4, 0.0, 0.0], [87, 128, 0.0, 45.4, 0.0, 0.0])
    Dreamland_drop_points = (
     [
      77, 91, 0.0, 124.4, 0.0, 0.0], [29, 92, 0.0, -154.5, 0.0, 0.0], [-28, 49, -16.4, -142.0, 0.0, 0.0], [21, 40, -16.0, -65.1, 0.0, 0.0], [48, 27, -15.4, -161.0, 0.0, 0.0], [-2, -22, -15.2, -132.1, 0.0, 0.0], [-92, -88, 0.0, -116.3, 0.0, 0.0], [-56, -93, 0.0, -21.5, 0.0, 0.0], [20, -88, 0.0, -123.4, 0.0, 0.0], [76, -90, 0.0, 11.0, 0.0, 0.0])
    Tutorial_drop_points = [
     130.9, -8.6, -1.3, 105.5, 0, 0]
    Default_drop_point = [
     0, 0, 0, 0, 0, 0]
    dbg_drop_mode = 0
    current_drop_point = 0

    def __init__(self, tcr):
        self.tcr = tcr
        return None
        return

    def get_drop_point(self, drop_point_list):
        if self.dbg_drop_mode == 0:
            return whrandom.choice(drop_point_list)
        else:
            droppnt = self.current_drop_point % len(drop_point_list)
            self.current_drop_point = (self.current_drop_point + 1) % len(drop_point_list)
            return drop_point_list[droppnt]

    def getAvailableZones(self):
        if base.launcher == None:
            return self.getZonesInPhase(4) + self.getZonesInPhase(6) + self.getZonesInPhase(8)
        else:
            first = base.launcher.firstPhase
            final = base.launcher.finalPhase
            zones = []
            for phase in range(first, final + 1):
                if base.launcher.getPhaseComplete(phase):
                    zones = zones + self.getZonesInPhase(phase)

            return zones
        return

    def getZonesInPhase(self, phase):
        p = []
        for i in phaseMap.items():
            if i[1] == phase:
                p.append(i[0])

        return p

    def getPhaseFromHood(self, hoodId):
        return phaseMap[hoodId]

    def getPlaygroundCenterFromId(self, hoodId):
        if hoodId == DonaldsDock:
            return self.get_drop_point(self.DonaldsDock_drop_points)
        else:
            if hoodId == ToontownCentral:
                return self.get_drop_point(self.ToontownCentral_drop_points)
            else:
                if hoodId == TheBrrrgh:
                    return self.get_drop_point(self.Brggh_drop_points)
                else:
                    if hoodId == MinniesMelodyland:
                        return self.get_drop_point(self.MelodyLand_drop_points)
                    else:
                        if hoodId == DaisyGardens:
                            return self.get_drop_point(self.DaisyGardens_drop_points)
                        else:
                            if hoodId == DonaldsDreamland:
                                return self.get_drop_point(self.Dreamland_drop_points)
                            else:
                                if hoodId == Tutorial:
                                    return self.get_drop_point(self.Tutorial_drop_points)
                                else:
                                    if hoodId == ConstructionZone:
                                        return Default_drop_point
                                    else:
                                        if hoodId == FunnyFarm:
                                            return Default_drop_point
                                        else:
                                            if hoodId == GoofyStadium:
                                                return Default_drop_point
                                            else:
                                                if hoodId == BossbotHQ:
                                                    return Default_drop_point
                                                else:
                                                    if hoodId == SellbotHQ:
                                                        return Default_drop_point
                                                    else:
                                                        if hoodId == CashbotHQ:
                                                            return Default_drop_point
                                                        else:
                                                            if hoodId == LawbotHQ:
                                                                return Default_drop_point
                                                            else:
                                                                self.notify.error('getSafeZoneCenterFromId: No such hood name as: ' + str(hoodId))

    def getIdFromName(self, hoodName):
        if hoodName == 'dd':
            return DonaldsDock
        else:
            if hoodName == 'tt':
                return ToontownCentral
            else:
                if hoodName == 'br':
                    return TheBrrrgh
                else:
                    if hoodName == 'mm':
                        return MinniesMelodyland
                    else:
                        if hoodName == 'dg':
                            return DaisyGardens
                        else:
                            if hoodName == 'cz':
                                return ConstructionZone
                            else:
                                if hoodName == 'ff':
                                    return FunnyFarm
                                else:
                                    if hoodName == 'gs':
                                        return GoofyStadium
                                    else:
                                        if hoodName == 'dl':
                                            return DonaldsDreamland
                                        else:
                                            if hoodName == 'bh':
                                                return BossbotHQ
                                            else:
                                                if hoodName == 'sh':
                                                    return SellbotHQ
                                                else:
                                                    if hoodName == 'ch':
                                                        return CashbotHQ
                                                    else:
                                                        if hoodName == 'lh':
                                                            return LawbotHQ
                                                        else:
                                                            self.notify.error('No such hood name as: ' + hoodName)
                                                            return None
        return None
        return

    def getNameFromId(self, hoodId):
        if hoodId == DonaldsDock:
            return 'dd'
        else:
            if hoodId == ToontownCentral:
                return 'tt'
            else:
                if hoodId == Tutorial:
                    return 'tt'
                else:
                    if hoodId == TheBrrrgh:
                        return 'br'
                    else:
                        if hoodId == MinniesMelodyland:
                            return 'mm'
                        else:
                            if hoodId == DaisyGardens:
                                return 'dg'
                            else:
                                if hoodId == ConstructionZone:
                                    return 'cz'
                                else:
                                    if hoodId == FunnyFarm:
                                        return 'ff'
                                    else:
                                        if hoodId == GoofyStadium:
                                            return 'gs'
                                        else:
                                            if hoodId == DonaldsDreamland:
                                                return 'dl'
                                            else:
                                                if hoodId == BossbotHQ:
                                                    return 'bh'
                                                else:
                                                    if hoodId == SellbotHQ:
                                                        return 'sh'
                                                    else:
                                                        if hoodId == CashbotHQ:
                                                            return 'ch'
                                                        else:
                                                            if hoodId == LawbotHQ:
                                                                return 'lh'
                                                            else:
                                                                self.notify.error('No such hood id as: ' + str(hoodId))
                                                                return None
        return

    def getFullnameFromId(self, hoodId):
        return hoodNameMap[hoodId][1]

    def addLinkTunnelHooks(self, hoodPart, nodeList):
        tunnelOriginList = []
        for i in nodeList:
            linkTunnelNPC = i.findAllMatches('**/linktunnel*')
            for p in range(linkTunnelNPC.getNumPaths()):
                linkTunnel = linkTunnelNPC.getPath(p)
                name = linkTunnel.getName()
                hoodStr = name[11:13]
                zoneStr = name[14:18]
                hoodId = self.getIdFromName(hoodStr)
                zoneId = int(zoneStr)
                linkSphere = linkTunnel.find('**/tunnel_trigger')
                if not linkSphere.isEmpty():
                    linkSphere.node().setName('tunnel_trigger_' + hoodStr + '_' + zoneStr)
                else:
                    linkSphere = linkTunnel.find('**/tunnel_trigger_' + hoodStr + '_' + zoneStr)
                    if linkSphere.isEmpty():
                        self.notify.error('tunnel_trigger not found')
                tunnelOrigin = linkTunnel.find('**/tunnel_origin')
                if tunnelOrigin.isEmpty():
                    self.notify.error('tunnel_origin not found')
                tunnelOriginPlaceHolder = render.attachNewNode('toph_' + hoodStr + '_' + zoneStr)
                tunnelOriginList.append(tunnelOriginPlaceHolder)
                tunnelOriginPlaceHolder.setPos(tunnelOrigin.getPos(render))
                tunnelOriginPlaceHolder.setHpr(tunnelOrigin.getHpr(render))
                hood = toonbase.localToon.cr.playGame.hood
                if ZoneUtil.tutorialDict:
                    how = 'teleportIn'
                    tutorialFlag = 1
                else:
                    how = 'tunnelIn'
                    tutorialFlag = 0
                hoodPart.accept('enter' + linkSphere.getName(), hoodPart.handleEnterTunnel, [{'loader': ZoneUtil.getLoaderName(zoneId), 'where': ZoneUtil.getToonWhereName(zoneId), 'how': how, 'hoodId': hoodId, 'zoneId': zoneId, 'shardId': None, 'tunnelOrigin': tunnelOriginPlaceHolder, 'tutorial': tutorialFlag}])

        return tunnelOriginList
        return

    def extractGroupName(self, groupFullName):
        return string.split(groupFullName, ':', 1)[0]

    def makeLinkTunnelName(self, hoodId, currentZone):
        return '**/toph_' + self.getNameFromId(hoodId) + '_' + str(currentZone)