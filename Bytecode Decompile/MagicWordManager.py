from ShowBaseGlobal import *
import DistributedObject, DistributedToon, DirectNotifyGlobal, TownBattleAttackPanel, RoguesGallery, Avatar, ChatManager, ToontownGlobals, string, Toon

class MagicWordManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManager')
    wantMagicWords = base.config.GetBool('want-magic-words', 0)
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.rogues = None
        self.dbg_running_fast = 0
        self.shownFontNode = None
        self.collisionVisualizer = None
        self.cameraCollisionVisualizer = None
        return None
        return

    def generate(self):
        self.accept('magicWord', self.b_setMagicWord)
        if base.config.GetBool('want-chat', 0):
            self.d_setMagicWord('~chat', toonbase.localToon.doId, 0)
        return None
        return

    def disable(self):
        self.ignore('magicWord')
        if self.dbg_running_fast:
            self.toggleRun()
        self.hidefont()
        return None
        return

    def setMagicWord(self, word, avId, zoneId):
        try:
            self.doMagicWord(word, avId, zoneId)
        except:
            self.notify.warning('Ignoring error in magic word.')
            exception = sys.exc_info()[0]
            extraInfo = sys.exc_info()[1]
            if extraInfo:
                response = str(extraInfo)
            else:
                response = str(exception)
            self.setMagicWordResponse(response)

    def doMagicWord(self, word, avId, zoneId):
        print word
        if word == '~endgame':
            print 'Requesting minigame abort...'
            messenger.send('minigameAbort')
        else:
            if word == '~wingame':
                print 'Requesting minigame victory...'
                messenger.send('minigameVictory')
            else:
                if word == '~oobe':
                    base.oobe()
                else:
                    if word == '~tex':
                        base.toggleTexture()
                    else:
                        if word == '~wire':
                            base.toggleWireframe()
                        else:
                            if word[:9] == '~showfont':
                                self.showfont(word[9:])
                            else:
                                if word == '~hidefont':
                                    self.hidefont()
                                else:
                                    if word == '~walk':
                                        try:
                                            fsm = toonbase.tcr.playGame.getPlace().fsm
                                            fsm.request('walk')
                                            if fsm.getCurrentState().getName() != 'walk':
                                                fsm.request('final')
                                                fsm.request('start')
                                                fsm.request('walk')
                                        except:
                                            pass

                                    else:
                                        if word[:7] == '~rogues':
                                            suitname = None
                                            if len(word) > 7:
                                                suitname = word[7:].split(' ')[1]
                                            self.rogues = RoguesGallery.RoguesGallery(suitname)
                                            self.rogues.enter()
                                            if suitname != None:
                                                self.rogues.animate()
                                            self.acceptOnce('mouse1', self.exit_rogues)
                                        else:
                                            if word[:7] == '~showCS' or word[:7] == '~showcs':
                                                bitmask = self.getCSBitmask(word[7:])
                                                render.showCS(bitmask)
                                            else:
                                                if word[:7] == '~hideCS' or word[:7] == '~hidecs':
                                                    bitmask = self.getCSBitmask(word[7:])
                                                    render.hideCS(bitmask)
                                                else:
                                                    if word == '~showCollisions':
                                                        self.showCollisions()
                                                    else:
                                                        if word == '~hideCollisions':
                                                            self.hideCollisions()
                                                        else:
                                                            if word == '~showCameraCollisions':
                                                                self.showCameraCollisions()
                                                            else:
                                                                if word == '~hideCameraCollisions':
                                                                    self.hideCameraCollisions()
                                                                else:
                                                                    if word == '~listen':
                                                                        toonbase.localToon.garbleChat = 0
                                                                    else:
                                                                        if word == '~nochat' or word == '~chat' or word == '~superchat':
                                                                            toonbase.localToon.garbleChat = 1
                                                                        else:
                                                                            if word[:7] == '~stress':
                                                                                factor = word[7:]
                                                                                if factor:
                                                                                    factor = float(factor)
                                                                                    LOD.setStressFactor(factor)
                                                                                    response = 'Set LOD stress factor to %s' % factor
                                                                                else:
                                                                                    factor = LOD.getStressFactor()
                                                                                    response = 'LOD stress factor is %s' % factor
                                                                                self.setMagicWordResponse(response)
                                                                            else:
                                                                                if word[:5] == '~for ':
                                                                                    self.forAnother(word, avId, zoneId)
                                                                                else:
                                                                                    if word[:11] == '~photoshoot':
                                                                                        toonbase.tcr.playGame.hood.sky.hide()
                                                                                        toonbase.tcr.playGame.getPlace().loader.geom.hide()
                                                                                        base.win.setClearColor(VBase4(1, 1, 1, 1))
                                                                                        toonbase.localToon.stopLookAroundNow()
                                                                                        toonbase.localToon.stopBlink()
                                                                                        toonbase.localToon.setNameVisible(0)
                                                                                    else:
                                                                                        if word[:9] == '~badname ':
                                                                                            word = '~for %s ~badname' % word[9:]
                                                                                            print 'word is %s' % word
                                                                                            self.forAnother(word, avId, zoneId)
                                                                                        else:
                                                                                            if word[:6] == '~doId ':
                                                                                                name = string.strip(word[6:])
                                                                                                objs = self.identifyDistributedObjects(name)
                                                                                                if len(objs) == 0:
                                                                                                    response = '%s is unknown.' % name
                                                                                                else:
                                                                                                    response = ''
                                                                                                    for name, obj in objs:
                                                                                                        response += '\n%s %d' % (name, obj.doId)

                                                                                                    response = response[1:]
                                                                                                self.setMagicWordResponse(response)
                                                                                            else:
                                                                                                if word == '~hideAttack':
                                                                                                    TownBattleAttackPanel.hideAttackPanel(1)
                                                                                                else:
                                                                                                    if word == '~showAttack':
                                                                                                        TownBattleAttackPanel.hideAttackPanel(0)
                                                                                                    else:
                                                                                                        if word == '~collisions_on':
                                                                                                            toonbase.localToon.collisionsOn()
                                                                                                        else:
                                                                                                            if word == '~collisions_off':
                                                                                                                toonbase.localToon.collisionsOff()
                                                                                                            else:
                                                                                                                if word == '~battle_detect_off':
                                                                                                                    import DistributedSuit
                                                                                                                    DistributedSuit.ALLOW_BATTLE_DETECT = 0
                                                                                                                else:
                                                                                                                    if word == '~battle_detect_on':
                                                                                                                        import DistributedSuit
                                                                                                                        DistributedSuit.ALLOW_BATTLE_DETECT = 1
                                                                                                                    else:
                                                                                                                        if word == '~addCameraPosition':
                                                                                                                            toonbase.localToon.addCameraPosition()
                                                                                                                        else:
                                                                                                                            if word == '~removeCameraPosition':
                                                                                                                                toonbase.localToon.removeCameraPosition()
                                                                                                                            else:
                                                                                                                                if word == '~printCameraPosition':
                                                                                                                                    toonbase.localToon.printCameraPosition(toonbase.localToon.cameraIndex)
                                                                                                                                else:
                                                                                                                                    if word == '~printCameraPositions':
                                                                                                                                        toonbase.localToon.printCameraPositions()
                                                                                                                                    else:
                                                                                                                                        if word == '~magic':
                                                                                                                                            MagicWordManager.wantMagicWords = 1
                                                                                                                                            if toonbase.localToon.chatMgr.fsm.getCurrentState().getName() == 'mainMenu':
                                                                                                                                                toonbase.localToon.chatMgr.fsm.request('mainMenu')
                                                                                                                                        else:
                                                                                                                                            if word == '~exec':
                                                                                                                                                ChatManager.ChatManager.execChat = 1
                                                                                                                                            else:
                                                                                                                                                if word == '~run':
                                                                                                                                                    self.toggleRun()
                                                                                                                                                else:
                                                                                                                                                    if word == '~who':
                                                                                                                                                        avIds = []
                                                                                                                                                        for av in Avatar.Avatar.ActiveAvatars:
                                                                                                                                                            if isinstance(av, DistributedToon.DistributedToon):
                                                                                                                                                                avIds.append(av.doId)

                                                                                                                                                        self.d_setWho(avIds)
                                                                                                                                                    else:
                                                                                                                                                        if word[:7] == '~period':
                                                                                                                                                            timeout = string.strip(word[7:])
                                                                                                                                                            if timeout != '':
                                                                                                                                                                seconds = int(timeout)
                                                                                                                                                                toonbase.tcr.stopPeriodTimer()
                                                                                                                                                                toonbase.tcr.resetPeriodTimer(seconds)
                                                                                                                                                                toonbase.tcr.startPeriodTimer()
                                                                                                                                                            if toonbase.tcr.periodTimerExpired:
                                                                                                                                                                response = 'Period timer has expired.'
                                                                                                                                                            else:
                                                                                                                                                                if toonbase.tcr.periodTimerStarted:
                                                                                                                                                                    elapsed = globalClock.getFrameTime() - toonbase.tcr.periodTimerStarted
                                                                                                                                                                    secondsRemaining = toonbase.tcr.periodTimerSecondsRemaining - elapsed
                                                                                                                                                                    response = 'Period timer expires in %s seconds.' % int(secondsRemaining)
                                                                                                                                                                else:
                                                                                                                                                                    response = 'Period timer not set.'
                                                                                                                                                            self.setMagicWordResponse(response)
                                                                                                                                                        else:
                                                                                                                                                            if word == '~direct':
                                                                                                                                                                taskMgr.removeTasksMatching('updateSmartCamera*')
                                                                                                                                                                camera.wrtReparentTo(render)
                                                                                                                                                                base.startTk()
                                                                                                                                                                base.startDirect()
                                                                                                                                                            else:
                                                                                                                                                                if word == '~tt':
                                                                                                                                                                    if direct:
                                                                                                                                                                        direct.disable()
                                                                                                                                                                        camera.wrtReparentTo(toonbase.localToon)
                                                                                                                                                                        toonbase.localToon.startUpdateSmartCamera()
                                                                                                                                                                else:
                                                                                                                                                                    if word == '~cogPageFull':
                                                                                                                                                                        toonbase.localToon.suitPage.updateAllCogs(3)
        return None
        return

    def toggleRun(self):
        if self.dbg_running_fast:
            self.dbg_running_fast = 0
            ToontownGlobals.ToonForwardSpeed = self.save_fwdspeed
            ToontownGlobals.ToonReverseSpeed = self.save_revspeed
            ToontownGlobals.ToonRotateSpeed = self.save_rotspeed
            toonbase.localToon.setWalkSpeedNormal()
        else:
            self.dbg_running_fast = 1
            self.save_fwdspeed = ToontownGlobals.ToonForwardSpeed
            self.save_revspeed = ToontownGlobals.ToonReverseSpeed
            self.save_rotspeed = ToontownGlobals.ToonRotateSpeed
            ToontownGlobals.ToonForwardSpeed = 60
            ToontownGlobals.ToonReverseSpeed = 30
            ToontownGlobals.ToonRotateSpeed = 100
            toonbase.localToon.setWalkSpeedNormal()

    def d_setMagicWord(self, magicWord, avId, zoneId):
        self.sendUpdate('setMagicWord', [magicWord, avId, zoneId])
        return None
        return

    def b_setMagicWord(self, magicWord, avId=None, zoneId=None):
        if self.wantMagicWords:
            if avId == None:
                avId = toonbase.localToon.doId
            if zoneId == None:
                try:
                    zoneId = toonbase.tcr.playGame.getPlace().getZoneId()
                except:
                    pass
                else:
                    if zoneId == None:
                        zoneId = 0

            self.d_setMagicWord(magicWord, avId, zoneId)
            self.setMagicWord(magicWord, avId, zoneId)
        return None
        return

    def setMagicWordResponse(self, response):
        toonbase.localToon.setChatAbsolute(response, CFSpeech | CFTimeout)

    def d_setWho(self, avIds):
        self.sendUpdate('setWho', [avIds])
        return None
        return

    def exit_rogues(self):
        self.rogues.exit()
        del self.rogues
        self.rogues = None
        return

    def forAnother(self, word, avId, zoneId):
        b = 5
        while word[b:b + 2] != ' ~':
            b += 1
            if b >= len(word):
                self.setMagicWordResponse('No next magic word!')
                return

        nextWord = word[b + 1:]
        name = string.strip(word[5:b])
        id = self.identifyAvatar(name)
        if id == None:
            self.setMagicWordResponse("Don't know who %s is." % name)
            return
        self.d_setMagicWord(nextWord, id, zoneId)
        return

    def identifyAvatar(self, name):
        for av in Avatar.Avatar.ActiveAvatars:
            if isinstance(av, DistributedToon.DistributedToon) and av.getName() == name:
                return av.doId

        lowerName = string.lower(name)
        for av in Avatar.Avatar.ActiveAvatars:
            if isinstance(av, DistributedToon.DistributedToon) and string.strip(string.lower(av.getName())) == lowerName:
                return av.doId

        try:
            avId = int(name)
            return avId
        except:
            pass

        return None
        return

    def identifyDistributedObjects(self, name):
        result = []
        lowerName = string.lower(name)
        for obj in toonbase.tcr.doId2do.values():
            className = obj.__class__.__name__
            try:
                name = obj.getName()
            except:
                name = className
            else:
                if string.lower(name) == lowerName or string.lower(className) == lowerName or string.lower(className) == 'distributed' + lowerName:
                    result.append((name, obj))

        return result

    def getCSBitmask(self, str):
        words = string.lower(str).split()
        if len(words) == 0:
            return None
        invalid = ''
        bitmask = BitMask32.allOff()
        for w in words:
            if w == 'wall':
                bitmask |= ToontownGlobals.WallBitmask
            else:
                if w == 'floor':
                    bitmask |= ToontownGlobals.FloorBitmask
                else:
                    if w == 'cam':
                        bitmask |= ToontownGlobals.CameraBitmask
                    else:
                        invalid += ' ' + w

        if invalid:
            self.setMagicWordResponse('Unknown CS keyword(s): %s' % invalid)
        return bitmask
        return

    def showfont(self, fontname):
        fontname = string.strip(string.lower(fontname))
        if fontname == '' or fontname == 'interface':
            font = ToontownGlobals.getInterfaceFont()
        else:
            if fontname == 'toon':
                font = ToontownGlobals.getToonFont()
            else:
                if fontname == 'suit':
                    font = ToontownGlobals.getSuitFont()
                else:
                    if fontname == 'sign':
                        font = ToontownGlobals.getSignFont()
                    else:
                        self.setMagicWordResponse('Unknown font: %s' % fontname)
                        return
        if not isinstance(font, DynamicTextFont):
            self.setMagicWordResponse('Font %s is not dynamic.' % fontname)
            return
        self.hidefont()
        self.shownFontNode = aspect2d.attachNewNode('shownFont')
        tn = TextNode('square')
        tn.freeze()
        tn.setCardActual(0.0, 1.0, -1.0, 0.0)
        tn.setFrameActual(0.0, 1.0, -1.0, 0.0)
        tn.setCardColor(1, 1, 1, 0.5)
        tn.setFrameColor(1, 1, 1, 1)
        tn.setFont(font)
        tn.setText(' ')
        numXPages = 2
        numYPages = 2
        pageScale = 0.8
        pageMargin = 0.1
        numPages = font.getNumPages()
        x = 0
        y = 0
        for pi in range(numPages):
            page = font.getPage(pi)
            tn.setCardTexture(page)
            np = self.shownFontNode.attachNewNode(tn.generate())
            np.setScale(pageScale)
            (
             np.setPos(float(x) / numXPages * 2 - 1 + pageMargin, 0, 1 - float(y) / numYPages * 2 - pageMargin),)
            x += 1
            if x >= numXPages:
                y += 1

    def hidefont(self):
        if self.shownFontNode != None:
            self.shownFontNode.removeNode()
            self.shownFontNode = None
        return

    def showCollisions(self):
        if self.collisionVisualizer == None:
            try:
                self.collisionVisualizer = CollisionVisualizer('showCollisions')
            except:
                self.setMagicWordResponse('CollisionVisualizer is not compiled in.')
                return
            else:
                self.collisionVisualizerNP = render.attachNewNode(self.collisionVisualizer)
                base.cTrav.setRecorder(self.collisionVisualizer.upcastToCollisionRecorder())
        return

    def hideCollisions(self):
        if self.collisionVisualizer != None:
            base.cTrav.clearRecorder()
            self.collisionVisualizerNP.removeNode()
            self.collisionVisualizer = None
        return

    def showCameraCollisions(self):
        if self.cameraCollisionVisualizer == None:
            try:
                self.cameraCollisionVisualizer = CollisionVisualizer('showCameraCollisions')
            except:
                self.setMagicWordResponse('CollisionVisualizer is not compiled in.')
                return
            else:
                self.cameraCollisionVisualizerNP = render.attachNewNode(self.cameraCollisionVisualizer)
                toonbase.localToon.ccTrav.setRecorder(self.cameraCollisionVisualizer.upcastToCollisionRecorder())
        return

    def hideCameraCollisions(self):
        if self.cameraCollisionVisualizer != None:
            toonbase.localToon.ccTrav.clearRecorder()
            self.cameraCollisionVisualizerNP.removeNode()
            self.cameraCollisionVisualizer = None
        return