from IntervalGlobal import *
from BattleBase import *
from BattleProps import *
import DirectNotifyGlobal, whrandom, ParticleEffect, BattleParticles, BattleProps, Localizer
notify = DirectNotifyGlobal.directNotify.newCategory('MovieUtil')
SUIT_LOSE_DURATION = 6.0
SUIT_LURE_DISTANCE = 2.6
SUIT_LURE_DOLLAR_DISTANCE = 5.1
SUIT_EXTRA_REACH_DISTANCE = 0.9
SUIT_EXTRA_RAKE_DISTANCE = 1.1
SUIT_TRAP_DISTANCE = 2.6
SUIT_TRAP_RAKE_DISTANCE = 4.5
SUIT_TRAP_MARBLES_DISTANCE = 3.7
SUIT_TRAP_TNT_DISTANCE = 5.1
PNT3_NEARZERO = Point3(0.01, 0.01, 0.01)
PNT3_ZERO = Point3(0.0, 0.0, 0.0)
PNT3_ONE = Point3(1.0, 1.0, 1.0)
largeSuits = [
 'f', 'cc', 'gh', 'tw', 'bf', 'sc', 'ds', 'hh', 'cr', 'tbc', 'bs', 'sd', 'le', 'bw', 'nc', 'mb', 'ls', 'rb', 'ms', 'tf', 'm', 'mh']
shotDirection = 'left'

def avatarDodge(leftAvatars, rightAvatars, leftData, rightData):
    if len(leftAvatars) > len(rightAvatars):
        PoLR = rightAvatars
        PoMR = leftAvatars
    else:
        PoLR = leftAvatars
        PoMR = rightAvatars
    upper = 1 + 4 * abs(len(leftAvatars) - len(rightAvatars))
    if whrandom.randint(0, upper) > 0:
        avDodgeList = PoLR
    else:
        avDodgeList = PoMR
    if avDodgeList is leftAvatars:
        data = leftData
    else:
        data = rightData
    return (
     avDodgeList, data)


def avatarHide(avatar):
    notify.debug('avatarHide(%d)' % avatar.doId)
    avatar.reparentTo(hidden)


def copyProp(prop):
    import Actor
    if isinstance(prop, Actor.Actor):
        return Actor.Actor(other=prop)
    else:
        return prop.copyTo(hidden)


def showProp(prop, hand, pos=None, hpr=None, scale=None):
    prop.reparentTo(hand)
    if pos:
        if callable(pos):
            pos = pos()
        prop.setPos(pos)
    if hpr:
        if callable(hpr):
            hpr = hpr()
        prop.setHpr(hpr)
    if scale:
        if callable(scale):
            scale = scale()
        prop.setScale(scale)


def showProps(props, hands, pos=None, hpr=None, scale=None):
    index = 0
    for prop in props:
        prop.reparentTo(hands[index])
        if pos:
            prop.setPos(pos)
        if hpr:
            prop.setHpr(hpr)
        if scale:
            prop.setScale(scale)
        index += 1


def hideProps(props):
    for prop in props:
        prop.reparentTo(hidden)


def removeProp(prop):
    import Actor
    if prop.isEmpty() == 1 or prop == None:
        notify.warning('removeProp() - empty prop!')
        return
    prop.reparentTo(hidden)
    if isinstance(prop, Actor.Actor):
        prop.cleanup()
    else:
        prop.removeNode()
    return


def removeProps(props):
    for prop in props:
        removeProp(prop)


def getActorIntervals(props, anim):
    tracks = []
    for prop in props:
        tracks.append(ActorInterval(prop, anim))

    return MultiTrack(tracks)


def getScaleIntervals(props, duration, startScale, endScale):
    tracks = []
    for prop in props:
        tracks.append(LerpScaleInterval(prop, duration, endScale, startScale=startScale))

    return MultiTrack(tracks)


def avatarFacePoint(av, other=render):
    pnt = av.getPos(other)
    pnt.setZ(pnt[2] + av.getHeight())
    return pnt


def insertDeathSuit(suit, deathSuit, battle=None, pos=None):
    avatarHide(suit)
    if deathSuit != None and not deathSuit.isEmpty():
        deathSuit.reparentTo(render)
        if battle != None and pos != None:
            deathSuit.setPos(battle, pos)
    return


def removeDeathSuit(suit, deathSuit):
    notify.debug('removeDeathSuit()')
    if not deathSuit.isEmpty():
        deathSuit.reparentTo(hidden)
        suit.cleanupLoseActor()


def createSuitDeathTrack(suit, toon, battle):
    suitIvals = []
    deathSuit = suit.getLoseActor()
    suitPos, suitHpr = battle.getActorPosHpr(suit)
    suitIvals.append(FunctionInterval(insertDeathSuit, extraArgs=[suit, deathSuit, battle, suitPos]))
    suitIvals.append(ActorInterval(deathSuit, 'lose', duration=SUIT_LOSE_DURATION))
    suitIvals.append(FunctionInterval(removeDeathSuit, name='remove-death-suit', extraArgs=[suit, deathSuit]))
    suitTrack = Track(suitIvals)
    spinningSound = base.loadSfx('phase_3.5/audio/sfx/Cog_Death.mp3')
    deathSound = base.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.mp3')
    deathSoundTrack = Track([WaitInterval(0.8), SoundInterval(spinningSound, duration=1.2, startTime=1.5, volume=0.2, node=suit), SoundInterval(spinningSound, duration=3.0, startTime=0.6, volume=0.9, node=suit), SoundInterval(deathSound, volume=0.4, node=suit)])
    BattleParticles.loadParticles()
    smallGears = BattleParticles.createParticleEffect(file='gearExplosionSmall')
    singleGear = BattleParticles.createParticleEffect('GearExplosion', numParticles=1)
    smallGearExplosion = BattleParticles.createParticleEffect('GearExplosion', numParticles=10)
    bigGearExplosion = BattleParticles.createParticleEffect('BigGearExplosion', numParticles=30)
    gearPoint = Point3(suitPos.getX(), suitPos.getY(), suitPos.getZ() + suit.height - 0.2)
    smallGears.setPos(gearPoint)
    singleGear.setPos(gearPoint)
    smallGearExplosion.setPos(gearPoint)
    bigGearExplosion.setPos(gearPoint)
    explosionIvals = []
    explosionIvals.append(WaitInterval(5.4))
    explosionIvals.extend(createKapowExplosionIvals(battle, explosionPoint=gearPoint))
    explosionTrack = Track(explosionIvals)
    gears1Track = Track([(2.1, ParticleInterval(smallGears, battle, worldRelative=0, duration=4.3))], name='gears1Track')
    gears2MTrack = MultiTrack([Track([(0.7, ParticleInterval(singleGear, battle, worldRelative=0, duration=5.7))]), Track([(5.2, ParticleInterval(smallGearExplosion, battle, worldRelative=0, duration=1.2))]), Track([(5.4, ParticleInterval(bigGearExplosion, battle, worldRelative=0, duration=1.0))]), explosionTrack], name='gears2MTrack')
    toonTracks = []
    for mtoon in battle.toons:
        toonTracks.append(Track([WaitInterval(1.0), ActorInterval(mtoon, 'duck'), ActorInterval(mtoon, 'duck', startTime=1.8), FunctionInterval(mtoon.loop, extraArgs=['neutral'])]))

    toonMTrack = MultiTrack(toonTracks)
    return MultiTrack([suitTrack, deathSoundTrack, gears1Track, gears2MTrack, toonMTrack])


def createSuitDodgeMultitrack(tDodge, suit, leftSuits, rightSuits):
    suitTracks = []
    suitDodgeList, sidestepAnim = avatarDodge(leftSuits, rightSuits, 'sidestep-left', 'sidestep-right')
    for s in suitDodgeList:
        suitTracks.append(Track([(tDodge, ActorInterval(s, sidestepAnim)), FunctionInterval(s.loop, extraArgs=['neutral'])]))

    suitTracks.append(Track([(tDodge, ActorInterval(suit, sidestepAnim)), FunctionInterval(suit.loop, extraArgs=['neutral'])]))
    suitTracks.append(Track([(tDodge, FunctionInterval(indicateMissed, extraArgs=[suit]))]))
    return MultiTrack(suitTracks)


def createToonDodgeMultitrack(tDodge, toon, leftToons, rightToons):
    toonTracks = []
    if len(leftToons) > len(rightToons):
        PoLR = rightToons
        PoMR = leftToons
    else:
        PoLR = leftToons
        PoMR = rightToons
    upper = 1 + 4 * abs(len(leftToons) - len(rightToons))
    if whrandom.randint(0, upper) > 0:
        toonDodgeList = PoLR
    else:
        toonDodgeList = PoMR
    if toonDodgeList is leftToons:
        sidestepAnim = 'sidestep-left'
        for t in toonDodgeList:
            toonTracks.append(Track([(tDodge, ActorInterval(t, sidestepAnim)), FunctionInterval(t.loop, extraArgs=['neutral'])]))

    else:
        sidestepAnim = 'sidestep-right'
    toonTracks.append(Track([(tDodge, ActorInterval(toon, sidestepAnim)), FunctionInterval(toon.loop, extraArgs=['neutral'])]))
    toonTracks.append(Track([(tDodge, FunctionInterval(indicateMissed, extraArgs=[toon]))]))
    return MultiTrack(toonTracks)


def createSuitTeaseMultiTrack(suit, delay=0.01):
    suitTrack = Track([WaitInterval(delay), ActorInterval(suit, 'victory', startTime=0.5, endTime=1.9), FunctionInterval(suit.loop, extraArgs=['neutral'])])
    missedTrack = Track([(delay + 0.2, FunctionInterval(indicateMissed, extraArgs=[suit, 0.9]))])
    return MultiTrack([suitTrack, missedTrack])


SPRAY_LEN = 1.5

def getSprayIntervals(battle, color, origin, target, dScaleUp, dHold, dScaleDown, horizScale=1.0, vertScale=1.0, parent=render):
    intervals = []
    sprayProp = globalPropPool.getProp('spray')
    sprayScale = hidden.attachNewNode('spray-parent')
    sprayRot = hidden.attachNewNode('spray-rotate')
    spray = sprayRot
    spray.setColor(color)
    if color[3] < 1.0:
        spray.setTransparency(1)

    def showSpray(sprayScale, sprayRot, sprayProp, origin, target, parent):
        if callable(origin):
            origin = origin()
        if callable(target):
            target = target()
        sprayRot.reparentTo(parent)
        sprayRot.clearMat()
        sprayScale.reparentTo(sprayRot)
        sprayScale.clearMat()
        sprayProp.reparentTo(sprayScale)
        sprayProp.clearMat()
        sprayRot.setPos(origin)
        sprayRot.lookAt(Point3(target))

    intervals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[sprayProp]))
    intervals.append(FunctionInterval(showSpray, extraArgs=[sprayScale, sprayRot, sprayProp, origin, target, parent]))

    def calcTargetScale(target=target, origin=origin, horizScale=horizScale, vertScale=vertScale):
        if callable(target):
            target = target()
        if callable(origin):
            origin = origin()
        distance = Vec3(target - origin).length()
        yScale = distance / SPRAY_LEN
        targetScale = Point3(yScale * horizScale, yScale, yScale * vertScale)
        return targetScale

    intervals.append(LerpScaleInterval(sprayScale, dScaleUp, calcTargetScale, startScale=PNT3_NEARZERO))
    intervals.append(WaitInterval(dHold))

    def prepareToShrinkSpray(spray, sprayProp, origin, target):
        if callable(target):
            target = target()
        if callable(origin):
            origin = origin()
        sprayProp.setPos(Point3(0.0, -SPRAY_LEN, 0.0))
        spray.setPos(target)

    intervals.append(FunctionInterval(prepareToShrinkSpray, extraArgs=[spray, sprayProp, origin, target]))
    intervals.append(LerpScaleInterval(sprayScale, dScaleDown, PNT3_NEARZERO))

    def hideSpray(spray, sprayScale, sprayRot, sprayProp, propPool):
        del spray
        sprayScale.reparentTo(hidden)
        sprayRot.reparentTo(hidden)
        sprayProp.reparentTo(hidden)
        removeProp(sprayProp)
        sprayRot.removeNode()
        sprayScale.removeNode()
        del sprayRot
        del sprayScale

    intervals.append(FunctionInterval(hideSpray, extraArgs=[spray, sprayScale, sprayRot, sprayProp, globalPropPool]))
    intervals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[sprayProp]))
    return intervals


T_HOLE_LEAVES_HAND = 1.708
T_TELEPORT_ANIM = 3.3
T_HOLE_CLOSES = 0.3

def getToonTeleportOutInterval(toon):
    holes = [
     toon.holeActors[0], toon.holeActors[1]]
    hole = holes[0]
    hole2 = holes[1]
    hands = toon.getRightHands()
    delay = T_HOLE_LEAVES_HAND
    dur = T_TELEPORT_ANIM
    holeIvals = []
    holeIvals.append(FunctionInterval(showProps, extraArgs=[holes, hands]))
    holeIvals.append((0.5, FunctionInterval(base.playSfx, extraArgs=[toon.getSoundTeleport()])))
    holeIvals.append((delay, FunctionInterval(hole.reparentTo, extraArgs=[toon])))
    holeIvals.append(FunctionInterval(hole2.reparentTo, extraArgs=[hidden]))
    holeAnimIvals = []
    holeAnimIvals.append(ActorInterval(hole, 'hole', duration=dur))
    holeAnimIvals.append(FunctionInterval(hideProps, extraArgs=[holes]))
    holeTrack = Track(holeIvals)
    holeAnimTrack = Track(holeAnimIvals)
    runTrack = Track([ActorInterval(toon, 'teleport', duration=dur), (T_HOLE_CLOSES, FunctionInterval(toon.reparentTo, extraArgs=[hidden]), PREVIOUS_END)])
    return MultiTrack([runTrack, holeAnimTrack, holeTrack])


def getToonTeleportInInterval(toon):
    hole = toon.holeActors[0]
    holeAnimIvals = []
    holeAnimIvals.append(FunctionInterval(toon.reparentTo, extraArgs=[hidden]))
    holeAnimIvals.append(FunctionInterval(hole.reparentTo, extraArgs=[toon]))
    pos = Point3(0, -2.4, 0)
    holeAnimIvals.append(FunctionInterval(hole.setPos, extraArgs=[toon, pos]))
    holeAnimIvals.append(ActorInterval(hole, 'hole', startTime=T_TELEPORT_ANIM, endTime=T_HOLE_LEAVES_HAND))
    holeAnimIvals.append(ActorInterval(hole, 'hole', startTime=T_HOLE_LEAVES_HAND, endTime=T_TELEPORT_ANIM))
    holeAnimIvals.append(FunctionInterval(hole.reparentTo, extraArgs=[hidden]))
    holeAnimTrack = Track(holeAnimIvals)
    delay = T_TELEPORT_ANIM - T_HOLE_LEAVES_HAND
    jumpTrack = Track([(delay, FunctionInterval(toon.reparentTo, extraArgs=[render])), ActorInterval(toon, 'jump')])
    return MultiTrack([holeAnimTrack, jumpTrack])


def getSuitRakeOffset(suit):
    suitName = suit.getStyleName()
    if suitName == 'gh':
        return 1.4
    else:
        if suitName == 'f':
            return 1.0
        else:
            if suitName == 'cc':
                return 0.7
            else:
                if suitName == 'tw':
                    return 1.3
                else:
                    if suitName == 'bf':
                        return 1.0
                    else:
                        if suitName == 'sc':
                            return 0.8
                        else:
                            if suitName == 'ym':
                                return 0.1
                            else:
                                if suitName == 'mm':
                                    return 0.05
                                else:
                                    if suitName == 'tm':
                                        return 0.07
                                    else:
                                        if suitName == 'nd':
                                            return 0.07
                                        else:
                                            if suitName == 'pp':
                                                return 0.04
                                            else:
                                                if suitName == 'bc':
                                                    return 0.36
                                                else:
                                                    if suitName == 'b':
                                                        return 0.41
                                                    else:
                                                        if suitName == 'dt':
                                                            return 0.31
                                                        else:
                                                            if suitName == 'ac':
                                                                return 0.39
                                                            else:
                                                                if suitName == 'ds':
                                                                    return 0.41
                                                                else:
                                                                    if suitName == 'hh':
                                                                        return 0.8
                                                                    else:
                                                                        if suitName == 'cr':
                                                                            return 2.1
                                                                        else:
                                                                            if suitName == 'tbc':
                                                                                return 1.4
                                                                            else:
                                                                                if suitName == 'bs':
                                                                                    return 0.4
                                                                                else:
                                                                                    if suitName == 'sd':
                                                                                        return 1.02
                                                                                    else:
                                                                                        if suitName == 'le':
                                                                                            return 1.3
                                                                                        else:
                                                                                            if suitName == 'bw':
                                                                                                return 1.4
                                                                                            else:
                                                                                                if suitName == 'nc':
                                                                                                    return 0.6
                                                                                                else:
                                                                                                    if suitName == 'mb':
                                                                                                        return 1.85
                                                                                                    else:
                                                                                                        if suitName == 'ls':
                                                                                                            return 1.4
                                                                                                        else:
                                                                                                            if suitName == 'rb':
                                                                                                                return 1.6
                                                                                                            else:
                                                                                                                if suitName == 'ms':
                                                                                                                    return 0.7
                                                                                                                else:
                                                                                                                    if suitName == 'tf':
                                                                                                                        return 0.75
                                                                                                                    else:
                                                                                                                        if suitName == 'm':
                                                                                                                            return 0.9
                                                                                                                        else:
                                                                                                                            if suitName == 'mh':
                                                                                                                                return 1.3
                                                                                                                            else:
                                                                                                                                notify.warning('getSuitRakeOffset(suit) - Unknown suit name: %s' % suitName)
                                                                                                                                return 0


def startSparksIval(tntProp):
    tip = tntProp.find('**/joint-attachEmitter')
    sparks = BattleParticles.createParticleEffect(file='tnt')
    return FunctionInterval(sparks.start, extraArgs=[tip])


def indicateMissed(actor, duration=1.1, scale=0.7):
    actor.showLaffString(Localizer.AttackMissed, duration=duration, scale=scale)


def createKapowExplosionIvals(parent, explosionPoint=None):
    explosionIvals = []
    explosion = loader.loadModel('phase_3.5/models/props/explosion.bam')
    explosion.setBillboardPointEye()
    if not explosionPoint:
        explosionPoint = Point3(0, 3.6, 2.1)
    explosionIvals.append(FunctionInterval(explosion.reparentTo, extraArgs=[parent]))
    explosionIvals.append(FunctionInterval(explosion.setPos, extraArgs=[explosionPoint]))
    explosionIvals.append(FunctionInterval(explosion.setScale, extraArgs=[0.4]))
    explosionIvals.append(WaitInterval(0.6))
    explosionIvals.append(FunctionInterval(removeProp, extraArgs=[explosion]))
    return explosionIvals


def createSuitStunInterval(suit, before, after):
    p1 = Point3(0)
    p2 = Point3(0)
    stars = globalPropPool.getProp('stun')
    stars.setColor(1, 1, 1, 1)
    stars.adjustAllPriorities(100)
    head = suit.getHeadParts()[0]
    head.calcTightBounds(p1, p2)
    return Sequence(Wait(before), Func(stars.reparentTo, head), Func(stars.setZ, max(0.0, p2[2] - 1.0)), Func(stars.loop, 'stun'), Wait(after), Func(stars.removeNode))