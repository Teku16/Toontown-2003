from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectGui import *
import Localizer

class MinigamePowerMeter(DirectFrame):
    __module__ = __name__

    def __init__(self, size, label=None):
        DirectFrame.__init__(self, relief=None, state=NORMAL, image_color=GlobalDialogColor, image_scale=(0.48, 1.0, 0.7), image_pos=(0.0, 0.1, 0.0), sortOrder=BACKGROUND_SORT_INDEX)
        self['image'] = getDefaultDialogGeom()
        self.resetFrameSize()
        if label == None:
            label = Localizer.MinigamePowerMeterLabel
        self.powerText = DirectLabel(self, relief=None, text=label, text_scale=0.07, pos=(0.01, 0.0, 0.29))
        self.tooSlow = DirectLabel(parent=self, relief=None, text=Localizer.MinigamePowerMeterTooSlow, scale=0.07, pos=(-0.15, 0, 0.05), color=(0.1, 0.3, 0.6))
        self.tooFast = DirectLabel(parent=self, relief=None, text=Localizer.MinigamePowerMeterTooFast, scale=0.07, pos=(0.15, 0, 0.05), color=(0.1, 0.3, 0.6))
        self.tooSlow.hide()
        self.tooFast.hide()
        self.largeGauge = []
        self.gaugeSize = size
        self.__createSpeedGauge()
        self.show()
        return

    def cleanup(self):
        del self.powerText
        for gauge in self.largeGauge:
            if gauge:
                del gauge

        del self.largeGauge
        self.destroy()

    def __createSpeedGauge(self):
        gaugeA = DirectWaitBar(parent=self, relief=RAISED, range=self.gaugeSize, frameSize=(-0.6, 0.6, -0.2, 0.2), borderWidth=(0.02, 0.02), scale=0.35, pos=(0, 0, 0), frameColor=(0.0, 0.0, 0.0, 0.0), barColor=(0, 1, 0, 0.6), sortOrder=FOREGROUND_SORT_INDEX)
        gaugeA.setR(90)
        gaugeA['value'] = 0
        self.largeGauge.append(gaugeA)
        gaugeTargetTop = DirectWaitBar(parent=self, relief=RAISED, range=self.gaugeSize, frameSize=(-0.6, 0.6, -0.2, 0.2), borderWidth=(0.02, 0.02), scale=0.35, pos=(0, 0, 0), frameColor=(1, 1, 1, 1), barColor=(1, 0, 0, 1), sortOrder=BACKGROUND_SORT_INDEX + 1)
        gaugeTargetTop.setR(90)
        gaugeTargetTop['value'] = 1
        self.largeGauge.append(gaugeTargetTop)
        gaugeTargetBot = DirectWaitBar(parent=self, relief=RAISED, range=self.gaugeSize, frameSize=(-0.6, 0.6, -0.2, 0.2), borderWidth=(0.02, 0.02), scale=0.35, pos=(0, 0, 0), frameColor=(1, 1, 1, 0), barColor=(1, 1, 1, 1), sortOrder=BACKGROUND_SORT_INDEX + 2)
        gaugeTargetBot['value'] = 0
        gaugeTargetBot.setR(90)
        self.largeGauge.append(gaugeTargetBot)
        for gauge in self.largeGauge:
            gauge.show()

    def setPower(self, power):
        self.largeGauge[0]['value'] = power

    def setTarget(self, target):
        self.largeGauge[2]['value'] = target
        self.largeGauge[1]['value'] = target + 1

    def updateTooSlowTooFast(self):
        curSpeed = self.largeGauge[0]['value']
        target = self.largeGauge[2]['value']
        self.tooSlow.hide()
        self.tooFast.hide()
        if curSpeed < target - 2:
            self.tooSlow.show()
        else:
            if curSpeed > target + 2:
                self.tooFast.show()

    def setBarColor(self, color):
        self.largeGauge[0]['barColor'] = color