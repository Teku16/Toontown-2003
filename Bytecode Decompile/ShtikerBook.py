from ShowBaseGlobal import *
import ToontownGlobals, PandaObject, StateData
from DirectGui import *

class ShtikerBook(DirectFrame, StateData.StateData):
    __module__ = __name__

    def __init__(self, doneEvent):
        DirectFrame.__init__(self, relief=None, sortOrder=BACKGROUND_SORT_INDEX)
        self.initialiseoptions(ShtikerBook)
        StateData.StateData.__init__(self, doneEvent)
        self.pages = []
        self.currPageIndex = None
        self.hide()
        self.entered = 0
        self.safeMode = 0
        self.__obscured = 0
        self.setPos(0, 0, 0.1)
        return

    def setSafeMode(self, setting):
        self.safeMode = setting

    def enter(self):
        if self.entered:
            return
        self.entered = 1
        base.playSfx(self.openSound)
        base.disableMouse()
        base.render.hide()
        base.setBackgroundColor(0.05, 0.15, 0.4)
        self.oldMin2dAlpha = NametagGlobals.getMin2dAlpha()
        self.oldMax2dAlpha = NametagGlobals.getMax2dAlpha()
        NametagGlobals.setMin2dAlpha(0.8)
        NametagGlobals.setMax2dAlpha(1.0)
        self.bookOpenButton.hide()
        self.bookCloseButton.show()
        self.show()
        self.showPageArrows()
        if not self.safeMode:
            self.accept('shtiker-page-done', self.__pageDone)
            self.accept(ToontownGlobals.StickerBookHotkey, self.__close)
            self.accept('arrow_right', self.__pageChange, [1])
            self.accept('arrow_left', self.__pageChange, [-1])
        self.pages[self.currPageIndex].enter()

    def exit(self):
        if not self.entered:
            return
        self.entered = 0
        base.playSfx(self.closeSound)
        self.pages[self.currPageIndex].exit()
        base.render.show()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        gsg = base.win.getGsg()
        if gsg:
            base.render.prepareScene(gsg)
        NametagGlobals.setMin2dAlpha(self.oldMin2dAlpha)
        NametagGlobals.setMax2dAlpha(self.oldMax2dAlpha)
        self.hide()
        self.hideButton()
        cleanupDialog('globalDialog')
        self.ignore('shtiker-page-done')
        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore('arrow_right')
        self.ignore('arrow_left')

    def load(self):
        bookModel = loader.loadModelOnce('phase_3.5/models/gui/stickerbook_gui')
        self['image'] = bookModel.find('**/big_book')
        self['image_scale'] = (2, 1, 1.5)
        self.resetFrameSize()
        self.bookOpenButton = DirectButton(image=(bookModel.find('**/BookIcon_CLSD'), bookModel.find('**/BookIcon_OPEN'), bookModel.find('**/BookIcon_RLVR')), relief=None, pos=(1.175, 0, -0.83), scale=0.305, command=self.__open)
        self.bookCloseButton = DirectButton(image=(bookModel.find('**/BookIcon_OPEN'), bookModel.find('**/BookIcon_CLSD'), bookModel.find('**/BookIcon_RLVR2')), relief=None, pos=(1.175, 0, -0.83), scale=0.305, command=self.__close)
        self.bookOpenButton.hide()
        self.bookCloseButton.hide()
        self.nextArrow = DirectButton(parent=self, relief=None, image=(bookModel.find('**/arrow_button'), bookModel.find('**/arrow_down'), bookModel.find('**/arrow_rollover')), scale=(0.1, 0.1, 0.1), pos=(0.838, 0, -0.661), command=self.__pageChange, extraArgs=[1])
        self.prevArrow = DirectButton(parent=self, relief=None, image=(bookModel.find('**/arrow_button'), bookModel.find('**/arrow_down'), bookModel.find('**/arrow_rollover')), scale=(-0.1, 0.1, 0.1), pos=(-0.838, 0, -0.661), command=self.__pageChange, extraArgs=[-1])
        bookModel.removeNode()
        self.openSound = base.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_open.mp3')
        self.closeSound = base.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_delete.mp3')
        self.pageSound = base.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_turn.mp3')
        return

    def unload(self):
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        self.destroy()
        self.bookOpenButton.destroy()
        del self.bookOpenButton
        self.bookCloseButton.destroy()
        del self.bookCloseButton
        del self.nextArrow
        del self.prevArrow
        for page in self.pages:
            page.unload()

        del self.pages
        del self.openSound
        del self.closeSound
        del self.pageSound
        return

    def addPage(self, page):
        self.pages.append(page)
        page.setBook(self)
        page.reparentTo(self)
        return None
        return

    def setPage(self, page):
        if self.currPageIndex is not None:
            self.pages[self.currPageIndex].exit()
        self.currPageIndex = self.pages.index(page)
        self.showPageArrows()
        page.enter()
        return

    def obscureButton(self, obscured):
        self.__obscured = obscured
        if self.__obscured:
            self.hideButton()

    def isObscured(self):
        return self.__obscured

    def showButton(self):
        if self.__obscured:
            return 0
        else:
            self.bookOpenButton.show()
            self.bookCloseButton.hide()
            return 1

    def hideButton(self):
        self.bookOpenButton.hide()
        self.bookCloseButton.hide()

    def __open(self):
        messenger.send('enterStickerBook')

    def __close(self):
        base.playSfx(self.closeSound)
        self.pages[self.currPageIndex].exit()
        self.doneStatus = {'mode': 'close'}
        messenger.send('exitStickerBook')
        messenger.send(self.doneEvent)

    def __pageDone(self):
        page = self.pages[self.currPageIndex]
        pageDoneStatus = page.getDoneStatus()
        if pageDoneStatus['mode'] == 'close':
            self.__close()
        else:
            self.doneStatus = pageDoneStatus
            messenger.send(self.doneEvent)

    def __pageChange(self, offset):
        messenger.send('wakeup')
        base.playSfx(self.pageSound)
        self.pages[self.currPageIndex].exit()
        self.currPageIndex = self.currPageIndex + offset
        messenger.send('stickerBookPageChange-' + str(self.currPageIndex))
        self.currPageIndex = max(self.currPageIndex, 0)
        self.currPageIndex = min(self.currPageIndex, len(self.pages) - 1)
        self.showPageArrows()
        self.pages[self.currPageIndex].enter()

    def showPageArrows(self):
        if self.currPageIndex == 0:
            self.prevArrow.hide()
            self.nextArrow.show()
        else:
            if self.currPageIndex == len(self.pages) - 1:
                self.prevArrow.show()
                self.nextArrow.hide()
            else:
                self.prevArrow.show()
                self.nextArrow.show()