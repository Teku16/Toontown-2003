from PandaModules import *
import Localizer
ENDLESS_GAME = config.GetBool('endless-ring-game', 0)
NUM_RING_GROUPS = 16
MAX_TOONXZ = 10.0
RING_RADIUS = MAX_TOONXZ / 3.0 * 0.9
ringColors = (
 (
  Localizer.ColorRed, VBase4(1.0, 0.4, 0.2, 1.0)), (Localizer.ColorGreen, VBase4(0.0, 0.9, 0.2, 1.0)), (Localizer.ColorOrange, VBase4(1.0, 0.5, 0.25, 1.0)), (Localizer.ColorPurple, VBase4(1.0, 0.0, 1.0, 1.0)), (Localizer.ColorWhite, VBase4(1.0, 1.0, 1.0, 1.0)), (Localizer.ColorBlack, VBase4(0.0, 0.0, 0.0, 1.0)), (Localizer.ColorYellow, VBase4(1.0, 1.0, 0.2, 1.0)))
ringColorSelection = [
 (
  0, 1, 2), 3, 4, 5, 6]