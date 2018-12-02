import ShtikerPage
from DirectGui import *
import ToontownGlobals, Localizer, AvatarDNA, Suit, SuitBattleGlobals
from CogPageGlobals import *
SCALE_FACTOR = 1.5
RADAR_DELAY = 0.2
BUILDING_RADAR_POS = (
 0.375, 0.065, -0.225, -0.5)
PANEL_COLORS = (
 Vec4(0.8, 0.78, 0.77, 1), Vec4(0.75, 0.78, 0.8, 1), Vec4(0.75, 0.82, 0.79, 1), Vec4(0.825, 0.76, 0.77, 1))
PANEL_COLORS_COMPLETE1 = (
 Vec4(0.7, 0.725, 0.545, 1), Vec4(0.625, 0.725, 0.65, 1), Vec4(0.6, 0.75, 0.525, 1), Vec4(0.675, 0.675, 0.55, 1))
PANEL_COLORS_COMPLETE2 = (
 Vec4(0.9, 0.725, 0.32, 1), Vec4(0.825, 0.725, 0.45, 1), Vec4(0.8, 0.75, 0.325, 1), Vec4(0.875, 0.675, 0.35, 1))
SHADOW_SCALE_POS = (
 (
  1.225, 0, 10, -0.03), (0.9, 0, 10, 0), (1.125, 0, 10, -0.015), (1.0, 0, 10, -0.02), (1.0, -0.02, 10, -0.01), (1.05, 0, 10, -0.0425), (1.0, 0, 10, -0.05), (0.9, -0.0225, 10, -0.025), (1.25, 0, 10, -0.03), (1.0, 0, 10, -0.01), (1.0, 0.005, 10, -0.01), (1.0, 0, 10, -0.01), (0.9, 0.005, 10, -0.01), (0.95, 0, 10, -0.01), (1.125, 0.005, 10, -0.035), (0.85, -0.005, 10, -0.035), (1.2, 0, 10, -0.01), (1.05, 0, 10, 0), (1.1, 0, 10, -0.04), (1.0, 0, 10, 0), (0.95, 0.0175, 10, -0.015), (1.0, 0, 10, -0.06), (0.95, 0.02, 10, -0.0175), (0.9, 0, 10, -0.03), (1.15, 0, 10, -0.01), (1.0, 0, 10, 0), (1.0, 0, 10, 0), (1.1, 0, 10, -0.04), (0.93, 0.005, 10, -0.01), (0.95, 0.005, 10, -0.01), (1.0, 0, 10, -0.02), (0.9, 0.0025, 10, -0.03))

class SuitPage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        frameModel = loader.loadModelOnce('phase_3.5/models/gui/suitpage_frame')
        frameModel.setScale(0.03375, 1, 0.045)
        frameModel.setPos(0, 10, -0.575)
        self.guiTop = NodePath('guiTop')
        self.guiTop.reparentTo(self)
        self.frameNode = NodePath('frameNode')
        self.frameNode.reparentTo(self.guiTop)
        self.panelNode = NodePath('panelNode')
        self.panelNode.reparentTo(self.guiTop)
        self.iconNode = NodePath('iconNode')
        self.iconNode.reparentTo(self.guiTop)
        self.enlargedPanelNode = NodePath('enlargedPanelNode')
        self.enlargedPanelNode.reparentTo(self.guiTop)
        frame = frameModel.find('**/frame')
        frame.wrtReparentTo(self.frameNode)
        screws = frameModel.find('**/screws')
        screws.wrtReparentTo(self.iconNode)
        icons = frameModel.find('**/icons')
        del frameModel
        self.title = DirectLabel(parent=self.iconNode, relief=None, text=Localizer.SuitPageTitle, text_scale=0.1, text_pos=(0.04, 0), textMayChange=0)
        self.radarButtons = []
        icon = icons.find('**/corp_icon')
        self.corpRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[0])
        self.radarButtons.append(self.corpRadarButton)
        icon = icons.find('**/legal_icon')
        self.legalRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[1])
        self.radarButtons.append(self.legalRadarButton)
        icon = icons.find('**/money_icon')
        self.moneyRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[2])
        self.radarButtons.append(self.moneyRadarButton)
        icon = icons.find('**/sales_icon')
        self.salesRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[3])
        self.radarButtons.append(self.salesRadarButton)
        for radarButton in self.radarButtons:
            radarButton.building = 0
            radarButton.buildingRadarLabel = None

        gui = loader.loadModelOnce('phase_3.5/models/gui/suitpage_gui')
        self.panelModel = gui.find('**/card')
        self.shadowModels = []
        for index in range(1, len(AvatarDNA.suitHeadTypes) + 1):
            self.shadowModels.append(gui.find('**/shadow' + str(index)))

        del gui
        self.makePanels()
        self.radarOn = [
         0, 0, 0, 0]
        self.guiTop.setZ(0.625)
        self.updatePage()
        return

    def unload(self):
        self.title.destroy()
        self.corpRadarButton.destroy()
        self.legalRadarButton.destroy()
        self.moneyRadarButton.destroy()
        self.salesRadarButton.destroy()
        for panel in self.panels:
            panel.destroy()

        del self.panels
        for shadow in self.shadowModels:
            shadow.removeNode()

        self.panelModel.removeNode()
        ShtikerPage.ShtikerPage.unload(self)

    def exit(self):
        taskMgr.remove('buildingListResponseTimeout-later')
        taskMgr.remove('suitListResponseTimeout-later')
        taskMgr.remove('showCogRadarLater')
        taskMgr.remove('showBuildingRadarLater')
        for index in range(0, len(self.radarOn)):
            if self.radarOn[index]:
                self.toggleRadar(index)
                self.radarButtons[index]['state'] = NORMAL

        ShtikerPage.ShtikerPage.exit(self)

    def grow(self, panel, pos):
        panel.reparentTo(self.enlargedPanelNode)
        panel.setScale(panel.getScale() * SCALE_FACTOR)

    def shrink(self, panel, pos):
        panel.setScale(panel.scale)
        panel.reparentTo(self.panelNode)

    def toggleRadar(self, deptNum):
        messenger.send('wakeup')
        if self.radarOn[deptNum]:
            self.radarOn[deptNum] = 0
        else:
            self.radarOn[deptNum] = 1
        deptSize = AvatarDNA.suitsPerDept
        panels = self.panels[deptSize * deptNum:AvatarDNA.suitsPerDept * (deptNum + 1)]
        if self.radarOn[deptNum]:
            if hasattr(toonbase.tcr, 'currSuitPlanner'):
                if toonbase.tcr.currSuitPlanner != None:
                    toonbase.tcr.currSuitPlanner.d_suitListQuery()
                    self.acceptOnce('suitListResponse', self.updateCogRadar, extraArgs=[deptNum, panels])
                    task = Task.Task(self.suitListResponseTimeout, 'suitListResponseTimeout')
                    task.deptNum = deptNum
                    task.panels = panels
                    taskMgr.doLater(1.0, task, 'suitListResponseTimeout-later')
                    if self.radarButtons[deptNum].building:
                        toonbase.tcr.currSuitPlanner.d_buildingListQuery()
                        self.acceptOnce('buildingListResponse', self.updateBuildingRadar, extraArgs=[deptNum])
                        task = Task.Task(self.buildingListResponseTimeout, 'buildingListResponseTimeout')
                        task.deptNum = deptNum
                        taskMgr.doLater(1.0, task, 'buildingListResponseTimeout-later')
                else:
                    self.updateCogRadar(deptNum, panels)
                    self.updateBuildingRadar(deptNum)
            else:
                self.updateCogRadar(deptNum, panels)
                self.updateBuildingRadar(deptNum)
            self.radarButtons[deptNum]['state'] = DISABLED
        else:
            self.updateCogRadar(deptNum, panels)
            self.updateBuildingRadar(deptNum)
        return

    def suitListResponseTimeout(self, task):
        self.updateCogRadar(task.deptNum, task.panels, 1)
        return Task.done

    def buildingListResponseTimeout(self, task):
        self.updateBuildingRadar(task.deptNum, 1)
        return Task.done

    def makePanels(self):
        self.panels = []
        xStart = -0.66
        yStart = -0.18
        xOffset = 0.199
        yOffset = 0.284
        for dept in range(0, len(AvatarDNA.suitDepts)):
            row = []
            color = PANEL_COLORS[dept]
            for type in range(0, AvatarDNA.suitsPerDept):
                panel = DirectLabel(parent=self.panelNode, pos=(xStart + type * xOffset, 0.0, yStart - dept * yOffset), relief=None, state=NORMAL, image=self.panelModel, image_scale=(1, 1, 1), image_color=color, text=Localizer.SuitPageMystery, text_scale=0.045, text_fg=(0, 0, 0, 1), text_pos=(0, 0.185, 0), text_font=ToontownGlobals.getSuitFont(), text_wordwrap=7)
                panel.bind(ENTER, self.grow, extraArgs=[panel])
                panel.bind(EXIT, self.shrink, extraArgs=[panel])
                panel.scale = 0.6
                panel.setScale(panel.scale)
                panel.quotaLabel = None
                panel.head = None
                panel.shadow = None
                panel.count = 0
                self.addCogRadarLabel(panel)
                self.panels.append(panel)

        return

    def addQuotaLabel(self, panel):
        index = self.panels.index(panel)
        count = str(toonbase.localToon.cogCounts[index])
        if toonbase.localToon.cogs[index] < COG_COMPLETE1:
            quota = str(COG_QUOTAS[0][index % AvatarDNA.suitsPerDept])
        else:
            quota = str(COG_QUOTAS[1][index % AvatarDNA.suitsPerDept])
        quotaLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DISABLED, text=count + ' of ' + quota, text_scale=0.065, text_fg=(0, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        panel.quotaLabel = quotaLabel
        return

    def addSuitHead(self, panel, suitName):
        panelIndex = self.panels.index(panel)
        shadow = panel.attachNewNode('shadow')
        shadowModel = self.shadowModels[panelIndex]
        shadowModel.copyTo(shadow)
        coords = SHADOW_SCALE_POS[panelIndex]
        shadow.setScale(coords[0])
        shadow.setPos(coords[1], coords[2], coords[3])
        panel.shadow = shadow
        suitDNA = AvatarDNA.AvatarDNA()
        suitDNA.newSuit(suitName)
        suit = Suit.Suit()
        suit.setDNA(suitDNA)
        headParts = suit.getHeadParts()
        head = panel.attachNewNode('head')
        for part in headParts:
            copyPart = part.copyTo(head)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)

        suit.delete()
        suit = None
        p1 = Point3()
        p2 = Point3()
        head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[2])
        column = panelIndex % AvatarDNA.suitsPerDept
        s = (0.2 + column / 100.0) / biggest
        pos = -0.14 + (AvatarDNA.suitsPerDept - column - 1) / 135.0
        head.setPosHprScale(0, 10.0, pos, 180, 0, 0, s, s, s)
        panel.head = head
        return

    def addCogRadarLabel(self, panel):
        cogRadarLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DISABLED, text='', text_scale=0.05, text_fg=(0, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        panel.cogRadarLabel = cogRadarLabel
        return

    def addBuildingRadarLabel(self, button):
        gui = loader.loadModelOnce('phase_3.5/models/gui/suit_detail_panel')
        zPos = BUILDING_RADAR_POS[self.radarButtons.index(button)]
        buildingRadarLabel = DirectLabel(parent=button, relief=None, pos=(0.225, 0.0, zPos), state=DISABLED, image=gui.find('**/avatar_panel'), image_hpr=(0, 0, 90), image_scale=(0.05, 1, 0.1), image_pos=(0, 0, 0.015), text='0 buildings', text_scale=0.05, text_fg=(1, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        gui.removeNode()
        button.buildingRadarLabel = buildingRadarLabel
        return

    def resetPanel(self, dept, type):
        panel = self.panels[dept * AvatarDNA.suitsPerDept + type]
        panel['text'] = Localizer.SuitPageMystery
        if panel.cogRadarLabel:
            panel.cogRadarLabel.hide()
        if panel.quotaLabel:
            panel.quotaLabel.hide()
        if panel.head:
            panel.head.hide()
        if panel.shadow:
            panel.shadow.hide()
        color = PANEL_COLORS[dept]
        panel['image_color'] = color
        for button in self.radarButtons:
            if button.buildingRadarLabel:
                button.buildingRadarLabel.hide()

    def setPanelStatus(self, panel, status):
        index = self.panels.index(panel)
        if status == COG_UNSEEN:
            panel['text'] = Localizer.SuitPageMystery
        else:
            if status == COG_BATTLED:
                suitName = AvatarDNA.suitHeadTypes[index]
                suitFullName = SuitBattleGlobals.SuitAttributes[suitName]['name']
                if suitName == 'mm':
                    suitFullName = 'Micro-\nmanager'
                else:
                    if suitName == 'b':
                        suitFullName = 'Blood-\nsucker'
                    else:
                        if suitName == 'tm':
                            suitFullName = 'Tele-\nmarketer'
                panel['text'] = suitFullName
                if panel.quotaLabel:
                    panel.quotaLabel.show()
                else:
                    self.addQuotaLabel(panel)
                if panel.head and panel.shadow:
                    panel.head.show()
                    panel.shadow.show()
                else:
                    self.addSuitHead(panel, suitName)
            else:
                if status == COG_DEFEATED:
                    count = str(toonbase.localToon.cogCounts[index])
                    if toonbase.localToon.cogs[index] < COG_COMPLETE1:
                        quota = str(COG_QUOTAS[0][index % AvatarDNA.suitsPerDept])
                    else:
                        quota = str(COG_QUOTAS[1][index % AvatarDNA.suitsPerDept])
                    panel.quotaLabel['text'] = count + ' of ' + quota
                else:
                    if status == COG_COMPLETE1:
                        panel['image_color'] = PANEL_COLORS_COMPLETE1[index / AvatarDNA.suitsPerDept]
                    else:
                        if status == COG_COMPLETE2:
                            panel['image_color'] = PANEL_COLORS_COMPLETE2[index / AvatarDNA.suitsPerDept]

    def updateAllCogs(self, status):
        for index in range(0, len(toonbase.localToon.cogs)):
            toonbase.localToon.cogs[index] = status

        self.updatePage()

    def updatePage(self):
        index = 0
        cogs = toonbase.localToon.cogs
        for dept in range(0, len(AvatarDNA.suitDepts)):
            for type in range(0, AvatarDNA.suitsPerDept):
                self.updateCogStatus(dept, type, cogs[index])
                index += 1

        self.updateCogRadarButtons(toonbase.localToon.cogRadar)
        self.updateBuildingRadarButtons(toonbase.localToon.buildingRadar)

    def updateCogStatus(self, dept, type, status):
        if dept < 0 or dept > len(AvatarDNA.suitDepts):
            print 'ucs: bad cog dept: ', dept
        else:
            if type < 0 or type > AvatarDNA.suitsPerDept:
                print 'ucs: bad cog type: ', type
            else:
                if status < COG_UNSEEN or status > COG_COMPLETE2:
                    print 'ucs: bad status: ', status
                else:
                    self.resetPanel(dept, type)
                    panel = self.panels[dept * AvatarDNA.suitsPerDept + type]
                    if status == COG_UNSEEN:
                        self.setPanelStatus(panel, COG_UNSEEN)
                    else:
                        if status == COG_BATTLED:
                            self.setPanelStatus(panel, COG_BATTLED)
                        else:
                            if status == COG_DEFEATED:
                                self.setPanelStatus(panel, COG_BATTLED)
                                self.setPanelStatus(panel, COG_DEFEATED)
                            else:
                                if status == COG_COMPLETE1:
                                    self.setPanelStatus(panel, COG_BATTLED)
                                    self.setPanelStatus(panel, COG_DEFEATED)
                                    self.setPanelStatus(panel, COG_COMPLETE1)
                                else:
                                    if status == COG_COMPLETE2:
                                        self.setPanelStatus(panel, COG_BATTLED)
                                        self.setPanelStatus(panel, COG_DEFEATED)
                                        self.setPanelStatus(panel, COG_COMPLETE2)

    def updateCogRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index]['state'] = NORMAL

    def updateCogRadar(self, deptNum, panels, timeout=0):
        taskMgr.remove('suitListResponseTimeout-later')
        if not timeout and hasattr(toonbase.tcr, 'currSuitPlanner') and toonbase.tcr.currSuitPlanner != None:
            cogList = toonbase.tcr.currSuitPlanner.suitList
        else:
            cogList = []
        for panel in panels:
            panel.count = 0

        for cog in cogList:
            self.panels[cog].count += 1

        for panel in panels:
            panel.cogRadarLabel['text'] = '%s present' % panel.count
            if self.radarOn[deptNum]:
                panel.quotaLabel.hide()

                def showLabel(task):
                    task.label.show()
                    return Task.done

                task = Task.Task(showLabel)
                task.label = panel.cogRadarLabel
                taskMgr.doLater(RADAR_DELAY * panels.index(panel), task, 'showCogRadarLater')

                def activateButton(s=self, index=deptNum):
                    self.radarButtons[index]['state'] = NORMAL
                    return Task.done

                if not self.radarButtons[deptNum].building:
                    taskMgr.doMethodLater(RADAR_DELAY * len(panels), activateButton, 'activateButtonLater')
            else:
                panel.cogRadarLabel.hide()
                panel.quotaLabel.show()

        return

    def updateBuildingRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index].building = 1

    def updateBuildingRadar(self, deptNum, timeout=0):
        taskMgr.remove('buildingListResponseTimeout-later')
        if not timeout and hasattr(toonbase.tcr, 'currSuitPlanner') and toonbase.tcr.currSuitPlanner != None:
            buildingList = toonbase.tcr.currSuitPlanner.buildingList
        else:
            buildingList = [
             0, 0, 0, 0]
        button = self.radarButtons[deptNum]
        if button.building:
            if not button.buildingRadarLabel:
                self.addBuildingRadarLabel(button)
            if self.radarOn[deptNum]:
                num = buildingList[deptNum]
                if num == 1:
                    button.buildingRadarLabel['text'] = '%s building' % num
                else:
                    button.buildingRadarLabel['text'] = '%s buildings' % num

                def showLabel(task):
                    task.button.buildingRadarLabel.show()
                    task.button['state'] = NORMAL
                    return Task.done

                task = Task.Task(showLabel)
                task.button = button
                taskMgr.doLater(RADAR_DELAY * AvatarDNA.suitsPerDept, task, 'showBuildingRadarLater')
            else:
                button.buildingRadarLabel.hide()
        return