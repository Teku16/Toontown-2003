from ShowBaseGlobal import *
import ToontownDialog, Localizer, LaffMeter

class DeathForceAcknowledge:
    __module__ = __name__

    def __init__(self, doneEvent):
        self.dialog = ToontownDialog.GlobalDialog(message=Localizer.PlaygroundDeathAckMessage, doneEvent=doneEvent, style=ToontownDialog.Acknowledge, fadeScreen=1.0)
        self.dialog['text_pos'] = (
         -0.26, 0.1)
        scale = self.dialog.component('image0').getScale()
        scale.setX(scale[0] * 1.3)
        self.dialog.component('image0').setScale(scale)
        av = toonbase.localToon
        self.laffMeter = LaffMeter.LaffMeter(av.style, av.hp, av.maxHp)
        self.laffMeter.reparentTo(self.dialog)
        self.laffMeter.setPos(-0.48, 0, -0.035)
        self.laffMeter.setScale(0.1)
        self.laffMeter.start()
        self.dialog.show()

    def cleanup(self):
        if self.laffMeter:
            self.laffMeter.destroy()
            del self.laffMeter
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        return