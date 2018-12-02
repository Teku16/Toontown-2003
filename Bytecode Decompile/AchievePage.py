import ShtikerPage
from DirectGui import *
import Localizer

class AchievePage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(parent=self, relief=None, text=Localizer.AchievePageTitle, text_scale=0.12, pos=(0, 0, 0.6))
        return

    def unload(self):
        del self.title
        ShtikerPage.ShtikerPage.unload(self)