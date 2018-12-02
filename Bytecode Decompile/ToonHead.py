import Actor, Task, FSM, State, string, whrandom
from ShowBaseGlobal import *
HeadDict = {'dls': '/models/char/dogMM_Shorts-head-', 'dss': '/models/char/dogMM_Skirt-head-', 'dsl': '/models/char/dogSS_Shorts-head-', 'dll': '/models/char/dogLL_Shorts-head-', 'c': '/models/char/cat-heads-', 'h': '/models/char/horse-heads-', 'm': '/models/char/mouse-heads-', 'r': '/models/char/rabbit-heads-', 'f': '/models/char/duck-heads-'}
EyelashDict = {'d': '/models/char/dog-lashes', 'c': '/models/char/cat-lashes', 'h': '/models/char/horse-lashes', 'm': '/models/char/mouse-lashes', 'r': '/models/char/rabbit-lashes', 'f': '/models/char/duck-lashes'}

class ToonHead(Actor.Actor):
    __module__ = __name__
    EyesOpen = loader.loadTexture('phase_3/maps/eyes.jpg', 'phase_3/maps/eyes_a.rgb')
    EyesOpen.setMinfilter(Texture.FTLinear)
    EyesOpen.setMagfilter(Texture.FTLinear)
    EyesClosed = loader.loadTexture('phase_3/maps/eyesClosed.jpg', 'phase_3/maps/eyesClosed_a.rgb')
    EyesClosed.setMinfilter(Texture.FTLinear)
    EyesClosed.setMagfilter(Texture.FTLinear)
    EyesSadOpen = loader.loadTexture('phase_3/maps/eyesSad.jpg', 'phase_3/maps/eyesSad_a.rgb')
    EyesSadOpen.setMinfilter(Texture.FTLinear)
    EyesSadOpen.setMagfilter(Texture.FTLinear)
    EyesSadClosed = loader.loadTexture('phase_3/maps/eyesSadClosed.jpg', 'phase_3/maps/eyesSadClosed_a.rgb')
    EyesSadClosed.setMinfilter(Texture.FTLinear)
    EyesSadClosed.setMagfilter(Texture.FTLinear)
    EyesAngryOpen = loader.loadTexture('phase_3/maps/eyesAngry.jpg', 'phase_3/maps/eyesAngry_a.rgb')
    EyesAngryOpen.setMinfilter(Texture.FTLinear)
    EyesAngryOpen.setMagfilter(Texture.FTLinear)
    EyesAngryClosed = loader.loadTexture('phase_3/maps/eyesAngryClosed.jpg', 'phase_3/maps/eyesAngryClosed_a.rgb')
    EyesAngryClosed.setMinfilter(Texture.FTLinear)
    EyesAngryClosed.setMagfilter(Texture.FTLinear)
    EyesSurprised = loader.loadTexture('phase_3/maps/eyesSurprised.jpg', 'phase_3/maps/eyesSurprised_a.rgb')
    EyesSurprised.setMinfilter(Texture.FTLinear)
    EyesSurprised.setMagfilter(Texture.FTLinear)
    Muzzle = loader.loadTexture('phase_3/maps/muzzleShrtGeneric.jpg')
    Muzzle.setMinfilter(Texture.FTLinear)
    Muzzle.setMagfilter(Texture.FTLinear)
    MuzzleSurprised = loader.loadTexture('phase_3/maps/muzzleShortSurprised.jpg')
    MuzzleSurprised.setMinfilter(Texture.FTLinear)
    MuzzleSurprised.setMagfilter(Texture.FTLinear)

    def __init__(self):
        try:
            self.ToonHead_initialized
        except:
            self.ToonHead_initialized = 1
            Actor.Actor.__init__(self)
            self.toonName = 'ToonHead-' + str(self.this)
            self.__blinkName = 'blink-' + self.toonName
            self.__stareAtName = 'stareAt-' + self.toonName
            self.__lookName = 'look-' + self.toonName
            self.__eyes = None
            self.__eyelashOpen = None
            self.__eyelashClosed = None
            self.__lod500Eyes = None
            self.__lod250Eyes = None
            self.__lpupil = None
            self.__lod500lPupil = None
            self.__lod250lPupil = None
            self.__rpupil = None
            self.__lod500rPupil = None
            self.__lod250rPupil = None
            self.__muzzle = None
            self.__eyesOpen = ToonHead.EyesOpen
            self.__eyesClosed = ToonHead.EyesClosed
            self.eyelids = FSM.FSM('eyelids', [
             State.State('off', self.enterEyelidsOff, self.exitEyelidsOff, [
              'open', 'closed', 'surprised']),
             State.State('open', self.enterEyelidsOpen, self.exitEyelidsOpen, [
              'closed', 'surprised', 'off']),
             State.State('surprised', self.enterEyelidsSurprised, self.exitEyelidsSurprised, [
              'open', 'closed', 'off']),
             State.State('closed', self.enterEyelidsClosed, self.exitEyelidsClosed, [
              'open', 'surprised', 'off'])], 'off', 'off')
            self.eyelids.enterInitialState()
            self.__stareAtNode = NodePath()
            self.__defaultStarePoint = Point3(0, 0, 0)
            self.__stareAtPoint = self.__defaultStarePoint
            self.__stareAtTime = 0
            self.lookAtPositionCallbackArgs = None

        return None
        return

    def delete(self):
        try:
            self.ToonHead_deleted
        except:
            self.ToonHead_deleted = 1
            taskMgr.remove(self.__blinkName)
            del self.eyelids
            del self.__stareAtNode
            del self.__stareAtPoint
            if self.__eyes:
                del self.__eyes
            if self.__lpupil:
                del self.__lpupil
            if self.__rpupil:
                del self.__rpupil
            if self.__eyelashOpen:
                del self.__eyelashOpen
            if self.__eyelashClosed:
                del self.__eyelashClosed
            Actor.Actor.delete(self)

    def setupHead(self, dna, forGui=0):
        self.generateToonHead(1, dna, ('1000',), forGui)
        self.generateToonColor(dna)
        if forGui:
            self.getGeomNode().setDepthWrite(1)
            self.getGeomNode().setDepthTest(1)
        if dna.getAnimal() == 'dog':
            self.loop('neutral')

    def fitAndCenterHead(self, maxDim, forGui=0):
        p1 = Point3()
        p2 = Point3()
        self.calcTightBounds(p1, p2)
        if forGui:
            h = 180
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        else:
            h = 0
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = maxDim / biggest
        mid = (p1 + d / 2.0) * s
        self.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2], h, 0, 0, s, s, s)

    def setLookAtPositionCallbackArgs(self, argTuple):
        self.lookAtPositionCallbackArgs = argTuple

    def getRandomForwardLookAtPoint(self):
        x = whrandom.choice((-0.8, -0.5, 0, 0.5, 0.8))
        z = whrandom.choice((-0.5, 0, 0.5, 0.8))
        return Point3(x, 1.5, z)

    def findSomethingToLookAt(self):
        if self.lookAtPositionCallbackArgs != None:
            pnt = self.lookAtPositionCallbackArgs[0].getLookAtPosition(self.lookAtPositionCallbackArgs[1], self.lookAtPositionCallbackArgs[2])
            self.startStareAt(self, pnt)
            return
        if whrandom.random() < 0.33:
            lookAtPnt = self.getRandomForwardLookAtPoint()
        else:
            lookAtPnt = self.__defaultStarePoint
        self.lerpLookAt(lookAtPnt, blink=1)
        return

    def generateToonHead(self, copy, style, lods, forGui=0):
        headStyle = style.head
        fix = None
        if headStyle == 'dls':
            filePrefix = HeadDict['dls']
            headHeight = 0.75
        else:
            if headStyle == 'dss':
                filePrefix = HeadDict['dss']
                headHeight = 0.5
            else:
                if headStyle == 'dsl':
                    filePrefix = HeadDict['dsl']
                    headHeight = 0.5
                else:
                    if headStyle == 'dll':
                        filePrefix = HeadDict['dll']
                        headHeight = 0.75
                    else:
                        if headStyle == 'cls':
                            filePrefix = HeadDict['c']
                            fix = self.__fixHeadLongShort
                            headHeight = 0.75
                        else:
                            if headStyle == 'css':
                                filePrefix = HeadDict['c']
                                fix = self.__fixHeadShortShort
                                headHeight = 0.5
                            else:
                                if headStyle == 'csl':
                                    filePrefix = HeadDict['c']
                                    fix = self.__fixHeadShortLong
                                    headHeight = 0.5
                                else:
                                    if headStyle == 'cll':
                                        filePrefix = HeadDict['c']
                                        fix = self.__fixHeadLongLong
                                        headHeight = 0.75
                                    else:
                                        if headStyle == 'hls':
                                            filePrefix = HeadDict['h']
                                            fix = self.__fixHeadLongShort
                                            headHeight = 0.75
                                        else:
                                            if headStyle == 'hss':
                                                filePrefix = HeadDict['h']
                                                fix = self.__fixHeadShortShort
                                                headHeight = 0.5
                                            else:
                                                if headStyle == 'hsl':
                                                    filePrefix = HeadDict['h']
                                                    fix = self.__fixHeadShortLong
                                                    headHeight = 0.5
                                                else:
                                                    if headStyle == 'hll':
                                                        filePrefix = HeadDict['h']
                                                        fix = self.__fixHeadLongLong
                                                        headHeight = 0.75
                                                    else:
                                                        if headStyle == 'mls':
                                                            filePrefix = HeadDict['m']
                                                            fix = self.__fixHeadLongLong
                                                            headHeight = 0.75
                                                        else:
                                                            if headStyle == 'mss':
                                                                filePrefix = HeadDict['m']
                                                                fix = self.__fixHeadShortShort
                                                                headHeight = 0.5
                                                            else:
                                                                if headStyle == 'rls':
                                                                    filePrefix = HeadDict['r']
                                                                    fix = self.__fixHeadLongShort
                                                                    headHeight = 0.75
                                                                else:
                                                                    if headStyle == 'rss':
                                                                        filePrefix = HeadDict['r']
                                                                        fix = self.__fixHeadShortShort
                                                                        headHeight = 0.5
                                                                    else:
                                                                        if headStyle == 'rsl':
                                                                            filePrefix = HeadDict['r']
                                                                            fix = self.__fixHeadShortLong
                                                                            headHeight = 0.5
                                                                        else:
                                                                            if headStyle == 'rll':
                                                                                filePrefix = HeadDict['r']
                                                                                fix = self.__fixHeadLongLong
                                                                                headHeight = 0.75
                                                                            else:
                                                                                if headStyle == 'fls':
                                                                                    filePrefix = HeadDict['f']
                                                                                    fix = self.__fixHeadLongShort
                                                                                    headHeight = 0.75
                                                                                else:
                                                                                    if headStyle == 'fss':
                                                                                        filePrefix = HeadDict['f']
                                                                                        fix = self.__fixHeadShortShort
                                                                                        headHeight = 0.5
                                                                                    else:
                                                                                        if headStyle == 'fsl':
                                                                                            filePrefix = HeadDict['f']
                                                                                            fix = self.__fixHeadShortLong
                                                                                            headHeight = 0.5
                                                                                        else:
                                                                                            if headStyle == 'fll':
                                                                                                filePrefix = HeadDict['f']
                                                                                                fix = self.__fixHeadLongLong
                                                                                                headHeight = 0.75
                                                                                            else:
                                                                                                ToonHead.notify.error('unknown head style: %s' % headStyle)
        animalType = style.getAnimal()
        if len(lods) == 1:
            self.loadModel('phase_3' + filePrefix + lods[0], 'head', 'lodRoot', copy)
            if not copy:
                self.showAllParts('head')
            if fix != None:
                fix(style, None, copy)
        for lod in lods:
            self.loadModel('phase_3' + filePrefix + lod, 'head', lod, copy)
            if not copy:
                self.showAllParts('head', lod)
            if fix != None:
                fix(style, lod, copy)

        self.__fixEyes(style, forGui)
        self.setupEyelashes(style)
        self.eyelids.request('closed')
        self.eyelids.request('open')
        self.__muzzle = self.find('**/1000/**/muzzle')
        return headHeight
        return

    def generateToonColor(self, style):
        parts = self.findAllMatches('**/head*')
        for partNum in range(0, parts.getNumPaths()):
            parts.getPath(partNum).setColor(style.getHeadColor())

        animalType = style.getAnimal()
        if animalType == 'cat' or animalType == 'rabbit' or animalType == 'mouse':
            parts = self.findAllMatches('**/ear?-*')
            for partNum in range(0, parts.getNumPaths()):
                parts.getPath(partNum).setColor(style.getHeadColor())

    def __fixEyes(self, style, forGui=0):
        mode = -3
        if forGui:
            mode = -2
        if self.hasLOD():
            for lodName in self.getLODNames():
                headFront = self.drawInFront('eyes*', 'head-front*', mode, lodName=lodName)
                if headFront:
                    self.drawInFront('joint-pupil?', 'eyes*', mode, lodName=lodName)
                else:
                    self.drawInFront('joint-pupil?', 'eyes*', -1, lodName=lodName)

        else:
            headFront = self.drawInFront('eyes*', 'head-front*', mode)
            if headFront:
                self.drawInFront('joint-pupil?', 'eyes*', mode)
            else:
                self.drawInFront('joint-pupil?', 'eyes*', -1)
        allEyes = self.findAllMatches('**/eyes*')
        for i in range(0, allEyes.getNumPaths()):
            allEyes.getPath(i).setColorOff()

        if self.hasLOD():
            self.__eyes = self.find('**/' + self.getLODNames()[0] + '/**/eyes*')
            self.__lod500Eyes = self.find('**/' + self.getLODNames()[1] + '/**/eyes*')
            if self.__lod500Eyes.isEmpty():
                self.__lod500Eyes = None
            else:
                self.__lod500lPupil = self.__lod500Eyes.find('**/joint-pupilL')
                self.__lod500rPupil = self.__lod500Eyes.find('**/joint-pupilR')
            self.__lod250Eyes = self.find('**/' + self.getLODNames()[2] + '/**/eyes*')
            if self.__lod250Eyes.isEmpty():
                self.__lod250Eyes = None
            else:
                self.__lod250lPupil = self.__lod250Eyes.find('**/joint-pupilL')
                self.__lod250rPupil = self.__lod250Eyes.find('**/joint-pupilR')
        else:
            self.__eyes = self.find('**/eyes*')
        if not self.__eyes.isEmpty():
            self.__lpupil = None
            self.__rpupil = None
            lp = self.__eyes.find('**/joint-pupilL')
            rp = self.__eyes.find('**/joint-pupilR')
            if lp.isEmpty() or rp.isEmpty():
                print 'Unable to locate pupils.'
            else:
                leye = self.__eyes.attachNewNode('leye')
                reye = self.__eyes.attachNewNode('reye')
                lmat = Mat4(0.802174, 0.59709, 0, 0, -0.586191, 0.787531, 0.190197, 0, 0.113565, -0.152571, 0.981746, 0, -0.233634, 0.418062, 0.0196875, 1)
                leye.setMat(lmat)
                rmat = Mat4(0.786788, -0.617224, 0, 0, 0.602836, 0.768447, 0.214658, 0, -0.132492, -0.16889, 0.976689, 0, 0.233634, 0.418062, 0.0196875, 1)
                reye.setMat(rmat)
                self.__lpupil = leye.attachNewNode('lpupil')
                self.__rpupil = reye.attachNewNode('rpupil')
                lpt = self.__eyes.attachNewNode('')
                rpt = self.__eyes.attachNewNode('')
                lpt.wrtReparentTo(self.__lpupil)
                rpt.wrtReparentTo(self.__rpupil)
                lp.reparentTo(lpt)
                rp.reparentTo(rpt)
                self.__lpupil.adjustAllPriorities(1)
                self.__rpupil.adjustAllPriorities(1)
                if self.__lod500Eyes:
                    self.__lod500lPupil.adjustAllPriorities(1)
                    self.__lod500rPupil.adjustAllPriorities(1)
                if self.__lod250Eyes:
                    self.__lod250lPupil.adjustAllPriorities(1)
                    self.__lod250rPupil.adjustAllPriorities(1)
                animalType = style.getAnimal()
                if animalType != 'dog':
                    self.__lpupil.flattenStrong()
                    self.__rpupil.flattenStrong()
        return

    def __setPupilDirection(self, x, y):
        LeftA = Point3(0.06, 0.0, 0.14)
        LeftB = Point3(-0.13, 0.0, 0.1)
        LeftC = Point3(-0.05, 0.0, 0.0)
        LeftD = Point3(0.06, 0.0, 0.0)
        RightA = Point3(0.13, 0.0, 0.1)
        RightB = Point3(-0.06, 0.0, 0.14)
        RightC = Point3(-0.06, 0.0, 0.0)
        RightD = Point3(0.05, 0.0, 0.0)
        LeftAD = Point3(LeftA[0] - LeftA[2] * (LeftD[0] - LeftA[0]) / (LeftD[2] - LeftA[2]), 0.0, 0.0)
        LeftBC = Point3(LeftB[0] - LeftB[2] * (LeftC[0] - LeftB[0]) / (LeftC[2] - LeftB[2]), 0.0, 0.0)
        RightAD = Point3(RightA[0] - RightA[2] * (RightD[0] - RightA[0]) / (RightD[2] - RightA[2]), 0.0, 0.0)
        RightBC = Point3(RightB[0] - RightB[2] * (RightC[0] - RightB[0]) / (RightC[2] - RightB[2]), 0.0, 0.0)
        if y < 0.0:
            y2 = -y
            left1 = LeftAD + (LeftD - LeftAD) * y2
            left2 = LeftBC + (LeftC - LeftBC) * y2
            right1 = RightAD + (RightD - RightAD) * y2
            right2 = RightBC + (RightC - RightBC) * y2
        else:
            y2 = y
            left1 = LeftAD + (LeftA - LeftAD) * y2
            left2 = LeftBC + (LeftB - LeftBC) * y2
            right1 = RightAD + (RightA - RightAD) * y2
            right2 = RightBC + (RightB - RightBC) * y2
        left0 = Point3(0.0, 0.0, left1[2] - left1[0] * (left2[2] - left1[2]) / (left2[0] - left1[0]))
        right0 = Point3(0.0, 0.0, right1[2] - right1[0] * (right2[2] - right1[2]) / (right2[0] - right1[0]))
        if x < 0.0:
            x2 = -x
            left = left0 + (left2 - left0) * x2
            right = right0 + (right2 - right0) * x2
        else:
            x2 = x
            left = left0 + (left1 - left0) * x2
            right = right0 + (right1 - right0) * x2
        self.__lpupil.setPos(left)
        self.__rpupil.setPos(right)

    def __lookPupilsAt(self, node, point):
        if node != None:
            mat = node.getMat(self.__eyes)
            point = mat.xformPoint(point)
        distance = 1.0
        recip_z = 1.0 / max(0.1, point[1])
        x = distance * point[0] * recip_z
        y = distance * point[2] * recip_z
        x = min(max(x, -1), 1)
        y = min(max(y, -1), 1)
        self.__setPupilDirection(x, y)
        return

    def __lookHeadAt(self, node, point, frac=1.0, lod=None):
        reachedTarget = 1
        if lod == None:
            head = self.getPart('head', self.getLODNames()[0])
        else:
            head = self.getPart('head', lod)
        if node != None:
            headParent = head.getParent()
            mat = node.getMat(headParent)
            point = mat.xformPoint(point)
        rot = Mat3()
        lookAt(rot, Vec3(point), Vec3(0, 0, 1), CSDefault)
        scale = VBase3()
        hpr = VBase3()
        if decomposeMatrix(rot, scale, hpr, 0.0, CSDefault):
            hpr = VBase3(min(max(hpr[0], -60), 60), min(max(hpr[1], -20), 30), 0)
            if frac != 1:
                currentHpr = head.getHpr()
                reachedTarget = abs(hpr[0] - currentHpr[0]) < 1.0 and abs(hpr[1] - currentHpr[1]) < 1.0
                hpr = currentHpr + (hpr - currentHpr) * frac
            if lod == None:
                for lodName in self.getLODNames():
                    head = self.getPart('head', lodName)
                    head.setHpr(hpr)

            else:
                head.setHpr(hpr)
        return reachedTarget
        return

    def setupEyelashes(self, style):
        if style.getGender() == 'm':
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
                self.__eyelashOpen = None
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
                self.__eyelashClosed = None
        else:
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
            animal = style.head[0]
            model = loader.loadModelOnce('phase_3' + EyelashDict[animal])
            if self.hasLOD():
                head = self.getPart('head', '1000')
            else:
                head = self.getPart('head', 'lodRoot')
            length = style.head[1]
            if length == 'l':
                openString = 'open-long'
                closedString = 'closed-long'
            else:
                openString = 'open-short'
                closedString = 'closed-short'
            self.__eyelashOpen = model.find('**/' + openString).copyTo(head)
            self.__eyelashClosed = model.find('**/' + closedString).copyTo(head)
            model.removeNode()
        return

    def __fixHeadLongLong(self, style, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*short')
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).hide()

        return

    def __fixHeadLongShort(self, style, lodName=None, copy=1):
        animalType = style.getAnimal()
        headStyle = style.head
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        if animalType != 'fowl' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-long').removeNode()
                else:
                    searchRoot.find('**/ears-long').hide()
            else:
                if copy:
                    searchRoot.find('**/ears-short').removeNode()
                else:
                    searchRoot.find('**/ears-short').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-short').removeNode()
            else:
                searchRoot.find('**/eyes-short').hide()
        if copy:
            self.find('**/head-short').removeNode()
            self.find('**/head-front-short').removeNode()
        else:
            self.find('**/head-short').hide()
            self.find('**/head-front-short').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/muzzle-long').removeNode()
            else:
                searchRoot.find('**/muzzle-long').hide()
        else:
            if copy:
                searchRoot.find('**/muzzle-short').removeNode()
            else:
                searchRoot.find('**/muzzle-short').hide()
        return

    def __fixHeadShortLong(self, style, lodName=None, copy=1):
        animalType = style.getAnimal()
        headStyle = style.head
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        if animalType != 'fowl' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-short').removeNode()
                else:
                    searchRoot.find('**/ears-short').hide()
            else:
                if copy:
                    searchRoot.find('**/ears-long').removeNode()
                else:
                    searchRoot.find('**/ears-long').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-long').removeNode()
            else:
                searchRoot.find('**/eyes-long').hide()
        if copy:
            searchRoot.find('**/head-long').removeNode()
            searchRoot.find('**/head-front-long').removeNode()
        else:
            searchRoot.find('**/head-long').hide()
            searchRoot.find('**/head-front-long').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/muzzle-short').removeNode()
            else:
                searchRoot.find('**/muzzle-short').hide()
        else:
            if copy:
                searchRoot.find('**/muzzle-long').removeNode()
            else:
                searchRoot.find('**/muzzle-long').hide()
        return

    def __fixHeadShortShort(self, style, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*long')
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).hide()

        return

    def __blinkOpenEyes(self, task):
        self.eyelids.request('open')
        r = whrandom.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        if self.eyelids.getCurrentState().getName() != 'open':
            taskMgr.doMethodLater(4.0, self.__blinkCloseEyes, self.__blinkName)
        else:
            self.eyelids.request('closed')
            taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def startBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.__eyes:
            self.openEyes()
        taskMgr.doMethodLater(whrandom.random() * 4.0 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.__eyes:
            self.eyelids.request('open')

    def closeEyes(self):
        self.eyelids.request('closed')

    def openEyes(self):
        self.eyelids.request('open')

    def surpriseEyes(self):
        self.eyelids.request('surprised')

    def sadEyes(self):
        self.__eyesOpen = ToonHead.EyesSadOpen
        self.__eyesClosed = ToonHead.EyesSadClosed

    def angryEyes(self):
        self.__eyesOpen = ToonHead.EyesAngryOpen
        self.__eyesClosed = ToonHead.EyesAngryClosed

    def normalEyes(self):
        self.__eyesOpen = ToonHead.EyesOpen
        self.__eyesClosed = ToonHead.EyesClosed

    def blinkEyes(self):
        taskMgr.remove(self.__blinkName)
        self.eyelids.request('closed')
        taskMgr.doMethodLater(0.1, self.__blinkOpenEyes, self.__blinkName)

    def __stareAt(self, task):
        frac = 0.08
        reachedTarget = self.__lookHeadAt(self.__stareAtNode, self.__stareAtPoint, frac)
        self.__lookPupilsAt(self.__stareAtNode, self.__stareAtPoint)
        if reachedTarget and self.__stareAtNode == None:
            return Task.done
        else:
            return Task.cont
        return

    def doLookAroundToStareAt(self, node, point):
        self.startStareAt(node, point)
        self.startLookAround()

    def startStareAtHeadPoint(self, point):
        self.startStareAt(self, point)

    def startStareAt(self, node, point):
        taskMgr.remove(self.__stareAtName)
        self.__stareAtNode = node
        if point != None:
            self.__stareAtPoint = point
        else:
            self.__stareAtPoint = self.__defaultStarePoint
        self.__stareAtTime = globalClock.getFrameTime()
        taskMgr.add(self.__stareAt, self.__stareAtName)
        return

    def lerpLookAt(self, point, time=1.0, blink=0):
        taskMgr.remove(self.__stareAtName)
        lodName = self.getLODNames()[0]
        head = self.getPart('head', lodName)
        startHpr = head.getHpr()
        startLpupil = self.__lpupil.getPos()
        startRpupil = self.__rpupil.getPos()
        self.__lookHeadAt(None, point, lod=lodName)
        self.__lookPupilsAt(None, point)
        endHpr = head.getHpr()
        endLpupil = self.__lpupil.getPos() * 0.5
        endRpupil = self.__rpupil.getPos() * 0.5
        head.setHpr(startHpr)
        self.__lpupil.setPos(startLpupil)
        self.__rpupil.setPos(startRpupil)
        if startHpr.almostEqual(endHpr, 10):
            return 0
        if blink:
            self.blinkEyes()
        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            head.lerpHpr(endHpr, time, blendType='easeInOut', task=self.__stareAtName)

        lookToTgt_TimeFraction = 0.2
        lookToTgtTime = time * lookToTgt_TimeFraction
        returnToEyeCenterTime = time - lookToTgtTime - 0.5
        origin = Point3(0, 0, 0)
        blend_type = 'easeOut'
        lPupilSeq = Task.sequence(self.__lpupil.lerpPos(endLpupil, lookToTgtTime, blendType=blend_type), Task.pause(0.5), self.__lpupil.lerpPos(origin, returnToEyeCenterTime, blendType=blend_type))
        rPupilSeq = Task.sequence(self.__rpupil.lerpPos(endRpupil, lookToTgtTime, blendType=blend_type), Task.pause(0.5), self.__rpupil.lerpPos(origin, returnToEyeCenterTime, blendType=blend_type))
        taskMgr.add(lPupilSeq, self.__stareAtName)
        taskMgr.add(rPupilSeq, self.__stareAtName)
        return 1
        return

    def stopStareAt(self):
        self.lerpLookAt(Vec3.forward())

    def stopStareAtNow(self):
        taskMgr.remove(self.__stareAtName)
        if self.__lpupil and self.__rpupil:
            self.__setPupilDirection(0, 0)
        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            head.setHpr(0, 0, 0)

    def __lookAround(self, task):
        self.findSomethingToLookAt()
        t = whrandom.random() * 4.0 + 3.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)
        return Task.done

    def startLookAround(self):
        taskMgr.remove(self.__lookName)
        t = whrandom.random() * 5.0 + 2.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)

    def stopLookAround(self):
        taskMgr.remove(self.__lookName)
        self.stopStareAt()

    def stopLookAroundNow(self):
        taskMgr.remove(self.__lookName)
        self.stopStareAtNow()

    def enterEyelidsOff(self):
        pass

    def exitEyelidsOff(self):
        pass

    def enterEyelidsOpen(self):
        if not self.__eyes.isEmpty():
            self.__eyes.setTexture(self.__eyesOpen, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.show()
            if self.__eyelashClosed:
                self.__eyelashClosed.hide()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(self.__eyesOpen, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(self.__eyesOpen, 1)
            if self.__lpupil:
                self.__lpupil.show()
                self.__rpupil.show()
            if self.__lod500lPupil:
                self.__lod500lPupil.show()
                self.__lod500rPupil.show()
            if self.__lod250lPupil:
                self.__lod250lPupil.show()
                self.__lod250rPupil.show()

    def exitEyelidsOpen(self):
        pass

    def enterEyelidsClosed(self):
        if not self.__eyes.isEmpty() and self.__eyesClosed:
            self.__eyes.setTexture(self.__eyesClosed, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.hide()
            if self.__eyelashClosed:
                self.__eyelashClosed.show()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(self.__eyesClosed, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(self.__eyesClosed, 1)
            if self.__lpupil:
                self.__lpupil.hide()
                self.__rpupil.hide()
            if self.__lod500lPupil:
                self.__lod500lPupil.hide()
                self.__lod500rPupil.hide()
            if self.__lod250lPupil:
                self.__lod250lPupil.hide()
                self.__lod250rPupil.hide()

    def exitEyelidsClosed(self):
        pass

    def enterEyelidsSurprised(self):
        if not self.__eyes.isEmpty() and ToonHead.EyesSurprised:
            self.__eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.show()
            if self.__eyelashClosed:
                self.__eyelashClosed.hide()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__muzzle:
                self.__muzzle.setTexture(ToonHead.MuzzleSurprised, 1)
            if self.__lpupil:
                self.__lpupil.show()
                self.__rpupil.show()
            if self.__lod500lPupil:
                self.__lod500lPupil.show()
                self.__lod500rPupil.show()
            if self.__lod250lPupil:
                self.__lod250lPupil.show()
                self.__lod250rPupil.show()

    def exitEyelidsSurprised(self):
        if self.__muzzle:
            self.__muzzle.setTexture(ToonHead.Muzzle, 1)