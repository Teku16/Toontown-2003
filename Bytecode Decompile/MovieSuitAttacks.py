from ToontownGlobals import *
from SuitBattleGlobals import *
from IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from AvatarDNA import *
from BattleBase import *
from BattleSounds import *
import MovieCamera, DirectNotifyGlobal, MovieUtil, ParticleEffect, BattleParticles, Toon, Localizer
notify = DirectNotifyGlobal.directNotify.newCategory('MovieSuitAttacks')

def __doDamage(toon, dmg, died):
    if dmg > 0 and toon.hp != None:
        if died != 0:
            hp = 0
        else:
            hp = toon.hp - dmg
        if hp > 0 or died != 0:
            notify.debug('setting toon: %s hp: %d' % (toon.getName(), hp))
            toon.setHp(hp)
        else:
            notify.warning('__doDamage() - hp: %d' % hp)
    return


def __showProp(prop, parent, pos, hpr=None, scale=None):
    prop.reparentTo(parent)
    prop.setPos(pos)
    if hpr:
        prop.setHpr(hpr)
    if scale:
        prop.setScale(scale)


def __animProp(prop, propName, propType='actor'):
    if 'actor' == propType:
        prop.play(propName)
    else:
        if 'model' == propType:
            pass
        else:
            self.notify.error('No such propType as: %s' % propType)


def __suitFacePoint(suit, zOffset=0):
    pnt = suit.getPos()
    pnt.setZ(pnt[2] + suit.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)


def __toonFacePoint(toon, zOffset=0, parent=render):
    pnt = toon.getPos(parent)
    pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)


def __toonTorsoPoint(toon, zOffset=0):
    pnt = toon.getPos()
    pnt.setZ(pnt[2] + toon.shoulderHeight - 0.2)
    return Point3(pnt)


def __toonGroundPoint(attack, toon, zOffset=0, parent=render):
    pnt = toon.getPos(parent)
    battle = attack['battle']
    pnt.setZ(battle.getZ(parent) + zOffset)
    return Point3(pnt)


def __toonGroundMissPoint(attack, prop, toon, zOffset=0):
    point = __toonMissPoint(prop, toon)
    battle = attack['battle']
    point.setZ(battle.getZ() + zOffset)
    return Point3(point)


def __toonMissPoint(prop, toon, yOffset=0, parent=None):
    if parent:
        p = __toonFacePoint(toon) - prop.getPos(parent)
    else:
        p = __toonFacePoint(toon) - prop.getPos()
    v = Vec3(p)
    baseDistance = v.length()
    v.normalize()
    if parent:
        endPos = prop.getPos(parent) + v * (baseDistance + 5 + yOffset)
    else:
        endPos = prop.getPos() + v * (baseDistance + 5 + yOffset)
    return Point3(endPos)


def __toonMissBehindPoint(toon, parent=render, offset=0):
    point = toon.getPos(parent)
    point.setY(point.getY() - 5 + offset)
    return point


def __throwBounceHitPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)


def __throwBounceMissPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)


def __throwBouncePoint(startPoint, endPoint):
    midPoint = startPoint + (endPoint - startPoint) / 2.0
    midPoint.setZ(0)
    return Point3(midPoint)


def doSuitAttack(attack):
    notify.debug('building suit attack in doSuitAttack: %s' % attack['name'])
    name = attack['id']
    if name == AUDIT:
        suitTrack = doAudit(attack)
    else:
        if name == BITE:
            suitTrack = doBite(attack)
        else:
            if name == BOUNCE_CHECK:
                suitTrack = doBounceCheck(attack)
            else:
                if name == BRAIN_STORM:
                    suitTrack = doBrainStorm(attack)
                else:
                    if name == BUZZ_WORD:
                        suitTrack = doBuzzWord(attack)
                    else:
                        if name == CALCULATE:
                            suitTrack = doCalculate(attack)
                        else:
                            if name == CANNED:
                                suitTrack = doCanned(attack)
                            else:
                                if name == CHOMP:
                                    suitTrack = doChomp(attack)
                                else:
                                    if name == CIGAR_SMOKE:
                                        suitTrack = doDefault(attack)
                                    else:
                                        if name == CLIPON_TIE:
                                            suitTrack = doClipOnTie(attack)
                                        else:
                                            if name == CRUNCH:
                                                suitTrack = doCrunch(attack)
                                            else:
                                                if name == DEMOTION:
                                                    suitTrack = doDemotion(attack)
                                                else:
                                                    if name == DOUBLE_TALK:
                                                        suitTrack = doDoubleTalk(attack)
                                                    else:
                                                        if name == DOWNSIZE:
                                                            suitTrack = doDownsize(attack)
                                                        else:
                                                            if name == EVICTION_NOTICE:
                                                                suitTrack = doEvictionNotice(attack)
                                                            else:
                                                                if name == EVIL_EYE:
                                                                    suitTrack = doEvilEye(attack)
                                                                else:
                                                                    if name == FILIBUSTER:
                                                                        suitTrack = doFilibuster(attack)
                                                                    else:
                                                                        if name == FILL_WITH_LEAD:
                                                                            suitTrack = doFillWithLead(attack)
                                                                        else:
                                                                            if name == FINGER_WAG:
                                                                                suitTrack = doFingerWag(attack)
                                                                            else:
                                                                                if name == FIRED:
                                                                                    suitTrack = doFired(attack)
                                                                                else:
                                                                                    if name == FIVE_O_CLOCK_SHADOW:
                                                                                        suitTrack = doDefault(attack)
                                                                                    else:
                                                                                        if name == FLOOD_THE_MARKET:
                                                                                            suitTrack = doDefault(attack)
                                                                                        else:
                                                                                            if name == FOUNTAIN_PEN:
                                                                                                suitTrack = doFountainPen(attack)
                                                                                            else:
                                                                                                if name == FREEZE_ASSETS:
                                                                                                    suitTrack = doFreezeAssets(attack)
                                                                                                else:
                                                                                                    if name == GAVEL:
                                                                                                        suitTrack = doDefault(attack)
                                                                                                    else:
                                                                                                        if name == GLOWER_POWER:
                                                                                                            suitTrack = doGlowerPower(attack)
                                                                                                        else:
                                                                                                            if name == GUILT_TRIP:
                                                                                                                suitTrack = doGuiltTrip(attack)
                                                                                                            else:
                                                                                                                if name == HALF_WINDSOR:
                                                                                                                    suitTrack = doHalfWindsor(attack)
                                                                                                                else:
                                                                                                                    if name == HANG_UP:
                                                                                                                        suitTrack = doHangUp(attack)
                                                                                                                    else:
                                                                                                                        if name == HEAD_SHRINK:
                                                                                                                            suitTrack = doHeadShrink(attack)
                                                                                                                        else:
                                                                                                                            if name == HOT_AIR:
                                                                                                                                suitTrack = doHotAir(attack)
                                                                                                                            else:
                                                                                                                                if name == JARGON:
                                                                                                                                    suitTrack = doJargon(attack)
                                                                                                                                else:
                                                                                                                                    if name == LEGALESE:
                                                                                                                                        suitTrack = doLegalese(attack)
                                                                                                                                    else:
                                                                                                                                        if name == LIQUIDATE:
                                                                                                                                            suitTrack = doLiquidate(attack)
                                                                                                                                        else:
                                                                                                                                            if name == MARKET_CRASH:
                                                                                                                                                suitTrack = doMarketCrash(attack)
                                                                                                                                            else:
                                                                                                                                                if name == MUMBO_JUMBO:
                                                                                                                                                    suitTrack = doMumboJumbo(attack)
                                                                                                                                                else:
                                                                                                                                                    if name == PARADIGM_SHIFT:
                                                                                                                                                        suitTrack = doParadigmShift(attack)
                                                                                                                                                    else:
                                                                                                                                                        if name == PECKING_ORDER:
                                                                                                                                                            suitTrack = doPeckingOrder(attack)
                                                                                                                                                        else:
                                                                                                                                                            if name == PICK_POCKET:
                                                                                                                                                                suitTrack = doPickPocket(attack)
                                                                                                                                                            else:
                                                                                                                                                                if name == PINK_SLIP:
                                                                                                                                                                    suitTrack = doPinkSlip(attack)
                                                                                                                                                                else:
                                                                                                                                                                    if name == PLAY_HARDBALL:
                                                                                                                                                                        suitTrack = doPlayHardball(attack)
                                                                                                                                                                    else:
                                                                                                                                                                        if name == POUND_KEY:
                                                                                                                                                                            suitTrack = doPoundKey(attack)
                                                                                                                                                                        else:
                                                                                                                                                                            if name == POWER_TIE:
                                                                                                                                                                                suitTrack = doPowerTie(attack)
                                                                                                                                                                            else:
                                                                                                                                                                                if name == POWER_TRIP:
                                                                                                                                                                                    suitTrack = doPowerTrip(attack)
                                                                                                                                                                                else:
                                                                                                                                                                                    if name == QUAKE:
                                                                                                                                                                                        suitTrack = doQuake(attack)
                                                                                                                                                                                    else:
                                                                                                                                                                                        if name == RAZZLE_DAZZLE:
                                                                                                                                                                                            suitTrack = doRazzleDazzle(attack)
                                                                                                                                                                                        else:
                                                                                                                                                                                            if name == RED_TAPE:
                                                                                                                                                                                                suitTrack = doRedTape(attack)
                                                                                                                                                                                            else:
                                                                                                                                                                                                if name == RE_ORG:
                                                                                                                                                                                                    suitTrack = doReOrg(attack)
                                                                                                                                                                                                else:
                                                                                                                                                                                                    if name == RESTRAINING_ORDER:
                                                                                                                                                                                                        suitTrack = doRestrainingOrder(attack)
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        if name == ROLODEX:
                                                                                                                                                                                                            suitTrack = doRolodex(attack)
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            if name == RUBBER_STAMP:
                                                                                                                                                                                                                suitTrack = doRubberStamp(attack)
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                if name == RUB_OUT:
                                                                                                                                                                                                                    suitTrack = doRubOut(attack)
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    if name == SACKED:
                                                                                                                                                                                                                        suitTrack = doSacked(attack)
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        if name == SANDTRAP:
                                                                                                                                                                                                                            suitTrack = doDefault(attack)
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            if name == SCHMOOZE:
                                                                                                                                                                                                                                suitTrack = doSchmooze(attack)
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                if name == SHAKE:
                                                                                                                                                                                                                                    suitTrack = doShake(attack)
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    if name == SHRED:
                                                                                                                                                                                                                                        suitTrack = doShred(attack)
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        if name == SONG_AND_DANCE:
                                                                                                                                                                                                                                            suitTrack = doDefault(attack)
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            if name == SPIN:
                                                                                                                                                                                                                                                suitTrack = doSpin(attack)
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                if name == SYNERGY:
                                                                                                                                                                                                                                                    suitTrack = doSynergy(attack)
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    if name == TABULATE:
                                                                                                                                                                                                                                                        suitTrack = doTabulate(attack)
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        if name == TEE_OFF:
                                                                                                                                                                                                                                                            suitTrack = doTeeOff(attack)
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            if name == THROW_BOOK:
                                                                                                                                                                                                                                                                suitTrack = doDefault(attack)
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                if name == TREMOR:
                                                                                                                                                                                                                                                                    suitTrack = doTremor(attack)
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    if name == WATERCOOLER:
                                                                                                                                                                                                                                                                        suitTrack = doWatercooler(attack)
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        if name == WITHDRAWAL:
                                                                                                                                                                                                                                                                            suitTrack = doWithdrawal(attack)
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            if name == WRITE_OFF:
                                                                                                                                                                                                                                                                                suitTrack = doWriteOff(attack)
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                notify.warning('unknown attack: %d substituting Finger Wag' % name)
                                                                                                                                                                                                                                                                                suitTrack = doDefault(attack)
    camTrack = MovieCamera.chooseSuitShot(attack, suitTrack.getDuration())
    battle = attack['battle']
    target = attack['target']
    groupStatus = attack['group']
    if groupStatus == ATK_TGT_SINGLE:
        toon = target['toon']
        toonHprTrack = Track([FunctionInterval(toon.headsUp, extraArgs=[battle, MovieUtil.PNT3_ZERO]), FunctionInterval(toon.loop, extraArgs=['neutral'])])
    else:
        toonTracks = []
        for t in target:
            toon = t['toon']
            toonTracks.append(Track([FunctionInterval(toon.headsUp, extraArgs=[battle, MovieUtil.PNT3_ZERO]), FunctionInterval(toon.loop, extraArgs=['neutral'])]))

        toonHprTrack = MultiTrack(toonTracks)
    suit = attack['suit']
    neutralIval = FunctionInterval(suit.loop, extraArgs=['neutral'])
    suitTrack = Track([suitTrack, neutralIval, toonHprTrack])
    suitPos = suit.getPos(battle)
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    if battle.isSuitLured(suit):
        resetTrack = getResetTrack(suit, battle)
        resetSuitTrack = Track([resetTrack, suitTrack])
        waitTrack = Track([WaitInterval(resetTrack.getDuration()), FunctionInterval(battle.unlureSuit, extraArgs=[suit])])
        resetCamTrack = Track([waitTrack, camTrack])
        return (
         resetSuitTrack, resetCamTrack)
    else:
        return (
         suitTrack, camTrack)


def getResetTrack(suit, battle):
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    moveDist = Vec3(suit.getPos(battle) - resetPos).length()
    moveDuration = 0.5
    walkTrack = Track([FunctionInterval(suit.setHpr, extraArgs=[battle, resetHpr]), ActorInterval(suit, 'walk', startTime=1, duration=moveDuration, endTime=1e-05), FunctionInterval(suit.loop, extraArgs=['neutral'])])
    moveTrack = Track([LerpPosInterval(suit, moveDuration, resetPos, other=battle)])
    return MultiTrack([walkTrack, moveTrack])


def __makeCancelledNodePath():
    tn = TextNode('CANCELLED')
    tn.setFont(getSuitFont())
    tn.setText(Localizer.MovieSuitCancelled)
    tn.setAlign(TextNode.ACenter)
    tntop = hidden.attachNewNode('CancelledTop')
    tnpath = tntop.attachNewNode(tn)
    tnpath.setPosHpr(0, 0, 0, 0, 0, 0)
    tnpath.setScale(1)
    tnpath.setColor(0.7, 0, 0, 1)
    tnpathback = tnpath.instanceUnderNode(tntop, 'backside')
    tnpathback.setPosHpr(0, 0, 0, 180, 0, 0)
    tnpath.setScale(1)
    return tntop


def doDefault(attack):
    notify.debug('building suit attack in doDefault')
    suitName = attack['suitName']
    if suitName == 'f':
        attack['id'] = POUND_KEY
        attack['name'] = 'PoundKey'
        attack['animName'] = 'phone'
        return doPoundKey(attack)
    else:
        if suitName == 'p':
            attack['id'] = FOUNTAIN_PEN
            attack['name'] = 'FountainPen'
            attack['animName'] = 'pen-squirt'
            return doFountainPen(attack)
        else:
            if suitName == 'ym':
                attack['id'] = RUBBER_STAMP
                attack['name'] = 'RubberStamp'
                attack['animName'] = 'rubber-stamp'
                return doRubberStamp(attack)
            else:
                if suitName == 'mm':
                    attack['id'] = FINGER_WAG
                    attack['name'] = 'FingerWag'
                    attack['animName'] = 'finger-wag'
                    return doFingerWag(attack)
                else:
                    if suitName == 'ds':
                        attack['id'] = DEMOTION
                        attack['name'] = 'Demotion'
                        attack['animName'] = 'magic1'
                        return doDemotion(attack)
                    else:
                        if suitName == 'hh':
                            attack['id'] = GLOWER_POWER
                            attack['name'] = 'GlowerPower'
                            attack['animName'] = 'glower'
                            return doGlowerPower(attack)
                        else:
                            if suitName == 'cr':
                                attack['id'] = PICK_POCKET
                                attack['name'] = 'PickPocket'
                                attack['animName'] = 'pickpocket'
                                return doPickPocket(attack)
                            else:
                                if suitName == 'tbc':
                                    attack['id'] = GLOWER_POWER
                                    attack['name'] = 'GlowerPower'
                                    attack['animName'] = 'glower'
                                    return doGlowerPower(attack)
                                else:
                                    if suitName == 'cc':
                                        attack['id'] = POUND_KEY
                                        attack['name'] = 'PoundKey'
                                        attack['animName'] = 'phone'
                                        return doPoundKey(attack)
                                    else:
                                        if suitName == 'tm':
                                            attack['id'] = CLIPON_TIE
                                            attack['name'] = 'ClipOnTie'
                                            attack['animName'] = 'throw-paper'
                                            return doClipOnTie(attack)
                                        else:
                                            if suitName == 'nd':
                                                attack['id'] = PICK_POCKET
                                                attack['name'] = 'PickPocket'
                                                attack['animName'] = 'pickpocket'
                                                return doPickPocket(attack)
                                            else:
                                                if suitName == 'gh':
                                                    attack['id'] = FOUNTAIN_PEN
                                                    attack['name'] = 'FountainPen'
                                                    attack['animName'] = 'pen-squirt'
                                                    return doFountainPen(attack)
                                                else:
                                                    if suitName == 'ms':
                                                        attack['id'] = BRAIN_STORM
                                                        attack['name'] = 'BrainStorm'
                                                        attack['animName'] = 'effort'
                                                        return doBrainStorm(attack)
                                                    else:
                                                        if suitName == 'tf':
                                                            attack['id'] = RED_TAPE
                                                            attack['name'] = 'RedTape'
                                                            attack['animName'] = 'throw-object'
                                                            return doRedTape(attack)
                                                        else:
                                                            if suitName == 'm':
                                                                attack['id'] = BUZZ_WORD
                                                                attack['name'] = 'BuzzWord'
                                                                attack['animName'] = 'speak'
                                                                return doBuzzWord(attack)
                                                            else:
                                                                if suitName == 'mh':
                                                                    attack['id'] = RAZZLE_DAZZLE
                                                                    attack['name'] = 'RazzleDazzle'
                                                                    attack['animName'] = 'smile'
                                                                    return doRazzleDazzle(attack)
                                                                else:
                                                                    if suitName == 'sc':
                                                                        attack['id'] = WATERCOOLER
                                                                        attack['name'] = 'Watercooler'
                                                                        attack['animName'] = 'water-cooler'
                                                                        return doWatercooler(attack)
                                                                    else:
                                                                        if suitName == 'pp':
                                                                            attack['id'] = BOUNCE_CHECK
                                                                            attack['name'] = 'BounceCheck'
                                                                            attack['animName'] = 'throw-paper'
                                                                            return doBounceCheck(attack)
                                                                        else:
                                                                            if suitName == 'tw':
                                                                                attack['id'] = GLOWER_POWER
                                                                                attack['name'] = 'GlowerPower'
                                                                                attack['animName'] = 'glower'
                                                                                return doGlowerPower(attack)
                                                                            else:
                                                                                if suitName == 'bc':
                                                                                    attack['id'] = AUDIT
                                                                                    attack['name'] = 'Audit'
                                                                                    attack['animName'] = 'phone'
                                                                                    return doAudit(attack)
                                                                                else:
                                                                                    if suitName == 'nc':
                                                                                        attack['id'] = RED_TAPE
                                                                                        attack['name'] = 'RedTape'
                                                                                        attack['animName'] = 'throw-object'
                                                                                        return doRedTape(attack)
                                                                                    else:
                                                                                        if suitName == 'mb':
                                                                                            attack['id'] = LIQUIDATE
                                                                                            attack['name'] = 'Liquidate'
                                                                                            attack['animName'] = 'magic1'
                                                                                            return doLiquidate(attack)
                                                                                        else:
                                                                                            if suitName == 'ls':
                                                                                                attack['id'] = WRITE_OFF
                                                                                                attack['name'] = 'WriteOff'
                                                                                                attack['animName'] = 'hold-pencil'
                                                                                                return doWriteOff(attack)
                                                                                            else:
                                                                                                if suitName == 'rb':
                                                                                                    attack['id'] = TEE_OFF
                                                                                                    attack['name'] = 'TeeOff'
                                                                                                    attack['animName'] = 'golf-club-swing'
                                                                                                    return doTeeOff(attack)
                                                                                                else:
                                                                                                    if suitName == 'bf':
                                                                                                        attack['id'] = RUBBER_STAMP
                                                                                                        attack['name'] = 'RubberStamp'
                                                                                                        attack['animName'] = 'rubber-stamp'
                                                                                                        return doRubberStamp(attack)
                                                                                                    else:
                                                                                                        if suitName == 'b':
                                                                                                            attack['id'] = EVICTION_NOTICE
                                                                                                            attack['name'] = 'EvictionNotice'
                                                                                                            attack['animName'] = 'throw-paper'
                                                                                                            return doEvictionNotice(attack)
                                                                                                        else:
                                                                                                            if suitName == 'dt':
                                                                                                                attack['id'] = RUBBER_STAMP
                                                                                                                attack['name'] = 'RubberStamp'
                                                                                                                attack['animName'] = 'rubber-stamp'
                                                                                                                return doRubberStamp(attack)
                                                                                                            else:
                                                                                                                if suitName == 'ac':
                                                                                                                    attack['id'] = RED_TAPE
                                                                                                                    attack['name'] = 'RedTape'
                                                                                                                    attack['animName'] = 'throw-object'
                                                                                                                    return doRedTape(attack)
                                                                                                                else:
                                                                                                                    if suitName == 'bs':
                                                                                                                        attack['id'] = FINGER_WAG
                                                                                                                        attack['name'] = 'FingerWag'
                                                                                                                        attack['animName'] = 'finger-wag'
                                                                                                                        return doFingerWag(attack)
                                                                                                                    else:
                                                                                                                        if suitName == 'sd':
                                                                                                                            attack['id'] = WRITE_OFF
                                                                                                                            attack['name'] = 'WriteOff'
                                                                                                                            attack['animName'] = 'hold-pencil'
                                                                                                                            return doWriteOff(attack)
                                                                                                                        else:
                                                                                                                            if suitName == 'le':
                                                                                                                                attack['id'] = JARGON
                                                                                                                                attack['name'] = 'Jargon'
                                                                                                                                attack['animName'] = 'speak'
                                                                                                                                return doJargon(attack)
                                                                                                                            else:
                                                                                                                                if suitName == 'bw':
                                                                                                                                    attack['id'] = FINGER_WAG
                                                                                                                                    attack['name'] = 'FingerWag'
                                                                                                                                    attack['animName'] = 'finger-wag'
                                                                                                                                    return doFingerWag(attack)
                                                                                                                                else:
                                                                                                                                    self.notify.error('doDefault() - unsupported suit type: %s' % suitName)
    return None
    return


def getSuitTrack(attack, delay=1e-06, splicedAnims=None):
    suit = attack['suit']
    battle = attack['battle']
    tauntIndex = attack['taunt']
    target = attack['target']
    toon = target['toon']
    targetPos = toon.getPos(battle)
    taunt = getAttackTaunt(attack['name'], tauntIndex)
    trapStorage = {}
    trapStorage['trap'] = None
    ivals = [
     WaitInterval(delay), FunctionInterval(suit.setChatAbsolute, extraArgs=[taunt, CFSpeech | CFTimeout])]

    def reparentTrap(suit=suit, battle=battle, trapStorage=trapStorage):
        trapProp = suit.battleTrapProp
        if trapProp != None:
            trapProp.wrtReparentTo(battle)
            trapStorage['trap'] = trapProp
        return

    ivals.append(FunctionInterval(reparentTrap))
    ivals.append(FunctionInterval(suit.headsUp, extraArgs=[battle, targetPos]))
    if splicedAnims:
        ivals.extend(getSplicedAnims(splicedAnims, actor=suit))
    else:
        ivals.append(ActorInterval(suit, attack['animName']))
    origPos, origHpr = battle.getActorPosHpr(suit)
    ivals.append(FunctionInterval(suit.setHpr, extraArgs=[battle, origHpr]))

    def returnTrapToSuit(suit=suit, trapStorage=trapStorage):
        trapProp = trapStorage['trap']
        if trapProp != None:
            trapProp.wrtReparentTo(suit)
            suit.battleTrapProp = trapProp
        return

    ivals.append(FunctionInterval(returnTrapToSuit))
    ivals.append(FunctionInterval(suit.clearChat))
    return Track(ivals)
    return


def getSuitAnimTrack(attack, delay=0):
    suit = attack['suit']
    tauntIndex = attack['taunt']
    taunt = getAttackTaunt(attack['name'], tauntIndex)
    return Track([WaitInterval(delay), FunctionInterval(suit.setChatAbsolute, extraArgs=[taunt, CFSpeech | CFTimeout]), ActorInterval(attack['suit'], attack['animName']), FunctionInterval(suit.clearChat)])


def getPartTrack(particleEffect, startDelay, durationDelay, partExtraArgs):
    particleEffect = partExtraArgs[0]
    parent = partExtraArgs[1]
    if len(partExtraArgs) > 2:
        worldRelative = partExtraArgs[2]
    else:
        worldRelative = 1
    return Track([(startDelay, ParticleInterval(particleEffect, parent, worldRelative, duration=durationDelay))])


def getToonTrack(attack, damageDelay=1e-06, damageAnimNames=None, dodgeDelay=0.0001, dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None, target=None, showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    if not target:
        target = attack['target']
    toon = target['toon']
    battle = attack['battle']
    suit = attack['suit']
    suitPos = suit.getPos(battle)
    dmg = target['hp']
    ivals = []
    ivals.append(FunctionInterval(toon.headsUp, extraArgs=[battle, suitPos]))
    if dmg > 0:
        ivals.append(getToonTakeDamageIntervals(toon, target['died'], dmg, damageDelay, damageAnimNames, splicedDamageAnims, showDamageExtraTime))
        return Track(ivals)
    else:
        ivals.extend(getToonDodgeMultiTrack(target, dodgeDelay, dodgeAnimNames, splicedDodgeAnims, showMissedExtraTime))
        animTrack = Track(ivals)
        indicatorTrack = Track([WaitInterval(dodgeDelay + showMissedExtraTime), FunctionInterval(MovieUtil.indicateMissed, extraArgs=[toon])])
        return MultiTrack([animTrack, indicatorTrack])


def getToonTracks(attack, damageDelay=1e-06, damageAnimNames=None, dodgeDelay=1e-06, dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None, showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    toonTracks = []
    targets = attack['target']
    for i in range(len(targets)):
        tgt = targets[i]
        toonTracks.append(getToonTrack(attack, damageDelay, damageAnimNames, dodgeDelay, dodgeAnimNames, splicedDamageAnims, splicedDodgeAnims, target=tgt, showDamageExtraTime=showDamageExtraTime, showMissedExtraTime=showMissedExtraTime))

    return toonTracks


def getToonDodgeMultiTrack(target, dodgeDelay, dodgeAnimNames, splicedDodgeAnims, showMissedExtraTime):
    toon = target['toon']
    toonAnims = []
    toonAnims.append(WaitInterval(dodgeDelay))
    if dodgeAnimNames:
        for d in dodgeAnimNames:
            if d == 'sidestep':
                toonAnims.append(getAllyToonsDodgeMultiTrack(target))
            else:
                toonAnims.append(ActorInterval(toon, d))

    else:
        toonAnims.extend(getSplicedAnims(splicedDodgeAnims, actor=toon))
    toonAnims.append(FunctionInterval(toon.loop, extraArgs=['neutral']))
    return toonAnims


def getAllyToonsDodgeMultiTrack(target):
    toon = target['toon']
    leftToons = target['leftToons']
    rightToons = target['rightToons']
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
        soundEffect = globalBattleSoundCache.getSound('AV_side_step.mp3')
    else:
        sidestepAnim = 'sidestep-right'
        soundEffect = globalBattleSoundCache.getSound('AV_jump_to_side.mp3')
    toonTracks = []
    for t in toonDodgeList:
        toonTracks.append(Track([ActorInterval(t, sidestepAnim), FunctionInterval(t.loop, extraArgs=['neutral'])]))

    toonTracks.append(Track([ActorInterval(toon, sidestepAnim), FunctionInterval(toon.loop, extraArgs=['neutral'])]))
    toonTracks.append(Track([WaitInterval(0.5), SoundInterval(soundEffect, node=toon)]))
    return MultiTrack(toonTracks)


def getPropTrack(prop, parent, posPoints, appearDelay, remainDelay, scaleUpPoint=Point3(1), scaleUpTime=0.5, scaleDownTime=0.5, startScale=Point3(0.01), anim=0, propName='none', animDuration=0.0, animStartTime=0.0, onlyIvals=0):
    extraArgsForShowProp = [
     prop, parent]
    extraArgsForShowProp.extend(posPoints)
    if anim == 1:
        ivals = [
         WaitInterval(appearDelay), FunctionInterval(__showProp, extraArgs=extraArgsForShowProp), LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale), ActorInterval(prop, propName, duration=animDuration, startTime=animStartTime), WaitInterval(remainDelay), FunctionInterval(MovieUtil.removeProp, extraArgs=[prop])]
    else:
        ivals = [
         WaitInterval(appearDelay), FunctionInterval(__showProp, extraArgs=extraArgsForShowProp), LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale), WaitInterval(remainDelay), LerpScaleInterval(prop, scaleDownTime, MovieUtil.PNT3_NEARZERO), FunctionInterval(MovieUtil.removeProp, extraArgs=[prop])]
    if onlyIvals == 1:
        return ivals
    else:
        return Track(ivals)


def getPropAppearIntervals(prop, parent, posPoints, appearDelay, scaleUpPoint=Point3(1), scaleUpTime=0.5, startScale=Point3(0.01), poseExtraArgs=[]):
    showPropExtraArgs = [
     prop, parent]
    showPropExtraArgs.extend(posPoints)
    propIvals = [
     WaitInterval(appearDelay), FunctionInterval(__showProp, extraArgs=showPropExtraArgs)]
    if poseExtraArgs != []:
        propIvals.append(FunctionInterval(prop.pose, extraArgs=poseExtraArgs))
    propIvals.append(LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale))
    return propIvals


def getPropThrowIntervals(attack, prop, hitPoints=[], missPoints=[], hitDuration=0.5, missDuration=0.5, hitPointNames='none', missPointNames='none', lookAt='none', groundPointOffSet=0, missScaleDown=None, parent=render):
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    battle = attack['battle']

    def getLambdas(list, prop, toon):
        for i in range(len(list)):
            if list[i] == 'face':
                list[i] = lambda toon=toon: __toonFacePoint(toon)
            else:
                if list[i] == 'miss':
                    list[i] = lambda prop=prop, toon=toon: __toonMissPoint(prop, toon)
                else:
                    if list[i] == 'bounceHit':
                        list[i] = lambda prop=prop, toon=toon: __throwBounceHitPoint(prop, toon)
                    else:
                        if list[i] == 'bounceMiss':
                            list[i] = lambda prop=prop, toon=toon: __throwBounceMissPoint(prop, toon)

        return list

    if hitPointNames != 'none':
        hitPoints = getLambdas(hitPointNames, prop, toon)
    if missPointNames != 'none':
        missPoints = getLambdas(missPointNames, prop, toon)
    propIvals = []
    propIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[prop]))
    propIvals.append(FunctionInterval(prop.wrtReparentTo, extraArgs=[parent]))
    if lookAt != 'none':
        propIvals.append(FunctionInterval(prop.lookAt, extraArgs=lookAt))
    if dmg > 0:
        for i in range(len(hitPoints)):
            pos = hitPoints[i]
            propIvals.append(LerpPosInterval(prop, hitDuration, pos=pos))

    else:
        for i in range(len(missPoints)):
            pos = missPoints[i]
            propIvals.append(LerpPosInterval(prop, missDuration, pos=pos))

        if missScaleDown:
            propIvals.append(LerpScaleInterval(prop, missScaleDown, MovieUtil.PNT3_NEARZERO))
    propIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[prop]))
    propIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[prop]))
    return propIvals


def getThrowIvals(object, target, duration=1.0, parent=render, gravity=-32.144):
    values = {}

    def calcOriginAndVelocity(object=object, target=target, values=values, duration=duration, parent=parent, gravity=gravity):
        if callable(target):
            target = target()
        object.wrtReparentTo(parent)
        values['origin'] = object.getPos(parent)
        origin = object.getPos(parent)
        values['velocity'] = (target[2] - origin[2] - 0.5 * gravity * duration * duration) / duration

    return [
     FunctionInterval(calcOriginAndVelocity), LerpFunctionInterval(throwPos, fromData=0.0, toData=1.0, duration=duration, extraArgs=[object, duration, target, values, gravity])]


def throwPos(t, object, duration, target, values, gravity=-32.144):
    origin = values['origin']
    velocity = values['velocity']
    if callable(target):
        target = target()
    x = origin[0] * (1 - t) + target[0] * t
    y = origin[1] * (1 - t) + target[1] * t
    time = t * duration
    z = origin[2] + velocity * time + 0.5 * gravity * time * time
    object.setPos(x, y, z)


def getToonTakeDamageIntervals(toon, died, dmg, delay, damageAnimNames=None, splicedDamageAnims=None, showDamageExtraTime=0.01):
    toonIvals = []
    toonIvals.append(WaitInterval(delay))
    if damageAnimNames:
        for d in damageAnimNames:
            toonIvals.append(ActorInterval(toon, d))

        indicatorTrack = Track([(delay + showDamageExtraTime, FunctionInterval(__doDamage, extraArgs=[toon, dmg, died]))])
    else:
        splicedAnims = getSplicedAnims(splicedDamageAnims, actor=toon)
        firstAnim = splicedAnims[0]
        remainingAnims = splicedAnims[1:]
        toonIvals.append(firstAnim)
        toonIvals.extend(remainingAnims)
        indicatorTrack = Track([(delay + showDamageExtraTime, FunctionInterval(__doDamage, extraArgs=[toon, dmg, died]))])
    if died != 0:
        loseIval = ActorInterval(toon, 'lose')
        delay = loseIval.getDuration() * 0.8
        shrinkDur = loseIval.getDuration() * 0.2
        soundTrack = getSoundTrack('ENC_Lose.mp3', delay=0.9, node=toon)
        toonIvals.append(MultiTrack([Track([loseIval]),
         Track([
          (delay,
           LerpScaleInterval(toon, shrinkDur, MovieUtil.PNT3_NEARZERO))]), soundTrack]))
        toonIvals.append(FunctionInterval(toon.reparentTo, extraArgs=[hidden]))
        toonIvals.append(FunctionInterval(toon.setScale, extraArgs=[MovieUtil.PNT3_ONE]))
    else:
        toonIvals.append(FunctionInterval(toon.loop, extraArgs=['neutral']))
    return MultiTrack([Track(toonIvals), indicatorTrack])


def getSplicedAnims(anims, actor=None):
    ivals = []
    for nextAnim in anims:
        delay = 1e-06
        if len(nextAnim) >= 2:
            if nextAnim[1] > 0:
                delay = nextAnim[1]
        if len(nextAnim) <= 0:
            ivals.append(WaitInterval(delay))
        else:
            if len(nextAnim) == 1:
                ivals.append(ActorInterval(actor, nextAnim[0]))
            else:
                if len(nextAnim) == 2:
                    ivals.append(WaitInterval(delay))
                    ivals.append(ActorInterval(actor, nextAnim[0]))
                else:
                    if len(nextAnim) == 3:
                        ivals.append(WaitInterval(delay))
                        ivals.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2]))
                    else:
                        if len(nextAnim) == 4:
                            ivals.append(WaitInterval(delay))
                            duration = nextAnim[3]
                            if duration < 0:
                                startTime = nextAnim[2]
                                endTime = startTime + duration
                                if endTime <= 0:
                                    endTime = 0.01
                                ivals.append(ActorInterval(actor, nextAnim[0], startTime=startTime, endTime=endTime))
                            else:
                                ivals.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2], duration=duration))
                        else:
                            if len(nextAnim) == 5:
                                ivals.append(WaitInterval(delay))
                                ivals.append(ActorInterval(nextAnim[4], nextAnim[0], startTime=nextAnim[2], duration=nextAnim[3]))

    return ivals


def getSplicedLerpAnims(animName, origDuration, newDuration, startTime=0, fps=30, reverse=0):
    ivals = []
    addition = 0
    numIvals = origDuration * fps
    timeInterval = newDuration / numIvals
    animInterval = origDuration / numIvals
    if reverse == 1:
        animInterval = -animInterval
    for i in range(0, numIvals):
        ivals.append([animName, timeInterval, startTime + addition, animInterval])
        addition += animInterval

    return ivals


def getSoundTrack(fileName, delay=0.01, duration=None, node=None):
    soundEffect = globalBattleSoundCache.getSound(fileName)
    if duration:
        return Track([(delay, SoundInterval(soundEffect, duration=duration, node=node))])
    else:
        return Track([(delay, SoundInterval(soundEffect, node=node))])


def doClipOnTie(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('clip-on-tie')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    else:
        if suitType == 'b':
            throwDelay = 2.17
            damageDelay = 3.3
            dodgeDelay = 3.1
        else:
            if suitType == 'c':
                throwDelay = 1.45
                damageDelay = 2.61
                dodgeDelay = 2.34
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.66, 0.51, 0.28), Point3(-26.56, 68.2, -98.13)]
    tiePropIvals = getPropAppearIntervals(tie, suit.getRightHand(), posPoints, 0.5, MovieUtil.PNT3_ONE, scaleUpTime=0.5, poseExtraArgs=['clip-on-tie', 0])
    if dmg > 0:
        tiePropIvals.append(ActorInterval(tie, 'clip-on-tie', duration=throwDelay, startTime=1.1))
    else:
        tiePropIvals.append(WaitInterval(throwDelay))
    tiePropIvals.append(FunctionInterval(tie.setHpr, extraArgs=[Point3(0, -90, 0)]))
    tiePropIvals.extend(getPropThrowIntervals(attack, tie, [__toonFacePoint(toon)], [
     __toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4, missDuration=0.8, missScaleDown=1.2))
    tiePropTrack = Track(tiePropIvals)
    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    throwSound = getSoundTrack('SA_powertie_throw.mp3', delay=throwDelay + 1, node=suit)
    return MultiTrack([suitTrack, toonTrack, tiePropTrack, throwSound])


def doPoundKey(attack):
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('PoundKey')
    BattleParticles.setEffectTexture(particleEffect, 'poundsign', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.55, [particleEffect, suit, 0])
    phonePosPoints = [Point3(0.23, 0.17, -0.11), Point3(-6.05, -2.51, 177.58)]
    receiverPosPoints = [Point3(0.23, 0.17, -0.11), Point3(-6.05, -2.51, 177.58)]
    propTrack = Track([WaitInterval(0.3), FunctionInterval(__showProp, extraArgs=[phone, suit.getLeftHand(), phonePosPoints[0], phonePosPoints[1]]), FunctionInterval(__showProp, extraArgs=[receiver, suit.getLeftHand(), receiverPosPoints[0], receiverPosPoints[1]]), LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_ONE, MovieUtil.PNT3_NEARZERO), WaitInterval(0.74), FunctionInterval(receiver.wrtReparentTo, extraArgs=[suit.getRightHand()]), LerpPosHprInterval(receiver, 0.0001, Point3(-0.45, 0.48, -0.62), Point3(-82.57, 71.11, -89.48)), WaitInterval(3.14), FunctionInterval(receiver.wrtReparentTo, extraArgs=[phone]), WaitInterval(0.62), LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO), FunctionInterval(MovieUtil.removeProps, extraArgs=[[receiver, phone]])])
    toonTrack = getToonTrack(attack, 2.7, ['cringe'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_hangup.mp3', delay=1.3, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, partTrack, soundTrack])


def doShred(attack):
    suit = attack['suit']
    battle = attack['battle']
    paper = globalPropPool.getProp('shredder-paper')
    shredder = globalPropPool.getProp('shredder')
    particleEffect = BattleParticles.createParticleEffect('Shred')
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 3.5, 1.9, [particleEffect, suit, 0])
    paperPosPoints = [Point3(0.59, -0.31, 0.81), Point3(-79.51, -30.07, 177.45)]
    paperPropTrack = getPropTrack(paper, suit.getRightHand(), paperPosPoints, 2.4, 1e-05, scaleUpTime=0.2, anim=1, propName='shredder-paper', animDuration=1.5, animStartTime=2.8)
    shredderPosPoints = [
     Point3(0, -0.12, -0.34), Point3(-90.0, -48.44, -5.33)]
    shredderPropTrack = getPropTrack(shredder, suit.getLeftHand(), shredderPosPoints, 1, 3, scaleUpPoint=Point3(4.81, 4.81, 4.81))
    toonTrack = getToonTrack(attack, suitTrack.getDuration() - 1.1, ['conked'], suitTrack.getDuration() - 3.1, ['sidestep'])
    soundTrack = getSoundTrack('SA_shred.mp3', delay=3.4, node=suit)
    return MultiTrack([suitTrack, paperPropTrack, shredderPropTrack, partTrack, toonTrack, soundTrack])


def doFillWithLead(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pencil = globalPropPool.getProp('pencil')
    sharpener = globalPropPool.getProp('sharpener')
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='fillWithLeadSpray')
    headSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    torsoSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    legsSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    BattleParticles.setEffectTexture(sprayEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(headSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(torsoSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(legsSmotherEffect, 'roll-o-dex', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 2.5, 1.9, [sprayEffect, suit, 0])
    pencilPosPoints = [Point3(-0.29, -0.33, -0.13), Point3(-158.75, 7.71, -168.69)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, 0.7, 3.2, scaleUpTime=0.2)
    sharpenerPosPoints = [Point3(0.0, 0.0, -0.03), MovieUtil.PNT3_ZERO]
    sharpenerPropTrack = getPropTrack(sharpener, suit.getLeftHand(), sharpenerPosPoints, 1.3, 2.3, scaleUpPoint=MovieUtil.PNT3_ONE)
    damageAnims = []
    damageAnims.append(['conked', suitTrack.getDuration() - 1.5, 1e-05, 1.4])
    damageAnims.append(['conked', 1e-05, 0.7, 0.7])
    damageAnims.append(['conked', 1e-05, 0.7, 0.7])
    damageAnims.append(['conked', 1e-05, 1.4])
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=suitTrack.getDuration() - 3.1, dodgeAnimNames=['sidestep'], showDamageExtraTime=4.5, showMissedExtraTime=1.6)
    animal = toon.style.getAnimal()
    bodyScale = Toon.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = Toon.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = Toon.torsoHeightDict[toon.style.torso] * bodyScale / 2 + legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headSmotherEffect.getX()
    effectY = headSmotherEffect.getY()
    headSmotherEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoSmotherEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsSmotherEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 3.5
    partIvalDelay = 0.7
    partDuration = 1.0
    headTrack = getPartTrack(headSmotherEffect, partDelay, partDuration, [
     headSmotherEffect, toon, 0])
    torsoTrack = getPartTrack(torsoSmotherEffect, partDelay + partIvalDelay, partDuration, [
     torsoSmotherEffect, toon, 0])
    legsTrack = getPartTrack(legsSmotherEffect, partDelay + partIvalDelay * 2, partDuration, [
     legsSmotherEffect, toon, 0])

    def colorParts(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.setColorScale, extraArgs=[Vec4(0, 0, 0, 1)]))

        return ivals

    def resetParts(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.clearColorScale))

        return ivals

    if dmg > 0:
        colorIvals = []
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()
        colorIvals.append(WaitInterval(partDelay + 0.2))
        colorIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        colorIvals.extend(colorParts(headParts))
        colorIvals.append(WaitInterval(partIvalDelay))
        colorIvals.extend(colorParts(torsoParts))
        colorIvals.append(WaitInterval(partIvalDelay))
        colorIvals.extend(colorParts(legsParts))
        colorIvals.append(WaitInterval(2.5))
        colorIvals.extend(resetParts(headParts))
        colorIvals.extend(resetParts(torsoParts))
        colorIvals.extend(resetParts(legsParts))
        colorIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        colorTrack = Track(colorIvals)
        return MultiTrack([suitTrack, pencilPropTrack, sharpenerPropTrack, sprayTrack, headTrack, torsoTrack, legsTrack, colorTrack, toonTrack])
    else:
        return MultiTrack([suitTrack, pencilPropTrack, sharpenerPropTrack, sprayTrack, toonTrack])


def doFountainPen(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pen = globalPropPool.getProp('pen')

    def getPenTip(pen=pen):
        tip = pen.find('**/joint-toSpray')
        return tip.getPos(render)

    hitPoint = lambda toon=toon: __toonFacePoint(toon)
    missPoint = lambda prop=pen, toon=toon: __toonMissPoint(prop, toon, 0, parent=render)
    hitSprayIvals = MovieUtil.getSprayIntervals(battle, VBase4(0, 0, 0, 1), getPenTip, hitPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
    missSprayIvals = MovieUtil.getSprayIntervals(battle, VBase4(0, 0, 0, 1), getPenTip, missPoint, 0.2, 0.2, 0.2, horizScale=0.1, vertScale=0.1)
    suitTrack = getSuitTrack(attack)
    propIvals = [WaitInterval(0.01), FunctionInterval(__showProp, extraArgs=[pen, suit.getRightHand(), MovieUtil.PNT3_ZERO]), LerpScaleInterval(pen, 0.5, Point3(1.5, 1.5, 1.5)), WaitInterval(1.05)]
    if dmg > 0:
        propIvals += hitSprayIvals
    else:
        propIvals += missSprayIvals
    propIvals += [LerpScaleInterval(pen, 0.5, MovieUtil.PNT3_NEARZERO), FunctionInterval(MovieUtil.removeProp, extraArgs=[pen])]
    propTrack = Track(propIvals)
    splashTrack = []
    if dmg > 0:

        def prepSplash(splash, targetPoint):
            splash.reparentTo(render)
            splash.setPos(targetPoint)
            scale = splash.getScale()
            splash.setBillboardPointWorld()
            splash.setScale(scale)

        splash = globalPropPool.getProp('splash-from-splat')
        splash.setColor(0, 0, 0, 1)
        splash.setScale(0.15)
        splashIvals = [FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[splash]), (1.65, FunctionInterval(prepSplash, extraArgs=[splash, __toonFacePoint(toon)])), ActorInterval(splash, 'splash-from-splat'), FunctionInterval(MovieUtil.removeProp, extraArgs=[splash]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[splash])]
        headParts = toon.getHeadParts()
        splashIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        for partNum in range(0, headParts.getNumPaths()):
            nextPart = headParts.getPath(partNum)
            splashIvals.append(FunctionInterval(nextPart.setColorScale, extraArgs=[Vec4(0, 0, 0, 1)]))

        splashIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[splash]))
        splashIvals.append(WaitInterval(2.6))
        for partNum in range(0, headParts.getNumPaths()):
            nextPart = headParts.getPath(partNum)
            splashIvals.append(FunctionInterval(nextPart.clearColorScale))

        splashIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        splashTrack.append(Track(splashIvals))
    penSpill = BattleParticles.createParticleEffect(file='penSpill')
    penSpill.setPos(getPenTip())
    penSpillTrack = getPartTrack(penSpill, 1.4, 0.7, [penSpill, pen, 0])
    toonTrack = getToonTrack(attack, 1.81, ['conked'], dodgeDelay=0.11, splicedDodgeAnims=[['duck', 0.01, 0.6]], showMissedExtraTime=1.66)
    soundTrack = getSoundTrack('SA_fountain_pen.mp3', delay=1.6, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack, penSpillTrack] + splashTrack)


def doRubOut(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    headEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getHeadColor())
    torsoEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getArmColor())
    legsEffect = BattleParticles.createParticleEffect('RubOut', color=toon.style.getLegColor())
    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.66, 0.81, -0.06), Point3(-14.93, 2.29, 180.0)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.5, 2.57)
    pencilPosPoints = [Point3(0.04, -0.38, -0.1), Point3(-172.25, 7.06, -63.73)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, 0.5, 2.57)
    toonTrack = getToonTrack(attack, 2.2, ['conked'], 2.0, ['jump'])
    hideIvals = []
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()
    animal = toon.style.getAnimal()
    bodyScale = Toon.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = Toon.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = Toon.torsoHeightDict[toon.style.torso] * bodyScale / 2 + legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headEffect.getX()
    effectY = headEffect.getY()
    headEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 2.5
    headTrack = getPartTrack(headEffect, partDelay + 0, 0.5, [headEffect, toon, 0])
    torsoTrack = getPartTrack(torsoEffect, partDelay + 1.1, 0.5, [torsoEffect, toon, 0])
    legsTrack = getPartTrack(legsEffect, partDelay + 2.2, 0.5, [legsEffect, toon, 0])

    def hideParts(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.setTransparency, extraArgs=[1]))
            ivals.append(LerpFunctionInterval(nextPart.setAlphaScale, fromData=1, toData=0, duration=0.2))

        return ivals

    def showParts(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.clearColorScale))
            ivals.append(FunctionInterval(nextPart.clearTransparency))

        return ivals

    soundTrack = getSoundTrack('SA_rubout.mp3', delay=1.7, node=suit)
    if dmg > 0:
        hideIvals.append(WaitInterval(2.2))
        hideIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        hideIvals.extend(hideParts(headParts))
        hideIvals.append(WaitInterval(0.4))
        hideIvals.extend(hideParts(torsoParts))
        hideIvals.append(WaitInterval(0.4))
        hideIvals.extend(hideParts(legsParts))
        hideIvals.append(WaitInterval(1))
        hideIvals.extend(showParts(headParts))
        hideIvals.extend(showParts(torsoParts))
        hideIvals.extend(showParts(legsParts))
        hideIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        hideTrack = Track(hideIvals)
        return MultiTrack([suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack, hideTrack, headTrack, torsoTrack, legsTrack])
    else:
        return MultiTrack([suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack])


def doFingerWag(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('FingerWag')
    BattleParticles.setEffectTexture(particleEffect, 'blah', color=Vec4(0.55, 0, 0.55, 1))
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 1.3
        damageDelay = 2.7
        dodgeDelay = 1.7
    else:
        if suitType == 'b':
            partDelay = 1.3
            damageDelay = 2.7
            dodgeDelay = 1.8
        else:
            if suitType == 'c':
                partDelay = 1.3
                damageDelay = 2.7
                dodgeDelay = 2.0
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay, 2, [particleEffect, suit, 0])
    suitName = attack['suitName']
    if suitName == 'mm':
        particleEffect.setPos(0.167, 1.5, 2.731)
    else:
        if suitName == 'tw':
            particleEffect.setPos(0.167, 1.8, 5)
            particleEffect.setHpr(90.0, -120, -0.019)
        else:
            if suitName == 'pp':
                particleEffect.setPos(0.167, 1, 4.1)
            else:
                if suitName == 'bs':
                    particleEffect.setPos(0.167, 1, 5.1)
                else:
                    if suitName == 'bw':
                        particleEffect.setPos(0.167, 1.9, suit.getHeight() - 1.8)
                        particleEffect.setP(-110)
    toonTrack = getToonTrack(attack, damageDelay, ['slip-backward'], dodgeDelay, ['sidestep'])
    soundTrack = getSoundTrack('SA_finger_wag.mp3', delay=1.3, node=suit)
    return MultiTrack([suitTrack, toonTrack, partTrack, soundTrack])


def doWriteOff(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    BattleParticles.loadParticles()
    checkmark = MovieUtil.copyProp(BattleParticles.getParticle('checkmark'))
    checkmark.setBillboardPointEye()
    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.25, 1.38, -0.08), Point3(19.83, 3.64, 171.12)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.5, 2.57, Point3(1.89, 1.89, 1.89))
    missPoint = lambda checkmark=checkmark, toon=toon: __toonMissPoint(checkmark, toon)
    pencilPosPoints = [
     Point3(-0.47, 1.08, 0.28), Point3(-21.8, -11.31, 176.19)]
    extraArgsForShowProp = [
     pencil, suit.getRightHand()]
    extraArgsForShowProp.extend(pencilPosPoints)
    pencilPropIvals = [
     WaitInterval(0.5), FunctionInterval(__showProp, extraArgs=extraArgsForShowProp), LerpScaleInterval(pencil, 0.5, Point3(1.5, 1.5, 1.5), startScale=Point3(0.01)), WaitInterval(2), FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[checkmark]), FunctionInterval(checkmark.reparentTo, extraArgs=[render]), FunctionInterval(checkmark.setScale, extraArgs=[1.6]), FunctionInterval(checkmark.setPosHpr, extraArgs=[pencil, 0, 0, 0, 0, 0, 0]), FunctionInterval(checkmark.setP, extraArgs=[0]), FunctionInterval(checkmark.setR, extraArgs=[0])]
    pencilPropIvals.extend(getPropThrowIntervals(attack, checkmark, [__toonFacePoint(toon)], [
     missPoint]))
    pencilPropIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[checkmark]))
    pencilPropIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[checkmark]))
    pencilPropIvals.append(WaitInterval(0.3))
    pencilPropIvals.append(LerpScaleInterval(pencil, 0.5, MovieUtil.PNT3_NEARZERO))
    pencilPropIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[pencil]))
    pencilPropTrack = Track(pencilPropIvals)
    toonTrack = getToonTrack(attack, 3.4, ['slip-forward'], 2.4, ['sidestep'])
    soundTrack = Track([WaitInterval(2.3), SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_pen_only.mp3'), duration=0.9, node=suit), SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_ding_only.mp3'), node=suit)])
    return MultiTrack([suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack])


def doRubberStamp(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    suitTrack = getSuitTrack(attack)
    stamp = globalPropPool.getProp('rubber-stamp')
    pad = globalPropPool.getProp('pad')
    cancelled = __makeCancelledNodePath()
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        padPosPoints = [
         Point3(-0.65, 0.83, -0.04), Point3(-6.58, -2.86, 165.07)]
        stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
    else:
        if suitType == 'c':
            padPosPoints = [
             Point3(0.19, -0.55, -0.21), Point3(-166.65, -3.61, -1.7)]
            stampPosPoints = [Point3(-0.64, -0.08, 0.11), MovieUtil.PNT3_ZERO]
        else:
            padPosPoints = [
             Point3(-0.65, 0.83, -0.04), Point3(-6.58, -2.86, 165.07)]
            stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 1e-06, 3.2)
    missPoint = lambda cancelled=cancelled, toon=toon: __toonMissPoint(cancelled, toon)
    propIvals = [
     FunctionInterval(__showProp, extraArgs=[stamp, suit.getRightHand(), stampPosPoints[0], stampPosPoints[1]]), LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_ONE), WaitInterval(2.6), FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[cancelled]), FunctionInterval(cancelled.reparentTo, extraArgs=[render]), FunctionInterval(cancelled.setScale, extraArgs=[0.6]), FunctionInterval(cancelled.setPosHpr, extraArgs=[stamp, 0.81, -1.11, -0.16, 0, 0, 270]), FunctionInterval(cancelled.setP, extraArgs=[0]), FunctionInterval(cancelled.setR, extraArgs=[0])]
    propIvals.extend(getPropThrowIntervals(attack, cancelled, [__toonFacePoint(toon)], [
     missPoint]))
    propIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[cancelled]))
    propIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[cancelled]))
    propIvals.append(WaitInterval(0.3))
    propIvals.append(LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_NEARZERO))
    propIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[stamp]))
    propTrack = Track(propIvals)
    toonTrack = getToonTrack(attack, 3.4, ['conked'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_rubber_stamp.mp3', delay=1.3, duration=1.1, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, padPropTrack, soundTrack])


def doRazzleDazzle(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    hitSuit = dmg > 0
    sign = globalPropPool.getProp('smile')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Smile')
    suitTrack = getSuitTrack(attack)
    signPosPoints = [
     Point3(0.0, -0.42, -0.04), Point3(171.09, 85.66, 14.78)]
    if hitSuit:
        hitPoint = lambda toon=toon: __toonFacePoint(toon)
    else:
        hitPoint = lambda particleEffect=particleEffect, toon=toon, suit=suit: __toonMissPoint(particleEffect, toon, parent=suit.getRightHand())
    signPropIvals = [
     WaitInterval(0.5), FunctionInterval(__showProp, extraArgs=[sign, suit.getRightHand(), signPosPoints[0], signPosPoints[1]]), LerpScaleInterval(sign, 0.5, Point3(1.39, 1.39, 1.39)), WaitInterval(0.5), FunctionInterval(battle.movie.needRestoreParticleEffect, extraArgs=[particleEffect]), FunctionInterval(particleEffect.start, extraArgs=[sign]), FunctionInterval(particleEffect.wrtReparentTo, extraArgs=[render]), LerpPosInterval(particleEffect, 2.0, pos=hitPoint), FunctionInterval(particleEffect.cleanup), FunctionInterval(battle.movie.clearRestoreParticleEffect, extraArgs=[particleEffect])]
    signPropTrack = Track(signPropIvals)
    signPropAnimInterval = [
     ActorInterval(sign, 'smile', duration=4, startTime=0)]
    signPropAnimTrack = Track(signPropAnimInterval)
    toonTrack = getToonTrack(attack, 2.6, ['cringe'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_razzle_dazzle.mp3', delay=1.6, node=suit)
    return Track([MultiTrack([suitTrack, signPropTrack, signPropAnimTrack, toonTrack, soundTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[sign])])


def doSynergy(attack):
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    damageDelay = 1.7
    hitAtleastOneToon = 0
    for t in targets:
        if t['hp'] > 0:
            hitAtleastOneToon = 1

    particleEffect = BattleParticles.createParticleEffect('Synergy')
    waterfallEffect = BattleParticles.createParticleEffect(file='synergyWaterfall')
    suitTrack = getSuitAnimTrack(attack)
    partTrack = getPartTrack(particleEffect, 1.0, 1.9, [particleEffect, suit, 0])
    waterfallTrack = getPartTrack(waterfallEffect, 0.8, 1.9, [
     waterfallEffect, suit, 0])
    damageAnims = [
     [
      'slip-forward']]
    dodgeAnims = []
    dodgeAnims.append(['jump', 0.01, 0, 0.6])
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.3, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91])
    toonTracks = getToonTracks(attack, damageDelay=damageDelay, damageAnimNames=['slip-forward'], dodgeDelay=0.91, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.0)
    synergySoundTrack = Track([(0.9, SoundInterval(globalBattleSoundCache.getSound('SA_synergy.mp3'), node=suit))])
    if hitAtleastOneToon > 0:
        fallingSoundTrack = Track([(damageDelay + 0.5, SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit))])
        return MultiTrack([suitTrack, partTrack, waterfallTrack, synergySoundTrack, fallingSoundTrack] + toonTracks)
    else:
        return MultiTrack([suitTrack, partTrack, waterfallTrack, synergySoundTrack] + toonTracks)


def doTeeOff(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    club = globalPropPool.getProp('golf-club')
    ball = globalPropPool.getProp('golf-ball')
    suitTrack = getSuitTrack(attack)
    clubPosPoints = [MovieUtil.PNT3_ZERO, Point3(48.3, 60.7, 20.0)]
    clubPropTrack = getPropTrack(club, suit.getLeftHand(), clubPosPoints, 0.5, 5.2, Point3(1.1, 1.1, 1.1))
    suitName = attack['suitName']
    if suitName == 'ym':
        ballPosPoints = [
         Point3(2.1, 0, 0.1)]
    else:
        if suitName == 'tbc':
            ballPosPoints = [
             Point3(4.1, 0, 0.1)]
        else:
            if suitName == 'm':
                ballPosPoints = [
                 Point3(3.2, 0, 0.1)]
            else:
                if suitName == 'rb':
                    ballPosPoints = [
                     Point3(4.2, 0, 0.1)]
                else:
                    ballPosPoints = [
                     Point3(2.1, 0, 0.1)]
    ballIvals = getPropAppearIntervals(ball, suit, ballPosPoints, 1.7, Point3(1.5, 1.5, 1.5))
    ballIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[ball]))
    ballIvals.append(FunctionInterval(ball.wrtReparentTo, extraArgs=[render]))
    ballIvals.append(WaitInterval(2.15))
    missPoint = lambda ball=ball, toon=toon: __toonMissPoint(ball, toon)
    ballIvals.extend(getPropThrowIntervals(attack, ball, [__toonFacePoint(toon)], [
     missPoint]))
    ballIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[ball]))
    ballPropTrack = Track(ballIvals)
    dodgeDelay = suitTrack.getDuration() - 4.35
    toonTrack = getToonTrack(attack, suitTrack.getDuration() - 2.25, ['conked'], dodgeDelay, ['duck'], showMissedExtraTime=1.7)
    soundTrack = getSoundTrack('SA_tee_off.mp3', delay=4.1, node=suit)
    return MultiTrack([suitTrack, toonTrack, clubPropTrack, ballPropTrack, soundTrack])


def doBrainStorm(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    BattleParticles.loadParticles()
    snowEffect = BattleParticles.createParticleEffect('BrainStorm')
    snowEffect2 = BattleParticles.createParticleEffect('BrainStorm')
    snowEffect3 = BattleParticles.createParticleEffect('BrainStorm')
    effectColor = Vec4(0.65, 0.79, 0.93, 0.3)
    BattleParticles.setEffectTexture(snowEffect, 'brainstorm-box', color=effectColor)
    BattleParticles.setEffectTexture(snowEffect2, 'brainstorm-env', color=effectColor)
    BattleParticles.setEffectTexture(snowEffect3, 'brainstorm-track', color=effectColor)
    cloud = globalPropPool.getProp('stormcloud')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 1.2
        damageDelay = 4.5
        dodgeDelay = 3.3
    else:
        if suitType == 'b':
            partDelay = 1.2
            damageDelay = 4.5
            dodgeDelay = 3.3
        else:
            if suitType == 'c':
                partDelay = 1.2
                damageDelay = 4.5
                dodgeDelay = 3.3
    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), Point3(180, 0, 0)]
    cloudIvals = []
    cloudIvals.append(FunctionInterval(cloud.pose, extraArgs=['stormcloud', 0]))
    cloudIvals.extend(getPropAppearIntervals(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7))
    cloudIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(cloud.wrtReparentTo, extraArgs=[render]))
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2] + 3)
    cloudIvals.append(WaitInterval(1.1))
    cloudIvals.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    cloudIvals.append(WaitInterval(partDelay))
    pivals = []
    pivals.append(Track([ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.2)]))
    pivals.append(Track([(0.5, ParticleInterval(snowEffect2, cloud, worldRelative=0, duration=1.7))]))
    pivals.append(Track([(1.0, ParticleInterval(snowEffect3, cloud, worldRelative=0, duration=1.2))]))
    pivals.append(Track([ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.5), ActorInterval(cloud, 'stormcloud', startTime=2.5, duration=0.5), ActorInterval(cloud, 'stormcloud', startTime=1, duration=1.5)]))
    cloudIvals.append(MultiTrack(pivals))
    cloudIvals.append(WaitInterval(0.4))
    cloudIvals.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
    cloudIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[cloud]))
    cloudPropTrack = Track(cloudIvals)
    damageAnims = [
     [
      'cringe', 0.01, 0.4, 0.8], ['duck', 1e-06, 1.6]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showMissedExtraTime=1.1)
    soundTrack = getSoundTrack('SA_brainstorm.mp3', delay=2.6, node=suit)
    return MultiTrack([suitTrack, toonTrack, cloudPropTrack, soundTrack])


def doBuzzWord(attack):
    suit = attack['suit']
    target = attack['target']
    toon = target['toon']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffects = []
    texturesList = ['buzzwords-crash', 'buzzwords-inc', 'buzzwords-main', 'buzzwords-over', 'buzzwords-syn']
    for i in range(0, 5):
        effect = BattleParticles.createParticleEffect('BuzzWord')
        if whrandom.random() > 0.5:
            BattleParticles.setEffectTexture(effect, texturesList[i], color=Vec4(1, 0.94, 0.02, 1))
        else:
            BattleParticles.setEffectTexture(effect, texturesList[i], color=Vec4(0, 0, 0, 1))
        particleEffects.append(effect)

    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 4.0
        partDuration = 2.2
        damageDelay = 4.5
        dodgeDelay = 3.8
    else:
        if suitType == 'b':
            partDelay = 1.3
            partDuration = 2
            damageDelay = 2.5
            dodgeDelay = 1.8
        else:
            if suitType == 'c':
                partDelay = 4.0
                partDuration = 2.2
                damageDelay = 4.5
                dodgeDelay = 3.8
    suitName = suit.getStyleName()
    if suitName == 'm':
        for effect in particleEffects:
            effect.setPos(0, 2.8, suit.getHeight() - 2.5)
            effect.setHpr(0, -20, 0)

    else:
        if suitName == 'mm':
            for effect in particleEffects:
                effect.setPos(0, 2.1, suit.getHeight() - 0.8)

    suitTrack = getSuitTrack(attack)
    particleTracks = []
    for effect in particleEffects:
        particleTracks.append(getPartTrack(effect, partDelay, partDuration, [
         effect, suit, 0]))

    toonTrack = getToonTrack(attack, damageDelay=damageDelay, damageAnimNames=['cringe'], splicedDodgeAnims=[['duck', dodgeDelay, 1.4]], showMissedExtraTime=dodgeDelay + 0.5)
    soundTrack = getSoundTrack('SA_buzz_word.mp3', delay=3.9, node=suit)
    return MultiTrack([suitTrack, toonTrack, soundTrack] + particleTracks)


def doDemotion(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect('DemotionSpray')
    freezeEffect = BattleParticles.createParticleEffect('DemotionFreeze')
    unFreezeEffect = BattleParticles.createParticleEffect(file='demotionUnFreeze')
    BattleParticles.setEffectTexture(sprayEffect, 'snow-particle')
    BattleParticles.setEffectTexture(freezeEffect, 'snow-particle')
    BattleParticles.setEffectTexture(unFreezeEffect, 'snow-particle')
    facePoint = __toonFacePoint(toon)
    freezeEffect.setPos(0, 0, facePoint.getZ())
    unFreezeEffect.setPos(0, 0, facePoint.getZ())
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(sprayEffect, 0.7, 1.1, [sprayEffect, suit, 0])
    partTrack2 = getPartTrack(freezeEffect, 1.4, 2.9, [freezeEffect, toon, 0])
    partTrack3 = getPartTrack(unFreezeEffect, 6.65, 0.5, [unFreezeEffect, toon, 0])
    dodgeAnims = [
     [
      'duck', 1e-06, 0.8]]
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0, 0.5])
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.4, 0.5, startTime=0.5))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.5, startTime=0.9))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.6, startTime=1.2))
    damageAnims.append(['cringe', 2.6, 1.5])
    toonTrack = getToonTrack(attack, damageDelay=1.0, splicedDamageAnims=damageAnims, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.6, showDamageExtraTime=1.3)
    soundTrack = getSoundTrack('SA_demotion.mp3', delay=1.2, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, toonTrack, soundTrack, partTrack, partTrack2, partTrack3])
    else:
        return MultiTrack([suitTrack, toonTrack, soundTrack, partTrack])


def doCanned(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    hips = toon.getHipsParts()
    propDelay = 0.8
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'c':
        suitDelay = 1.13
        dodgeDelay = 3.1
    else:
        suitDelay = 1.83
        dodgeDelay = 3.6
    throwDuration = 1.5
    can = globalPropPool.getProp('can')
    scale = 26
    torso = toon.style.torso
    torso = torso[0]
    if torso == 's':
        scaleUpPoint = Point3(scale * 2.63, scale * 2.63, scale * 1.9975)
    else:
        if torso == 'm':
            scaleUpPoint = Point3(scale * 2.63, scale * 2.63, scale * 1.7975)
        else:
            if torso == 'l':
                scaleUpPoint = Point3(scale * 2.63, scale * 2.63, scale * 2.31)
    canHpr = Point3(6.34, -181.62, -18.02)
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.14, 0.15, 0.08), Point3(6.34, -14.62, -198.02)]
    canIvals = getPropAppearIntervals(can, suit.getRightHand(), posPoints, propDelay, Point3(6, 6, 6), scaleUpTime=0.5)
    propDelay = propDelay + 0.5
    canIvals.append(WaitInterval(suitDelay))
    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.1)
    hitPoint.setY(hitPoint.getY() - 0.5)
    hitPoint.setZ(hitPoint.getZ() + toon.height + 1.1)
    canIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[can]))
    canIvals.extend(getThrowIvals(can, hitPoint, duration=throwDuration, parent=battle))
    if dmg > 0:
        can2 = MovieUtil.copyProp(can)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        can2Point = Point3(hitPoint.getX(), hitPoint.getY() + 6.4, hitPoint.getZ())
        can2.setPos(can2Point)
        can2.setScale(scaleUpPoint)
        can2.setHpr(canHpr)
        canIvals.append(FunctionInterval(battle.movie.needRestoreHips))
        canIvals.append(FunctionInterval(can.wrtReparentTo, extraArgs=[hips1]))
        canIvals.append(FunctionInterval(can2.reparentTo, extraArgs=[hips2]))
        canIvals.append(WaitInterval(2.4))
        canIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[can2]))
        canIvals.append(FunctionInterval(battle.movie.clearRestoreHips))
        scaleTrack = Track([WaitInterval(propDelay + suitDelay), LerpScaleInterval(can, throwDuration, scaleUpPoint)])
        hprTrack = Track([WaitInterval(propDelay + suitDelay), LerpHprInterval(can, throwDuration, canHpr)])
        soundTrack = Track([WaitInterval(2.6), SoundInterval(globalBattleSoundCache.getSound('SA_canned_tossup_only.mp3'), node=suit), SoundInterval(globalBattleSoundCache.getSound('SA_canned_impact_only.mp3'), node=suit)])
    else:
        land = toon.getPos(battle)
        land.setZ(land.getZ() + 0.7)
        bouncePoint1 = Point3(land.getX(), land.getY() - 1.5, land.getZ() + 2.5)
        bouncePoint2 = Point3(land.getX(), land.getY() - 2.1, land.getZ() - 0.2)
        bouncePoint3 = Point3(land.getX(), land.getY() - 3.1, land.getZ() + 1.5)
        bouncePoint4 = Point3(land.getX(), land.getY() - 4.1, land.getZ() + 0.3)
        canIvals.append(LerpPosInterval(can, 0.4, land))
        canIvals.append(LerpPosInterval(can, 0.4, bouncePoint1))
        canIvals.append(LerpPosInterval(can, 0.3, bouncePoint2))
        canIvals.append(LerpPosInterval(can, 0.3, bouncePoint3))
        canIvals.append(LerpPosInterval(can, 0.3, bouncePoint4))
        canIvals.append(WaitInterval(1.1))
        canIvals.append(LerpScaleInterval(can, 0.3, MovieUtil.PNT3_NEARZERO))
        scaleTrack = Track([WaitInterval(propDelay + suitDelay), LerpScaleInterval(can, throwDuration, Point3(11, 11, 11))])
        hprTrack = Track([WaitInterval(propDelay + suitDelay), LerpHprInterval(can, throwDuration, canHpr), WaitInterval(0.4), LerpHprInterval(can, 0.4, Point3(-96.34, -181.62, -18.02)), LerpHprInterval(can, 0.3, Point3(6.34, -91.62, -18.02)), LerpHprInterval(can, 0.2, Point3(96.34, 1.62, -181.02))])
        soundTrack = getSoundTrack('SA_canned_tossup_only.mp3', delay=2.6, node=suit)
    throwTrack = Track(canIvals)
    canTrack = Track([MultiTrack([throwTrack, scaleTrack, hprTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[can]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[can])])
    damageAnims = [
     [
      'struggle', propDelay + suitDelay + throwDuration, 0.01, 0.7], ['slip-backward', 0.01, 0.45]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showDamageExtraTime=propDelay + suitDelay + 2.4)
    return MultiTrack([suitTrack, toonTrack, canTrack, soundTrack])


def doDownsize(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 2.3
    sprayEffect = BattleParticles.createParticleEffect(file='downsizeSpray')
    cloudEffect = BattleParticles.createParticleEffect(file='downsizeCloud')
    toonPos = toon.getPos(toon)
    cloudPos = Point3(toonPos.getX(), toonPos.getY(), toonPos.getZ() + toon.getHeight() * 0.55)
    cloudEffect.setPos(cloudPos)
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.28, [sprayEffect, suit, 0])
    cloudTrack = getPartTrack(cloudEffect, 2.1, 1.9, [cloudEffect, toon, 0])
    if dmg > 0:
        initialScale = toon.getScale()
        downScale = Vec3(0.4, 0.4, 0.4)
        shrinkTrack = Track([WaitInterval(damageDelay + 0.5), FunctionInterval(battle.movie.needRestoreToonScale), LerpScaleInterval(toon, 1.0, downScale * 1.1), LerpScaleInterval(toon, 0.1, downScale * 0.9), LerpScaleInterval(toon, 0.1, downScale * 1.05), LerpScaleInterval(toon, 0.1, downScale * 0.95), LerpScaleInterval(toon, 0.1, downScale), WaitInterval(2.1), LerpScaleInterval(toon, 0.5, initialScale * 1.5), LerpScaleInterval(toon, 0.15, initialScale * 0.5), LerpScaleInterval(toon, 0.15, initialScale * 1.2), LerpScaleInterval(toon, 0.15, initialScale * 0.8), LerpScaleInterval(toon, 0.15, initialScale), FunctionInterval(battle.movie.clearRestoreToonScale)])
    damageAnims = []
    damageAnims.append(['juggle', 0.01, 0.87, 0.5])
    damageAnims.append(['lose', 0.01, 2.17, 0.93])
    damageAnims.append(['lose', 0.01, 3.1, -0.93])
    damageAnims.append(['struggle', 0.01, 0.8, 1.8])
    damageAnims.append(['sidestep-right', 0.01, 2.97, 1.49])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.6, dodgeAnimNames=['sidestep'])
    if dmg > 0:
        return MultiTrack([suitTrack, sprayTrack, cloudTrack, shrinkTrack, toonTrack])
    else:
        return MultiTrack([suitTrack, sprayTrack, toonTrack])


def doPinkSlip(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    paper = globalPropPool.getProp('pink-slip')
    throwDelay = 3.03
    throwDuration = 0.5
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.07, -0.06, -0.18), Point3(-153.43, 8.43, -93.01)]
    paperIvals = getPropAppearIntervals(paper, suit.getRightHand(), posPoints, 0.8, Point3(8, 8, 8), scaleUpTime=0.5)
    paperIvals.append(WaitInterval(1.73))
    hitPoint = __toonGroundPoint(attack, toon, 0.2, parent=battle)
    paperIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[paper]))
    paperIvals.append(FunctionInterval(paper.wrtReparentTo, extraArgs=[battle]))
    paperIvals.append(LerpPosInterval(paper, throwDuration, hitPoint))
    if dmg > 0:
        paperPause = 0.01
        slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ() + 4)
        landPoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
        paperIvals.append(WaitInterval(paperPause))
        paperIvals.append(LerpPosInterval(paper, 0.2, slidePoint))
        paperIvals.append(LerpPosInterval(paper, 1.1, landPoint))
        paperAppearTrack = Track(paperIvals)
        paperSpinTrack = Track([WaitInterval(throwDelay), LerpHprInterval(paper, throwDuration, Point3(300, 0, 0)), WaitInterval(paperPause), LerpHprInterval(paper, 1.3, Point3(-200, 100, 100))])
    else:
        slidePoint = Point3(hitPoint.getX(), hitPoint.getY() - 5, hitPoint.getZ())
        paperIvals.append(LerpPosInterval(paper, 0.5, slidePoint))
        paperAppearTrack = Track(paperIvals)
        paperSpinTrack = Track([WaitInterval(throwDelay), LerpHprInterval(paper, throwDuration, Point3(300, 0, 0)), LerpHprInterval(paper, 0.5, Point3(10, 0, 0))])
    propIvals = []
    propIvals.append(MultiTrack([paperAppearTrack, paperSpinTrack]))
    propIvals.append(LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO))
    propIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[paper]))
    propIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[paper]))
    propTrack = Track(propIvals)
    damageAnims = [
     [
      'jump', 0.01, 0.3, 0.7], ['slip-forward', 0.01]]
    toonTrack = getToonTrack(attack, damageDelay=2.81, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['jump'], showDamageExtraTime=0.9)
    soundTrack = getSoundTrack('SA_pink_slip.mp3', delay=2.9, duration=1.1, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack])


def doReOrg(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 1.7
    attackDelay = 1.7
    sprayEffect = BattleParticles.createParticleEffect(file='reorgSpray')
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    if dmg > 0:
        headParts = toon.getHeadParts()
        print '***********headParts pos=', headParts[0].getPos()
        print '***********headParts hpr=', headParts[0].getHpr()
        headTracks = []
        for partNum in range(0, headParts.getNumPaths()):
            part = headParts.getPath(partNum)
            x = part.getX()
            y = part.getY()
            z = part.getZ()
            h = part.getH()
            p = part.getP()
            r = part.getR()
            headTracks.append(Track([WaitInterval(attackDelay), LerpPosInterval(part, 0.1, Point3(x - 0.2, y, z - 0.03)), LerpPosInterval(part, 0.1, Point3(x + 0.4, y, z - 0.03)), LerpPosInterval(part, 0.1, Point3(x - 0.4, y, z - 0.03)), LerpPosInterval(part, 0.1, Point3(x + 0.4, y, z - 0.03)), LerpPosInterval(part, 0.1, Point3(x - 0.2, y, z - 0.04)), LerpPosInterval(part, 0.25, Point3(x, y, z + 2.2)), LerpHprInterval(part, 0.4, Point3(360, 0, 180)), LerpPosInterval(part, 0.3, Point3(x, y, z + 3.1)), LerpPosInterval(part, 0.15, Point3(x, y, z + 0.3)), WaitInterval(0.15), LerpHprInterval(part, 0.6, Point3(-745, 0, 180), startHpr=Point3(0, 0, 180)), LerpHprInterval(part, 0.8, Point3(25, 0, 180), startHpr=Point3(0, 0, 180)), LerpPosInterval(part, 0.15, Point3(x, y, z + 1)), LerpHprInterval(part, 0.3, Point3(h, p, r)), WaitInterval(0.2), LerpPosInterval(part, 0.1, Point3(x, y, z)), WaitInterval(0.9)]))

        def getChestTrack(part, attackDelay=attackDelay):
            origScale = part.getScale()
            return Track([WaitInterval(attackDelay), LerpHprInterval(part, 1.1, Point3(180, 0, 0)), WaitInterval(1.1), LerpHprInterval(part, 1.1, part.getHpr())])

        chestTracks = []
        arms = toon.findAllMatches('**/arms')
        sleeves = toon.findAllMatches('**/sleeves')
        hands = toon.findAllMatches('**/hands')
        print '*************arms hpr=', arms[0].getHpr()
        for partNum in range(0, arms.getNumPaths()):
            chestTracks.append(getChestTrack(arms.getPath(partNum)))
            chestTracks.append(getChestTrack(sleeves.getPath(partNum)))
            chestTracks.append(getChestTrack(hands.getPath(partNum)))

    damageAnims = [
     [
      'neutral', 0.01, 0.01, 0.5], ['juggle', 0.01, 0.01, 1.48], ['think', 0.01, 2.28]]
    dodgeAnims = []
    dodgeAnims.append(['think', 0.01, 0, 0.6])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.01, dodgeAnimNames=['duck'], showDamageExtraTime=2.1, showMissedExtraTime=2.0)
    if dmg > 0:
        return MultiTrack([suitTrack, partTrack, toonTrack] + headTracks + chestTracks)
    else:
        return MultiTrack([suitTrack, partTrack, toonTrack])


def doSacked(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    hips = toon.getHipsParts()
    propDelay = 0.85
    suitDelay = 1.93
    throwDuration = 0.9
    sack = globalPropPool.getProp('sandbag')
    initialScale = Point3(0.65, 1.47, 1.28)
    scaleUpPoint = Point3(1.05, 1.67, 0.98) * 4.1
    sackHpr = Point3(26.34, -181.62, -18.02)
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.51, -2.03, -0.73), Point3(12.27, -90.0, -65.02)]
    sackIvals = getPropAppearIntervals(sack, suit.getRightHand(), posPoints, propDelay, initialScale, scaleUpTime=0.2)
    propDelay = propDelay + 0.2
    sackIvals.append(WaitInterval(suitDelay))
    hitPoint = toon.getPos(battle)
    if dmg > 0:
        hitPoint.setX(hitPoint.getX() + 2.1)
        hitPoint.setY(hitPoint.getY() + 0.9)
        hitPoint.setZ(hitPoint.getZ() + toon.height + 1.2)
    else:
        hitPoint.setZ(hitPoint.getZ() - 0.2)
    sackIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[sack]))
    sackIvals.extend(getThrowIvals(sack, hitPoint, duration=throwDuration, parent=battle))
    if dmg > 0:
        sack2 = MovieUtil.copyProp(sack)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        sack2.hide()
        sack2.reparentTo(battle)
        sack2.setPos(Point3(hitPoint.getX(), hitPoint.getY(), hitPoint.getZ()))
        sack2.setScale(scaleUpPoint)
        sack2.setHpr(sackHpr)
        sackIvals.append(FunctionInterval(battle.movie.needRestoreHips))
        sackIvals.append(FunctionInterval(sack.wrtReparentTo, extraArgs=[hips1]))
        sackIvals.append(FunctionInterval(sack2.show))
        sackIvals.append(FunctionInterval(sack2.wrtReparentTo, extraArgs=[hips2]))
        sackIvals.append(WaitInterval(2.4))
        sackIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[sack2]))
        sackIvals.append(FunctionInterval(battle.movie.clearRestoreHips))
        scaleTrack = Track([WaitInterval(propDelay + suitDelay), LerpScaleInterval(sack, throwDuration, scaleUpPoint), WaitInterval(1.8), LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO)])
        hprTrack = Track([WaitInterval(propDelay + suitDelay), LerpHprInterval(sack, throwDuration, sackHpr)])
        sackTrack = Track([MultiTrack([Track(sackIvals), scaleTrack, hprTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[sack]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[sack])])
    else:
        sackIvals.append(WaitInterval(1.1))
        sackIvals.append(LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO))
        sackTrack = Track([Track(sackIvals), FunctionInterval(MovieUtil.removeProp, extraArgs=[sack]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[sack])])
    damageAnims = [
     [
      'struggle', 0.01, 0.01, 0.7], ['slip-backward', 0.01, 0.45]]
    toonTrack = getToonTrack(attack, damageDelay=propDelay + suitDelay + throwDuration, splicedDamageAnims=damageAnims, dodgeDelay=3.0, dodgeAnimNames=['sidestep'], showDamageExtraTime=1.8, showMissedExtraTime=0.8)
    return MultiTrack([suitTrack, toonTrack, sackTrack])


def doGlowerPower(attack):
    suit = attack['suit']
    battle = attack['battle']
    leftKnives = []
    rightKnives = []
    for i in range(0, 3):
        leftKnives.append(globalPropPool.getProp('dagger'))
        rightKnives.append(globalPropPool.getProp('dagger'))

    suitTrack = getSuitTrack(attack)
    suitName = suit.getStyleName()
    if suitName == 'hh':
        leftPosPoints = [
         Point3(0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
    else:
        if suitName == 'tbc':
            leftPosPoints = [
             Point3(0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
            rightPosPoints = [Point3(-0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
        else:
            leftPosPoints = [
             Point3(0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
            rightPosPoints = [Point3(-0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
    leftKnifeTracks = []
    rightKnifeTracks = []
    for i in range(0, 3):
        knifeDelay = 0.11
        leftIvals = []
        leftIvals.append(WaitInterval(1.1))
        leftIvals.append(WaitInterval(i * knifeDelay))
        leftIvals.extend(getPropAppearIntervals(leftKnives[i], suit, leftPosPoints, 1e-06, Point3(0.4, 0.4, 0.4), scaleUpTime=0.1))
        leftIvals.extend(getPropThrowIntervals(attack, leftKnives[i], hitPointNames=['face'], missPointNames=['miss'], hitDuration=0.3, missDuration=0.3))
        leftKnifeTracks.append(Track(leftIvals))
        rightIvals = []
        rightIvals.append(WaitInterval(1.1))
        rightIvals.append(WaitInterval(i * knifeDelay))
        rightIvals.extend(getPropAppearIntervals(rightKnives[i], suit, rightPosPoints, 1e-06, Point3(0.4, 0.4, 0.4), scaleUpTime=0.1))
        rightIvals.extend(getPropThrowIntervals(attack, rightKnives[i], hitPointNames=['face'], missPointNames=['miss'], hitDuration=0.3, missDuration=0.3))
        rightKnifeTracks.append(Track(rightIvals))

    damageAnims = [['slip-backward', 0.01, 0.35]]
    toonTrack = getToonTrack(attack, damageDelay=1.6, splicedDamageAnims=damageAnims, dodgeDelay=0.7, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_glower_power.mp3', delay=1.1, node=suit)
    return MultiTrack([suitTrack, toonTrack, soundTrack] + leftKnifeTracks + rightKnifeTracks)


def doHalfWindsor(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('half-windsor')
    throwDelay = 2.17
    damageDelay = 3.4
    dodgeDelay = 2.4
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.02, 0.88, 0.48), Point3(-161.56, -80.54, -90.0)]
    tiePropIvals = getPropAppearIntervals(tie, suit.getRightHand(), posPoints, 0.5, Point3(7, 7, 7), scaleUpTime=0.5)
    tiePropIvals.append(WaitInterval(throwDelay))
    missPoint = __toonMissBehindPoint(toon, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    missPoint.setZ(missPoint.getZ() + 4)
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.1)
    hitPoint.setY(hitPoint.getY() - 0.7)
    hitPoint.setZ(hitPoint.getZ() + 0.9)
    tiePropIvals.extend(getPropThrowIntervals(attack, tie, [hitPoint], [missPoint], hitDuration=0.4, missDuration=0.8, missScaleDown=0.3, parent=battle))
    tiePropTrack = Track(tiePropIvals)
    damageAnims = [
     [
      'conked', 0.01, 0.01, 0.4], ['cringe', 0.01, 0.7]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    return MultiTrack([suitTrack, toonTrack, tiePropTrack])


def doHeadShrink(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 2.1
    dodgeDelay = 1.4
    shrinkSpray = BattleParticles.createParticleEffect(file='headShrinkSpray')
    shrinkCloud = BattleParticles.createParticleEffect(file='headShrinkCloud')
    shrinkDrop = BattleParticles.createParticleEffect(file='headShrinkDrop')
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(shrinkSpray, 0.3, 1.4, [shrinkSpray, suit, 0])
    shrinkCloud.reparentTo(battle)
    adjust = 0.4
    x = toon.getX(battle)
    y = toon.getY(battle) - adjust
    z = 8
    shrinkCloud.setPos(Point3(x, y, z))
    shrinkDrop.setPos(Point3(0, 0 - adjust, 7.5))
    off = 0.7
    cloudPoints = [Point3(x + off, y, z), Point3(x + off / 2, y + off / 2, z), Point3(x, y + off, z), Point3(x - off / 2, y + off / 2, z), Point3(x - off, y, z), Point3(x - off / 2, y - off / 2, z), Point3(x, y - off, z), Point3(x + off / 2, y - off / 2, z), Point3(x + off, y, z), Point3(x, y, z)]
    circleIvals = []
    for point in cloudPoints:
        circleIvals.append(LerpPosInterval(shrinkCloud, 0.14, point, other=battle))

    cloudIvals = []
    cloudIvals.append(WaitInterval(1.42))
    cloudIvals.append(FunctionInterval(battle.movie.needRestoreParticleEffect, extraArgs=[shrinkCloud]))
    cloudIvals.append(FunctionInterval(shrinkCloud.start, extraArgs=[battle]))
    cloudIvals.extend(circleIvals)
    cloudIvals.extend(circleIvals)
    cloudIvals.append(LerpFunctionInterval(shrinkCloud.setAlphaScale, fromData=1, toData=0, duration=0.7))
    cloudIvals.append(FunctionInterval(shrinkCloud.cleanup))
    cloudIvals.append(FunctionInterval(battle.movie.clearRestoreParticleEffect, extraArgs=[shrinkCloud]))
    cloudTrack = Track(cloudIvals)
    shrinkDelay = 0.8
    shrinkDuration = 1.1
    shrinkIvals = []
    if dmg > 0:
        headParts = toon.getHeadParts()
        initialScale = headParts.getPath(0).getScale()[0]
        shrinkIvals.append(WaitInterval(damageDelay + shrinkDelay))
        headTracks = []

        def scaleHeadMultiTrack(scale, duration, headParts=headParts):
            headTracks = []
            for partNum in range(0, headParts.getNumPaths()):
                nextPart = headParts.getPath(partNum)
                headTracks.append(Track([
                 LerpScaleInterval(nextPart, duration, Point3(scale, scale, scale))]))

            return MultiTrack(headTracks)

        shrinkIvals.append(FunctionInterval(battle.movie.needRestoreHeadScale))
        shrinkIvals.append(scaleHeadMultiTrack(0.6, shrinkDuration))
        shrinkIvals.append(WaitInterval(1.6))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 3.2, 0.4))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 0.7, 0.4))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 2.5, 0.3))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 0.8, 0.3))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 1.9, 0.2))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 0.85, 0.2))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 1.7, 0.15))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 0.9, 0.15))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale * 1.3, 0.1))
        shrinkIvals.append(scaleHeadMultiTrack(initialScale, 0.1))
        shrinkIvals.append(FunctionInterval(battle.movie.clearRestoreHeadScale))
        shrinkIvals.append(WaitInterval(0.7))
        shrinkTrack = Track(shrinkIvals)
    dropTrack = getPartTrack(shrinkDrop, 1.5, 2.5, [shrinkDrop, toon, 0])
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.65, 0.2])
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.64, 1.0, startTime=0.85))
    damageAnims.append(['cringe', 0.4, 1.49])
    damageAnims.append(['conked', 0.01, 3.6, -1.6])
    damageAnims.append(['conked', 0.01, 3.1, 0.4])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    if dmg > 0:
        shrinkSound = globalBattleSoundCache.getSound('SA_head_shrink_only.mp3')
        growSound = globalBattleSoundCache.getSound('SA_head_grow_back_only.mp3')
        soundTrack = Track([WaitInterval(2.1), SoundInterval(shrinkSound, duration=2.1, node=suit), WaitInterval(1.6), SoundInterval(growSound, node=suit)])
        return MultiTrack([suitTrack, sprayTrack, cloudTrack, dropTrack, toonTrack, shrinkTrack, soundTrack])
    else:
        return MultiTrack([suitTrack, sprayTrack, cloudTrack, dropTrack, toonTrack])


def doRolodex(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    rollodex = globalPropPool.getProp('rollodex')
    particleEffect2 = BattleParticles.createParticleEffect(file='rollodexWaterfall')
    particleEffect3 = BattleParticles.createParticleEffect(file='rollodexStream')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        propPosPoints = [
         Point3(-0.51, -0.03, -0.1), Point3(-87.75, -81.64, -100.52)]
        propScale = Point3(1.2, 1.2, 1.2)
        partDelay = 2.6
        part2Delay = 2.8
        part3Delay = 3.2
        partDuration = 1.6
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 3.8
        dodgeDelay = 2.5
    else:
        if suitType == 'b':
            propPosPoints = [
             Point3(0.12, 0.24, 0.01), Point3(-99.05, -6.98, -178.98)]
            propScale = Point3(0.91, 0.91, 0.91)
            partDelay = 2.9
            part2Delay = 3.1
            part3Delay = 3.5
            partDuration = 1.6
            part2Duration = 1.9
            part3Duration = 1
            damageDelay = 4
            dodgeDelay = 2.5
        else:
            if suitType == 'c':
                propPosPoints = [
                 Point3(-0.51, -0.03, -0.1), Point3(-87.75, -81.64, -100.52)]
                propScale = Point3(1.2, 1.2, 1.2)
                partDelay = 2.3
                part2Delay = 2.8
                part3Delay = 3.2
                partDuration = 1.9
                part2Duration = 1.9
                part3Duration = 1
                damageDelay = 3.5
                dodgeDelay = 2.5
    hitPoint = lambda toon=toon: __toonFacePoint(toon)
    partTrack2 = getPartTrack(particleEffect2, part2Delay, part2Duration, [
     particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, part3Delay, part3Duration, [
     particleEffect3, suit, 0])
    suitTrack = getSuitTrack(attack)
    propTrack = getPropTrack(rollodex, suit.getLeftHand(), propPosPoints, 1e-06, 4.7, scaleUpPoint=propScale, anim=0, propName='rollodex', animDuration=0, animStartTime=0)
    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    soundTrack = getSoundTrack('SA_rolodex.mp3', delay=2.8, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack, partTrack2, partTrack3])


def doEvilEye(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    eye = globalPropPool.getProp('evil-eye')
    damageDelay = 2.44
    dodgeDelay = 1.64
    suitName = suit.getStyleName()
    if suitName == 'cr':
        posPoints = [
         Point3(-0.46, 4.85, 5.28), Point3(205, -20, 0)]
    else:
        if suitName == 'tf':
            posPoints = [
             Point3(-0.4, 3.65, 5.01), Point3(205, -20, 0)]
        else:
            if suitName == 'le':
                posPoints = [
                 Point3(-0.64, 4.45, 5.91), Point3(205, -20, 0)]
            else:
                posPoints = [
                 Point3(-0.4, 3.65, 5.01), Point3(205, -20, 0)]
    appearDelay = 0.8
    suitHoldStart = 1.06
    suitHoldStop = 1.69
    suitHoldDuration = suitHoldStop - suitHoldStart
    eyeHoldDuration = 1.1
    moveDuration = 1.1
    suitSplicedAnims = []
    suitSplicedAnims.append(['glower', 0.01, 0.01, suitHoldStart])
    suitSplicedAnims.extend(getSplicedLerpAnims('glower', suitHoldDuration, 1.1, startTime=suitHoldStart))
    suitSplicedAnims.append(['glower', 0.01, suitHoldStop])
    suitTrack = getSuitTrack(attack, splicedAnims=suitSplicedAnims)
    eyeAppearTrack = Track([WaitInterval(suitHoldStart), FunctionInterval(__showProp, extraArgs=[eye, suit, posPoints[0], posPoints[1]]), LerpScaleInterval(eye, suitHoldDuration, Point3(11, 11, 11)), WaitInterval(eyeHoldDuration * 0.3), LerpHprInterval(eye, 0.02, Point3(205, 40, 0)), WaitInterval(eyeHoldDuration * 0.7), FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[eye]), FunctionInterval(eye.wrtReparentTo, extraArgs=[battle])])
    toonFace = __toonFacePoint(toon, parent=battle)
    if dmg > 0:
        lerpInterval = LerpPosInterval(eye, moveDuration, toonFace)
    else:
        lerpInterval = LerpPosInterval(eye, moveDuration, Point3(toonFace.getX(), toonFace.getY() - 5, toonFace.getZ() - 2))
    eyeMoveTrack = Track([lerpInterval])
    eyeRollTrack = Track([LerpHprInterval(eye, moveDuration, Point3(0, 0, 180))])
    eyePropTrack = Track([eyeAppearTrack, MultiTrack([eyeMoveTrack, eyeRollTrack]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[eye]), FunctionInterval(MovieUtil.removeProp, extraArgs=[eye])])
    damageAnims = [
     [
      'duck', 0.01, 0.01, 1.4], ['cringe', 0.01, 0.3]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, damageDelay=damageDelay, dodgeDelay=dodgeDelay, dodgeAnimNames=['duck'], showDamageExtraTime=1.7, showMissedExtraTime=1.7)
    soundTrack = getSoundTrack('SA_evil_eye.mp3', delay=1.3, node=suit)
    return MultiTrack([suitTrack, toonTrack, eyePropTrack, soundTrack])


def doPlayHardball(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    ball = globalPropPool.getProp('baseball')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        suitDelay = 1.09
        damageDelay = 2.76
        dodgeDelay = 1.86
    else:
        if suitType == 'b':
            suitDelay = 1.79
            damageDelay = 3.46
            dodgeDelay = 2.56
        else:
            if suitType == 'c':
                suitDelay = 1.09
                damageDelay = 2.76
                dodgeDelay = 1.86
    suitTrack = getSuitTrack(attack)
    ballPosPoints = [Point3(0.04, 0.03, -0.31), Point3(-77.47, 74.05, 15.52)]
    ballIvals = getPropAppearIntervals(ball, suit.getRightHand(), ballPosPoints, 0.8, Point3(5, 5, 5), scaleUpTime=0.5)
    ballIvals.append(WaitInterval(suitDelay))
    ballIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[ball]))
    ballIvals.append(FunctionInterval(ball.wrtReparentTo, extraArgs=[battle]))
    toonPos = toon.getPos(battle)
    x = toonPos.getX()
    y = toonPos.getY()
    z = toonPos.getZ()
    z = z + 0.2
    if dmg > 0:
        ballIvals.append(LerpPosInterval(ball, 0.5, __toonFacePoint(toon, parent=battle)))
        ballIvals.append(LerpPosInterval(ball, 0.5, Point3(x, y + 3, z)))
        ballIvals.append(LerpPosInterval(ball, 0.4, Point3(x, y + 5, z + 2)))
        ballIvals.append(LerpPosInterval(ball, 0.3, Point3(x, y + 6, z)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y + 7, z + 1)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y + 8, z)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y + 8.5, z + 0.6)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y + 9, z + 0.2)))
        ballIvals.append(WaitInterval(0.4))
        soundTrack = getSoundTrack('SA_hardball_impact_only.mp3', delay=2.8, node=suit)
    else:
        ballIvals.append(LerpPosInterval(ball, 0.5, Point3(x, y + 2, z)))
        ballIvals.append(LerpPosInterval(ball, 0.4, Point3(x, y - 1, z + 2)))
        ballIvals.append(LerpPosInterval(ball, 0.3, Point3(x, y - 3, z)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y - 4, z + 1)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y - 5, z)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y - 5.5, z + 0.6)))
        ballIvals.append(LerpPosInterval(ball, 0.1, Point3(x, y - 6, z + 0.2)))
        ballIvals.append(WaitInterval(0.4))
        soundTrack = getSoundTrack('SA_hardball.mp3', delay=3.1, node=suit)
    ballIvals.append(LerpScaleInterval(ball, 0.3, MovieUtil.PNT3_NEARZERO))
    ballIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[ball]))
    ballIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[ball]))
    propTrack = Track(ballIvals)
    damageAnims = [
     [
      'conked', damageDelay, 0.01, 0.5], ['slip-backward', 0.01, 0.7]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showDamageExtraTime=3.9)
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack])


def doPowerTie(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('power-tie')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    else:
        if suitType == 'b':
            throwDelay = 2.17
            damageDelay = 3.3
            dodgeDelay = 3.1
        else:
            if suitType == 'c':
                throwDelay = 1.45
                damageDelay = 2.61
                dodgeDelay = 2.34
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(1.16, 0.24, 0.63), Point3(-172.41, -4.09, -163.3)]
    tiePropIvals = getPropAppearIntervals(tie, suit.getRightHand(), posPoints, 0.5, Point3(3.5, 3.5, 3.5), scaleUpTime=0.5)
    tiePropIvals.append(WaitInterval(throwDelay))
    tiePropIvals.append(FunctionInterval(tie.setBillboardPointEye))
    tiePropIvals.extend(getPropThrowIntervals(attack, tie, [__toonFacePoint(toon)], [
     __toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4, missDuration=0.8))
    tiePropTrack = Track(tiePropIvals)
    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    throwSound = getSoundTrack('SA_powertie_throw.mp3', delay=2.3, node=suit)
    if dmg > 0:
        hitSound = getSoundTrack('SA_powertie_impact.mp3', delay=2.9, node=suit)
        return MultiTrack([suitTrack, toonTrack, tiePropTrack, throwSound, hitSound])
    else:
        return MultiTrack([suitTrack, toonTrack, tiePropTrack, throwSound])


def doDoubleTalk(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('DoubleTalkLeft')
    particleEffect2 = BattleParticles.createParticleEffect('DoubleTalkRight')
    BattleParticles.setEffectTexture(particleEffect, 'doubletalk-double', color=Vec4(0, 1.0, 0.0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'doubletalk-good', color=Vec4(0, 1.0, 0.0, 1))
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 3.3
        damageDelay = 3.5
        dodgeDelay = 3.3
    else:
        if suitType == 'b':
            partDelay = 3.3
            damageDelay = 3.5
            dodgeDelay = 3.3
        else:
            if suitType == 'c':
                partDelay = 3.3
                damageDelay = 3.5
                dodgeDelay = 3.3
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay, 1.8, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay, 1.8, [particleEffect2, suit, 0])
    damageAnims = [['duck', 0.01, 0.4, 1.05], ['cringe', 1e-06, 0.8]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=[['duck', 0.01, 1.4]], showMissedExtraTime=0.9, showDamageExtraTime=0.8)
    soundTrack = getSoundTrack('SA_filibuster.mp3', delay=2.5, node=suit)
    return MultiTrack([suitTrack, toonTrack, partTrack, partTrack2, soundTrack])


def doFreezeAssets(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    BattleParticles.loadParticles()
    snowEffect = BattleParticles.createParticleEffect('FreezeAssets')
    BattleParticles.setEffectTexture(snowEffect, 'snow-particle')
    cloud = globalPropPool.getProp('stormcloud')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.3
    else:
        if suitType == 'b':
            partDelay = 0.2
            damageDelay = 3.5
            dodgeDelay = 2.3
        else:
            if suitType == 'c':
                partDelay = 0.2
                damageDelay = 3.5
                dodgeDelay = 2.3
    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), MovieUtil.PNT3_ZERO]
    cloudIvals = []
    cloudIvals.append(FunctionInterval(cloud.pose, extraArgs=['stormcloud', 0]))
    cloudIvals.extend(getPropAppearIntervals(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7))
    cloudIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(cloud.wrtReparentTo, extraArgs=[render]))
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2] + 3)
    cloudIvals.append(WaitInterval(1.1))
    cloudIvals.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    cloudIvals.append(WaitInterval(partDelay))
    cloudIvals.append(ParticleInterval(snowEffect, cloud, worldRelative=0, duration=2.1))
    cloudIvals.append(WaitInterval(0.4))
    cloudIvals.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
    cloudIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[cloud]))
    cloudPropTrack = Track(cloudIvals)
    damageAnims = [
     [
      'cringe', 0.01, 0.4, 0.8], ['duck', 0.01, 1.6]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showMissedExtraTime=1.2)
    return MultiTrack([suitTrack, toonTrack, cloudPropTrack])


def doHotAir(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect('HotAir')
    baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameEffect = BattleParticles.createParticleEffect('FiredFlame')
    flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(sprayEffect, 'fire')
    BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
    BattleParticles.setEffectTexture(flameEffect, 'fire')
    BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex', color=Vec4(200, 200, 200, 1))
    sprayDelay = 1.3
    flameDelay = 3.2
    flameDuration = 2.6
    flecksDelay = flameDelay + 0.8
    flecksDuration = flameDuration - 0.8
    damageDelay = 3.6
    dodgeDelay = 2.0
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, sprayDelay, 2.3, [sprayEffect, suit, 0])
    baseFlameTrack = getPartTrack(baseFlameEffect, flameDelay, flameDuration, [
     baseFlameEffect, toon, 0])
    flameTrack = getPartTrack(flameEffect, flameDelay, flameDuration, [flameEffect, toon, 0])
    flecksTrack = getPartTrack(flecksEffect, flecksDelay, flecksDuration, [
     flecksEffect, toon, 0])

    def changeColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.setColorScale, extraArgs=[Vec4(0, 0, 0, 1)]))

        return ivals

    def resetColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.clearColorScale))

        return ivals

    if dmg > 0:
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()
        colorIvals = []
        colorIvals.append(WaitInterval(4.0))
        colorIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        colorIvals.extend(changeColor(headParts))
        colorIvals.extend(changeColor(torsoParts))
        colorIvals.extend(changeColor(legsParts))
        colorIvals.append(WaitInterval(3.5))
        colorIvals.extend(resetColor(headParts))
        colorIvals.extend(resetColor(torsoParts))
        colorIvals.extend(resetColor(legsParts))
        colorIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        colorTrack = Track(colorIvals)
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.7, 0.62])
    damageAnims.append(['slip-forward', 0.01, 0.4, 1.2])
    damageAnims.append(['slip-forward', 0.01, 1.0])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_hot_air.mp3', delay=1.6, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, toonTrack, sprayTrack, soundTrack, baseFlameTrack, flameTrack, flecksTrack, colorTrack])
    else:
        return MultiTrack([suitTrack, toonTrack, sprayTrack, soundTrack])


def doPickPocket(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    bill = globalPropPool.getProp('1dollar')
    suitTrack = getSuitTrack(attack)
    billPosPoints = [Point3(-0.01, 0.45, -0.25), Point3(-122.41, -21.32, -98.44)]
    billPropTrack = getPropTrack(bill, suit.getRightHand(), billPosPoints, 0.6, 0.55, scaleUpPoint=Point3(1.41, 1.41, 1.41))
    toonTrack = getToonTrack(attack, 0.6, ['cringe'], 0.01, ['sidestep'])
    multiTrackList = [
     suitTrack, toonTrack]
    if dmg > 0:
        soundTrack = getSoundTrack('SA_pick_pocket.mp3', delay=0.2, node=suit)
        multiTrackList.append(billPropTrack)
        multiTrackList.append(soundTrack)
    return MultiTrack(multiTrackList)


def doFilibuster(attack):
    suit = attack['suit']
    target = attack['target']
    dmg = target['hp']
    battle = attack['battle']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect4 = BattleParticles.createParticleEffect(file='filibusterSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect, 'filibuster-cut', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'filibuster-fiscal', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'filibuster-impeach', color=color)
    BattleParticles.setEffectTexture(sprayEffect4, 'filibuster-inc', color=color)
    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 2.45
    dodgeDelay = 1.7
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, partDelay, partDuration, [
     sprayEffect, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay + 0.8, partDuration, [
     sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay + 1.6, partDuration, [
     sprayEffect3, suit, 0])
    sprayTrack4 = getPartTrack(sprayEffect4, partDelay + 2.4, partDuration, [
     sprayEffect4, suit, 0])
    damageAnims = []
    for i in range(0, 4):
        damageAnims.append(['cringe', 1e-05, 0.3, 0.8])

    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_filibuster.mp3', delay=1.1, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, toonTrack, soundTrack, sprayTrack, sprayTrack2, sprayTrack3, sprayTrack4])
    else:
        return MultiTrack([suitTrack, toonTrack, soundTrack, sprayTrack, sprayTrack2, sprayTrack3])


def doSchmooze(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    upperEffects = []
    lowerEffects = []
    textureNames = ['schmooze-genius', 'schmooze-instant', 'schmooze-master', 'schmooze-viz']
    for i in range(0, 4):
        upperEffect = BattleParticles.createParticleEffect(file='schmoozeUpperSpray')
        lowerEffect = BattleParticles.createParticleEffect(file='schmoozeLowerSpray')
        BattleParticles.setEffectTexture(upperEffect, textureNames[i], color=Vec4(0, 0, 1, 1))
        BattleParticles.setEffectTexture(lowerEffect, textureNames[i], color=Vec4(0, 0, 1, 1))
        upperEffects.append(upperEffect)
        lowerEffects.append(lowerEffect)

    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 1.3
        damageDelay = 1.8
        dodgeDelay = 1.1
    else:
        if suitType == 'b':
            partDelay = 1.3
            damageDelay = 2.5
            dodgeDelay = 1.8
        else:
            if suitType == 'c':
                partDelay = 1.3
                damageDelay = partDelay + 1.4
                dodgeDelay = 0.9
    suitTrack = getSuitTrack(attack)
    upperPartTracks = []
    lowerPartTracks = []
    for i in range(0, 4):
        upperPartTracks.append(getPartTrack(upperEffects[i], partDelay + i * 0.65, 0.8, [upperEffects[i], suit, 0]))
        lowerPartTracks.append(getPartTrack(lowerEffects[i], partDelay + i * 0.65 + 0.7, 1.0, [lowerEffects[i], suit, 0]))

    damageAnims = []
    for i in range(0, 3):
        damageAnims.append(['conked', 0.01, 0.3, 0.71])

    damageAnims.append(['conked', 0.01, 0.3])
    dodgeAnims = []
    dodgeAnims.append(['duck', 0.01, 0.2, 2.7])
    dodgeAnims.append(['duck', 0.01, 1.22, 1.28])
    dodgeAnims.append(['duck', 0.01, 3.16])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.9, showDamageExtraTime=1.1)
    return MultiTrack([suitTrack, toonTrack] + upperPartTracks + lowerPartTracks)


def doQuake(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [
     [
      'slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.8, splicedDamageAnims=damageAnims, dodgeDelay=1.1, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    return MultiTrack([suitTrack] + toonTracks)


def doShake(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [
     [
      'slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.1, splicedDamageAnims=damageAnims, dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    return MultiTrack([suitTrack] + toonTracks)


def doTremor(attack):
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)
    damageAnims = [
     [
      'slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(attack, damageDelay=1.1, splicedDamageAnims=damageAnims, dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    soundTrack = getSoundTrack('SA_tremor.mp3', delay=0.9, node=suit)
    return MultiTrack([suitTrack, soundTrack] + toonTracks)


def doHangUp(attack):
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    suitTrack = getSuitTrack(attack)
    suitName = suit.getStyleName()
    if suitName == 'tf':
        phonePosPoints = [
         Point3(-0.23, 0.01, -0.26), Point3(-6.05, -2.51, 177.58)]
        receiverPosPoints = [Point3(-0.13, -0.07, -0.06), Point3(1.75, -2.51, 177.58)]
        receiverAdjustScale = Point3(0.8, 0.8, 0.8)
        pickupDelay = 0.44
        dialDuration = 3.07
        finalPhoneDelay = 0.01
        scaleUpPoint = Point3(0.75, 0.75, 0.75)
    else:
        phonePosPoints = [
         Point3(0.23, 0.17, -0.11), Point3(-6.05, -2.51, 177.58)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), Point3(-6.05, -2.51, 177.58)]
        receiverAdjustScale = MovieUtil.PNT3_ONE
        pickupDelay = 0.74
        dialDuration = 3.07
        finalPhoneDelay = 0.69
        scaleUpPoint = MovieUtil.PNT3_ONE
    propTrack = Track([WaitInterval(0.3), FunctionInterval(__showProp, extraArgs=[phone, suit.getLeftHand(), phonePosPoints[0], phonePosPoints[1]]), FunctionInterval(__showProp, extraArgs=[receiver, suit.getLeftHand(), receiverPosPoints[0], receiverPosPoints[1]]), LerpScaleInterval(phone, 0.5, scaleUpPoint, MovieUtil.PNT3_NEARZERO), WaitInterval(pickupDelay), FunctionInterval(receiver.wrtReparentTo, extraArgs=[suit.getRightHand()]), LerpScaleInterval(receiver, 0.01, receiverAdjustScale),
     LerpPosHprInterval(receiver, 0.0001, Point3(-0.53, 0.21, -0.54), Point3(-100.66, -43.3, 8.15)), WaitInterval(dialDuration), FunctionInterval(receiver.wrtReparentTo, extraArgs=[phone]), WaitInterval(finalPhoneDelay), LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO), FunctionInterval(MovieUtil.removeProps, extraArgs=[[receiver, phone]])])
    toonTrack = getToonTrack(attack, 5.5, ['slip-backward'], 4.7, ['jump'])
    soundTrack = getSoundTrack('SA_hangup.mp3', delay=1.3, node=suit)
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack])


def doRedTape(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tape = globalPropPool.getProp('redtape')
    tubes = []
    for i in range(0, 3):
        tubes.append(globalPropPool.getProp('redtape-tube'))

    suitTrack = getSuitTrack(attack)
    suitName = suit.getStyleName()
    if suitName == 'tf' or suitName == 'nc':
        tapePosPoints = [
         Point3(-0.24, 0.09, -0.38), Point3(-77.47, 74.05, 15.52)]
    else:
        tapePosPoints = [
         Point3(0.24, 0.09, -0.38), Point3(-77.47, 74.05, 15.52)]
    tapeScaleUpPoint = Point3(0.9, 0.9, 0.24)
    tapeIvals = getPropAppearIntervals(tape, suit.getRightHand(), tapePosPoints, 0.8, tapeScaleUpPoint, scaleUpTime=0.5)
    tapeIvals.append(WaitInterval(1.73))
    hitPoint = lambda toon=toon: __toonTorsoPoint(toon)
    tapeIvals.extend(getPropThrowIntervals(attack, tape, [hitPoint], [
     __toonGroundPoint(attack, toon, 0.7)]))
    propTrack = Track(tapeIvals)
    hips = toon.getHipsParts()
    animal = toon.style.getAnimal()
    scale = Toon.toonBodyScales[animal]
    legs = toon.style.legs
    torso = toon.style.torso
    torso = torso[0]
    animal = animal[0]
    tubeHeight = -0.8
    if torso == 's':
        scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
    else:
        if torso == 'm':
            scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 0.7975)
        else:
            if torso == 'l':
                scaleUpPoint = Point3(scale * 2.03, scale * 2.03, scale * 1.11)
    if animal == 'h' or animal == 'd':
        tubeHeight = -0.87
        scaleUpPoint = Point3(scale * 1.69, scale * 1.69, scale * 0.67)
    tubePosPoints = [Point3(0, 0, tubeHeight), MovieUtil.PNT3_ZERO]
    tubeTracks = []
    tubeTracks.append(FunctionInterval(battle.movie.needRestoreHips))
    for partNum in range(0, hips.getNumPaths()):
        nextPart = hips.getPath(partNum)
        tubeTracks.append(getPropTrack(tubes[partNum], nextPart, tubePosPoints, 3.25, 3.17, scaleUpPoint=scaleUpPoint))

    tubeTracks.append(FunctionInterval(battle.movie.clearRestoreHips))
    toonTrack = getToonTrack(attack, 3.4, ['struggle'], 2.8, ['jump'])
    soundTrack = getSoundTrack('SA_red_tape.mp3', delay=2.9, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack] + tubeTracks)
    else:
        return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack])


def doParadigmShift(attack):
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    hitAtleastOneToon = 0
    for t in targets:
        if t['hp'] > 0:
            hitAtleastOneToon = 1

    damageDelay = 1.95
    dodgeDelay = 0.95
    sprayEffect = BattleParticles.createParticleEffect('ShiftSpray')
    suitName = suit.getStyleName()
    if suitName == 'm':
        sprayEffect.setPos(Point3(-5.2, 4.6, 2.7))
    else:
        if suitName == 'sd':
            sprayEffect.setPos(Point3(-5.2, 4.6, 2.7))
        else:
            sprayEffect.setPos(Point3(0.1, 4.6, 2.7))
    suitTrack = getSuitAnimTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    liftTracks = []
    toonRiseTracks = []
    for t in targets:
        toon = t['toon']
        dmg = t['hp']
        if dmg > 0:
            liftEffect = BattleParticles.createParticleEffect('ShiftLift')
            liftEffect.setPos(toon.getPos(battle))
            liftEffect.setZ(liftEffect.getZ() - 1.3)
            liftTracks.append(getPartTrack(liftEffect, 1.1, 4.1, [liftEffect, battle, 0]))
            shadows = toon.dropShadows
            fakeShadow = MovieUtil.copyProp(shadows[0])

            def showShadows(true, shadows=shadows):
                ivals = []
                for shadow in shadows:
                    if true == 0:
                        ivals.append(FunctionInterval(shadow.hide))
                    else:
                        ivals.append(FunctionInterval(shadow.show))

                return ivals

            x = toon.getX()
            y = toon.getY()
            z = toon.getZ()
            height = 3
            groundPoint = Point3(x, y, z)
            risePoint = Point3(x, y, z + height)
            shakeRight = Point3(x, y + 0.7, z + height)
            shakeLeft = Point3(x, y - 0.7, z + height)
            shakeIvals = []
            shakeIvals.append(WaitInterval(damageDelay + 0.25))
            shakeIvals.extend(showShadows(0))
            shakeIvals.append(LerpPosInterval(toon, 1.1, risePoint))
            for i in range(0, 17):
                shakeIvals.append(LerpPosInterval(toon, 0.03, shakeLeft))
                shakeIvals.append(LerpPosInterval(toon, 0.03, shakeRight))

            shakeIvals.append(LerpPosInterval(toon, 0.1, risePoint))
            shakeIvals.append(LerpPosInterval(toon, 0.1, groundPoint))
            shakeIvals.extend(showShadows(1))
            shadowIvals = []
            shadowIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[fakeShadow]))
            shadowIvals.append(WaitInterval(damageDelay + 0.25))
            shadowIvals.append(FunctionInterval(fakeShadow.hide))
            shadowIvals.append(FunctionInterval(fakeShadow.setScale, extraArgs=[0.27]))
            shadowIvals.append(FunctionInterval(fakeShadow.reparentTo, extraArgs=[toon]))
            shadowIvals.append(FunctionInterval(fakeShadow.setPos, extraArgs=[MovieUtil.PNT3_ZERO]))
            shadowIvals.append(FunctionInterval(fakeShadow.wrtReparentTo, extraArgs=[battle]))
            shadowIvals.append(FunctionInterval(fakeShadow.show))
            shadowIvals.append(LerpScaleInterval(fakeShadow, 0.4, Point3(0.17, 0.17, 0.17)))
            shadowIvals.append(WaitInterval(1.81))
            shadowIvals.append(LerpScaleInterval(fakeShadow, 0.1, Point3(0.27, 0.27, 0.27)))
            shadowIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[fakeShadow]))
            shadowIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[fakeShadow]))
            toonRiseTracks.append(MultiTrack([Track(shakeIvals), Track(shadowIvals)]))

    damageAnims = []
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.9, startTime=2.06))
    damageAnims.append(['slip-backward', 0.01, 0.5])
    dodgeAnims = []
    dodgeAnims.append(['jump', 0.01, 0, 0.6])
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.0, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91])
    toonTracks = getToonTracks(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=2.7)
    if hitAtleastOneToon == 1:
        soundTrack = getSoundTrack('SA_paradigm_shift.mp3', delay=2.1, node=suit)
        return MultiTrack([suitTrack, sprayTrack, soundTrack] + liftTracks + toonTracks + toonRiseTracks)
    else:
        return MultiTrack([suitTrack, sprayTrack] + liftTracks + toonTracks + toonRiseTracks)


def doPowerTrip(attack):
    suit = attack['suit']
    battle = attack['battle']
    centerColor = Vec4(0.1, 0.1, 0.1, 0.4)
    edgeColor = Vec4(0.4, 0.1, 0.9, 0.7)
    powerBar1 = BattleParticles.createParticleEffect(file='powertrip')
    powerBar2 = BattleParticles.createParticleEffect(file='powertrip2')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-60, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(60, 0, 0)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)
    suitName = suit.getStyleName()
    if suitName == 'mh':
        waterfallEffect.setPos(0, 4, 3.6)
    suitTrack = getSuitAnimTrack(attack)

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Track([(1.0, FunctionInterval(battle.movie.needRestoreParticleEffect, extraArgs=[effect])), FunctionInterval(effect.start, extraArgs=[suit]), WaitInterval(0.4), LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)), LerpFunctionInterval(effect.setAlphaScale, fromData=1, toData=0, duration=0.4), FunctionInterval(effect.cleanup), FunctionInterval(battle.movie.clearRestoreParticleEffect, extraArgs=[effect])])
        return partTrack

    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 1.3, [
     waterfallEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.8, ['slip-forward'], 1.29, ['jump'])
    return MultiTrack([suitTrack, partTrack1, partTrack2, waterfallTrack] + toonTracks)


def getThrowEndPoint(suit, toon, battle, whichBounce):
    pnt = toon.getPos(toon)
    if whichBounce == 'one':
        pnt.setY(pnt[1] + 8)
    else:
        if whichBounce == 'two':
            pnt.setY(pnt[1] + 5)
        else:
            if whichBounce == 'threeHit':
                pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3)
            else:
                if whichBounce == 'threeMiss':
                    pass
                else:
                    if whichBounce == 'four':
                        pnt.setY(pnt[1] - 5)
    return Point3(pnt)


def doBounceCheck(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    battle = attack['battle']
    toon = target['toon']
    dmg = target['hp']
    hitSuit = dmg > 0
    check = globalPropPool.getProp('bounced-check')
    checkPosPoints = [MovieUtil.PNT3_ZERO, Point3(-176, 89, 11)]
    bounce1Point = lambda suit=suit, toon=toon, battle=battle: getThrowEndPoint(suit, toon, battle, 'one')
    bounce2Point = lambda suit=suit, toon=toon, battle=battle: getThrowEndPoint(suit, toon, battle, 'two')
    hit3Point = lambda suit=suit, toon=toon, battle=battle: getThrowEndPoint(suit, toon, battle, 'threeHit')
    miss3Point = lambda suit=suit, toon=toon, battle=battle: getThrowEndPoint(suit, toon, battle, 'threeMiss')
    bounce4Point = lambda suit=suit, toon=toon, battle=battle: getThrowEndPoint(suit, toon, battle, 'four')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        throwDelay = 2.5
        dodgeDelay = 4.3
        damageDelay = 5.1
    else:
        if suitType == 'b':
            throwDelay = 1.8
            dodgeDelay = 3.6
            damageDelay = 4.4
        else:
            if suitType == 'c':
                throwDelay = 1.8
                dodgeDelay = 3.6
                damageDelay = 4.4
    suitTrack = getSuitTrack(attack)
    checkIvals = getPropAppearIntervals(check, suit.getRightHand(), checkPosPoints, 1e-05, Point3(8.5, 8.5, 8.5), startScale=MovieUtil.PNT3_ONE)
    checkIvals.append(WaitInterval(throwDelay))
    checkIvals.append(FunctionInterval(check.wrtReparentTo, extraArgs=[toon]))
    checkIvals.append(FunctionInterval(check.setHpr, extraArgs=[Point3(0, -90, 0)]))
    checkIvals.extend(getThrowIvals(check, bounce1Point, duration=0.5, parent=toon))
    checkIvals.extend(getThrowIvals(check, bounce2Point, duration=0.9, parent=toon))
    if hitSuit:
        checkIvals.extend(getThrowIvals(check, hit3Point, duration=0.7, parent=toon))
    else:
        checkIvals.extend(getThrowIvals(check, miss3Point, duration=0.7, parent=toon))
        checkIvals.extend(getThrowIvals(check, bounce4Point, duration=0.7, parent=toon))
        checkIvals.append(LerpScaleInterval(check, 0.3, MovieUtil.PNT3_NEARZERO))
    checkIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[check]))
    checkPropTrack = Track(checkIvals)
    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    soundTracks = Track(getSoundTrack('SA_pink_slip.mp3', delay=throwDelay + 0.5, duration=0.6, node=suit), getSoundTrack('SA_pink_slip.mp3', delay=0.4, duration=0.6, node=suit))
    return MultiTrack([suitTrack, checkPropTrack, toonTrack, soundTracks])


def doWatercooler(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    watercooler = globalPropPool.getProp('watercooler')

    def getCoolerSpout(watercooler=watercooler):
        spout = watercooler.find('**/joint-toSpray')
        return spout.getPos(render)

    hitPoint = lambda toon=toon: __toonFacePoint(toon)
    missPoint = lambda prop=watercooler, toon=toon: __toonMissPoint(prop, toon, 0, parent=render)
    hitSprayIvals = MovieUtil.getSprayIntervals(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, hitPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
    missSprayIvals = MovieUtil.getSprayIntervals(battle, Point4(0.75, 0.75, 1.0, 0.8), getCoolerSpout, missPoint, 0.2, 0.2, 0.2, horizScale=0.3, vertScale=0.3)
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.48, 0.11, -0.92), Point3(37.03, -10.62, -79.21)]
    propIvals = [WaitInterval(1.01), FunctionInterval(__showProp, extraArgs=[watercooler, suit.getLeftHand(), posPoints[0], posPoints[1]]), LerpScaleInterval(watercooler, 0.5, Point3(1.15, 1.15, 1.15)), WaitInterval(1.6)]
    if dmg > 0:
        propIvals += hitSprayIvals
    else:
        propIvals += missSprayIvals
    propIvals += [WaitInterval(0.01), LerpScaleInterval(watercooler, 0.5, MovieUtil.PNT3_NEARZERO), FunctionInterval(MovieUtil.removeProp, extraArgs=[watercooler])]
    propTrack = Track(propIvals)
    splashTrack = []
    if dmg > 0:

        def prepSplash(splash, targetPoint):
            splash.reparentTo(render)
            splash.setPos(targetPoint)
            scale = splash.getScale()
            splash.setBillboardPointWorld()
            splash.setScale(scale)

        splash = globalPropPool.getProp('splash-from-splat')
        splash.setColor(0.75, 0.75, 1, 0.8)
        splash.setScale(0.3)
        splashIvals = [FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[splash]), (3.2, FunctionInterval(prepSplash, extraArgs=[splash, __toonFacePoint(toon)])), ActorInterval(splash, 'splash-from-splat'), FunctionInterval(MovieUtil.removeProp, extraArgs=[splash]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[splash])]
        splashTrack.append(Track(splashIvals))
    toonTrack = getToonTrack(attack, suitTrack.getDuration() - 1.5, ['cringe'], 2.4, ['sidestep'])
    soundTrack = Track([WaitInterval(1.1), SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_appear_only.mp3'), node=suit), WaitInterval(0.4), SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_spray_only.mp3'), node=suit)])
    return MultiTrack([suitTrack, toonTrack, propTrack, soundTrack] + splashTrack)


def doFired(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameEffect = BattleParticles.createParticleEffect('FiredFlame')
    flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
    BattleParticles.setEffectTexture(flameEffect, 'fire')
    BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex', color=Vec4(200, 200, 200, 1))
    baseFlameSmall = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameSmall = BattleParticles.createParticleEffect('FiredFlame')
    flecksSmall = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(baseFlameSmall, 'fire')
    BattleParticles.setEffectTexture(flameSmall, 'fire')
    BattleParticles.setEffectTexture(flecksSmall, 'roll-o-dex', color=Vec4(200, 200, 200, 1))
    baseFlameSmall.setScale(0.7)
    flameSmall.setScale(0.7)
    flecksSmall.setScale(0.7)
    suitTrack = getSuitTrack(attack)
    baseFlameTrack = getPartTrack(baseFlameEffect, 1.0, 1.9, [
     baseFlameEffect, toon, 0])
    flameTrack = getPartTrack(flameEffect, 1.0, 1.9, [flameEffect, toon, 0])
    flecksTrack = getPartTrack(flecksEffect, 1.8, 1.1, [flecksEffect, toon, 0])
    baseFlameSmallTrack = getPartTrack(baseFlameSmall, 1.0, 1.9, [
     baseFlameSmall, toon, 0])
    flameSmallTrack = getPartTrack(flameSmall, 1.0, 1.9, [flameSmall, toon, 0])
    flecksSmallTrack = getPartTrack(flecksSmall, 1.8, 1.1, [flecksSmall, toon, 0])

    def changeColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.setColorScale, extraArgs=[Vec4(0, 0, 0, 1)]))

        return ivals

    def resetColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.clearColorScale))

        return ivals

    if dmg > 0:
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()
        colorIvals = []
        colorIvals.append(WaitInterval(2.0))
        colorIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        colorIvals.extend(changeColor(headParts))
        colorIvals.extend(changeColor(torsoParts))
        colorIvals.extend(changeColor(legsParts))
        colorIvals.append(WaitInterval(3.5))
        colorIvals.extend(resetColor(headParts))
        colorIvals.extend(resetColor(torsoParts))
        colorIvals.extend(resetColor(legsParts))
        colorIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        colorTrack = Track(colorIvals)
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.7, 0.62])
    damageAnims.append(['slip-forward', 1e-05, 0.4, 1.2])
    damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.8, startTime=1.2))
    toonTrack = getToonTrack(attack, damageDelay=1.5, splicedDamageAnims=damageAnims, dodgeDelay=0.3, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_hot_air.mp3', delay=1.0, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, baseFlameTrack, flameTrack, flecksTrack, toonTrack, colorTrack, soundTrack])
    else:
        return MultiTrack([suitTrack, baseFlameSmallTrack, flameSmallTrack, flecksSmallTrack, toonTrack, soundTrack])


def doAudit(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-two', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-three', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-four', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-mult', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitName = attack['suitName']
    if suitName == 'nc':
        calcPosPoints = [
         Point3(-0.15, 0.37, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [
         Point3(0.35, 0.52, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 0.9, ['duck'], showMissedExtraTime=2.2)
    soundTrack = getSoundTrack('SA_audit.mp3', delay=1.9, node=suit)
    return MultiTrack([suitTrack, toonTrack, calcPropTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5])


def doCalculate(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-plus', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-three', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-div', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitName = attack['suitName']
    if suitName == 'nc':
        calcPosPoints = [
         Point3(-0.15, 0.37, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [
         Point3(0.35, 0.52, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])
    return MultiTrack([suitTrack, toonTrack, calcPropTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5])


def doTabulate(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-plus', color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-minus', color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult', color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-div', color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-one', color=Vec4(0, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])
    suitName = attack['suitName']
    if suitName == 'nc':
        calcPosPoints = [
         Point3(-0.15, 0.37, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [
         Point3(0.35, 0.52, 0.03), Point3(2.03, -6.34, 6.01)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)
    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 1e-06, calcDuration, scaleUpPoint=scaleUpPoint, anim=1, propName='calculator', animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])
    return MultiTrack([suitTrack, toonTrack, calcPropTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5])


def doCrunch(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    throwDuration = 3.03
    suitTrack = getSuitTrack(attack)
    numberNames = ['one', 'two', 'three', 'four', 'five', 'six']
    BattleParticles.loadParticles()
    numberSpill1 = BattleParticles.createParticleEffect(file='numberSpill')
    numberSpill2 = BattleParticles.createParticleEffect(file='numberSpill')
    spillTexture1 = whrandom.choice(numberNames)
    spillTexture2 = whrandom.choice(numberNames)
    BattleParticles.setEffectTexture(numberSpill1, 'audit-' + spillTexture1)
    BattleParticles.setEffectTexture(numberSpill2, 'audit-' + spillTexture2)
    numberSpillTrack1 = getPartTrack(numberSpill1, 1.1, 2.2, [
     numberSpill1, suit, 0])
    numberSpillTrack2 = getPartTrack(numberSpill2, 1.5, 1.0, [
     numberSpill2, suit, 0])
    numberSprayTracks = []
    numOfNumbers = whrandom.randint(5, 9)
    for i in range(0, numOfNumbers - 1):
        nextSpray = BattleParticles.createParticleEffect(file='numberSpray')
        nextTexture = whrandom.choice(numberNames)
        BattleParticles.setEffectTexture(nextSpray, 'audit-' + nextTexture)
        nextStartTime = whrandom.random() * 0.6 + throwDuration
        nextDuration = whrandom.random() * 0.4 + 1.4
        nextSprayTrack = getPartTrack(nextSpray, nextStartTime, nextDuration, [
         nextSpray, suit, 0])
        numberSprayTracks.append(nextSprayTrack)

    numbers = []
    numberTracks = []
    for i in range(0, numOfNumbers):
        texture = whrandom.choice(numberNames)
        next = MovieUtil.copyProp(BattleParticles.getParticle('audit-' + texture))
        next.reparentTo(suit.getRightHand())
        next.setScale(0.01, 0.01, 0.01)
        next.setColor(Vec4(0.0, 0.0, 0.0, 1.0))
        next.setPos(whrandom.random() * 0.6 - 0.3, whrandom.random() * 0.6 - 0.3, whrandom.random() * 0.6 - 0.3)
        next.setHpr(Point3(-77.47, 74.05, 15.52))
        numberTrack = Track([WaitInterval(0.9), LerpScaleInterval(next, 0.6, MovieUtil.PNT3_ONE), WaitInterval(1.7), FunctionInterval(MovieUtil.removeProp, extraArgs=[next])])
        numberTracks.append(numberTrack)

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.14, 0.28])
    damageAnims.append(['cringe', 0.01, 0.16, 0.3])
    damageAnims.append(['cringe', 0.01, 0.13, 0.22])
    damageAnims.append(['slip-forward', 0.01, 0.6])
    toonTrack = getToonTrack(attack, damageDelay=4.7, splicedDamageAnims=damageAnims, dodgeDelay=3.6, dodgeAnimNames=['sidestep'])
    return MultiTrack([suitTrack, toonTrack, numberSpillTrack1, numberSpillTrack2] + numberTracks + numberSprayTracks)


def doLiquidate(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    BattleParticles.loadParticles()
    rainEffect = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
    cloud = globalPropPool.getProp('stormcloud')
    suitType = getSuitBodyType(attack['suitName'])
    if suitType == 'a':
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.45
    else:
        if suitType == 'b':
            partDelay = 0.2
            damageDelay = 3.5
            dodgeDelay = 2.45
        else:
            if suitType == 'c':
                partDelay = 0.2
                damageDelay = 3.5
                dodgeDelay = 2.45
    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), Point3(180, 0, 0)]
    cloudIvals = []
    cloudIvals.append(FunctionInterval(cloud.pose, extraArgs=['stormcloud', 0]))
    cloudIvals.extend(getPropAppearIntervals(cloud, suit, cloudPosPoints, 1e-06, Point3(3, 3, 3), scaleUpTime=0.7))
    cloudIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(cloud.wrtReparentTo, extraArgs=[render]))
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2] + 3)
    cloudIvals.append(WaitInterval(1.1))
    cloudIvals.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    cloudIvals.append(WaitInterval(partDelay))
    pivals = []
    pivals.append(Track([ParticleInterval(rainEffect, cloud, worldRelative=0, duration=2.1)]))
    pivals.append(Track([(0.1, ParticleInterval(rainEffect2, cloud, worldRelative=0, duration=2.0))]))
    pivals.append(Track([(0.1, ParticleInterval(rainEffect3, cloud, worldRelative=0, duration=2.0))]))
    pivals.append(Track([ActorInterval(cloud, 'stormcloud', startTime=3, duration=0.1), ActorInterval(cloud, 'stormcloud', startTime=1, duration=2.3)]))
    cloudIvals.append(MultiTrack(pivals))
    cloudIvals.append(WaitInterval(0.4))
    cloudIvals.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
    cloudIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[cloud]))
    cloudIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[cloud]))
    cloudPropTrack = Track(cloudIvals)
    damageAnims = [
     [
      'melt'], ['jump', 1.5, 0.4]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_liquidate.mp3', delay=2.0, node=suit)
    if dmg > 0:
        puddle = globalPropPool.getProp('quicksand')
        puddle.setColor(Vec4(0.0, 0.0, 1.0, 1))
        puddle.setHpr(Point3(120, 0, 0))
        puddle.setScale(0.01)
        puddleTrack = Track([FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[puddle]), WaitInterval(damageDelay - 0.7), FunctionInterval(puddle.reparentTo, extraArgs=[battle]), FunctionInterval(puddle.setPos, extraArgs=[toon.getPos(battle)]), LerpScaleInterval(puddle, 1.7, Point3(1.7, 1.7, 1.7), startScale=MovieUtil.PNT3_NEARZERO), WaitInterval(3.2), LerpFunctionInterval(puddle.setAlphaScale, fromData=1, toData=0, duration=0.8), FunctionInterval(MovieUtil.removeProp, extraArgs=[puddle]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[puddle])])
        return MultiTrack([suitTrack, toonTrack, cloudPropTrack, soundTrack, puddleTrack])
    else:
        return MultiTrack([suitTrack, toonTrack, cloudPropTrack, soundTrack])


def doMarketCrash(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    suitDelay = 1.32
    propDelay = 0.6
    throwDuration = 1.5
    paper = globalPropPool.getProp('newspaper')
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.07, 0.17, -0.13), Point3(-169.7, -36.03, -39.29)]
    paperIvals = getPropAppearIntervals(paper, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=0.5)
    paperIvals.append(WaitInterval(suitDelay))
    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.2)
    hitPoint.setY(hitPoint.getY() + 1.5)
    if dmg > 0:
        hitPoint.setZ(hitPoint.getZ() + 1.1)
    movePoint = Point3(hitPoint.getX(), hitPoint.getY() - 1.8, hitPoint.getZ() + 0.2)
    paperIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[paper]))
    paperIvals.append(FunctionInterval(paper.wrtReparentTo, extraArgs=[battle]))
    paperIvals.extend(getThrowIvals(paper, hitPoint, duration=throwDuration, parent=battle))
    paperIvals.append(WaitInterval(0.6))
    paperIvals.append(LerpPosInterval(paper, 0.4, movePoint))
    paperTrack = Track(paperIvals)
    spinTrack = Track([WaitInterval(propDelay + suitDelay + 0.2), LerpHprInterval(paper, throwDuration, Point3(-360, 0, 0))])
    sizeTrack = Track([WaitInterval(propDelay + suitDelay + 0.2), LerpScaleInterval(paper, throwDuration, Point3(6, 6, 6)), WaitInterval(0.95), LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO)])
    propTrack = Track([MultiTrack([paperTrack, spinTrack, sizeTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[paper]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[paper])])
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.21, 0.08])
    damageAnims.append(['slip-forward', 0.01, 0.6, 0.85])
    damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.95, startTime=1.2))
    damageAnims.append(['slip-forward', 0.01, 1.51])
    toonTrack = getToonTrack(attack, damageDelay=3.8, splicedDamageAnims=damageAnims, dodgeDelay=2.4, dodgeAnimNames=['sidestep'], showDamageExtraTime=0.4, showMissedExtraTime=1.3)
    return MultiTrack([suitTrack, toonTrack, propTrack])


def doBite(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    teeth = globalPropPool.getProp('teeth')
    propDelay = 0.8
    propScaleUpTime = 0.5
    suitDelay = 1.73
    throwDelay = propDelay + propScaleUpTime + suitDelay
    throwDuration = 0.4
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.05, 0.41, -0.54), Point3(0.0, -5.71, -51.34)]
    teethIvals = getPropAppearIntervals(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime)
    teethIvals.append(WaitInterval(suitDelay))
    teethIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[teeth]))
    teethIvals.append(FunctionInterval(teeth.wrtReparentTo, extraArgs=[battle]))
    if dmg > 0:
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        toonHeight = z + toon.getHeight()
        flyPoint = Point3(x, y + 2.7, toonHeight * 0.8)
        teethIvals.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethIvals.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
        teethIvals.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
        teethIvals.append(WaitInterval(0.2))
        teethIvals.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.2, toonHeight * 0.9)))
        teethIvals.append(WaitInterval(0.4))
        scaleTrack = Track([(throwDelay, LerpScaleInterval(teeth, throwDuration, Point3(8, 8, 8))), WaitInterval(0.9), LerpScaleInterval(teeth, 0.2, Point3(14, 14, 14)), WaitInterval(1.2), LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)])
        hprTrack = Track([(throwDelay, LerpHprInterval(teeth, 0.3, Point3(180, 0, 0))), WaitInterval(0.2), LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)), WaitInterval(0.6), LerpHprInterval(teeth, 0.1, Point3(180, -75, 0), startHpr=Point3(180, -35, 0))])
        animTrack = Track([(throwDelay, ActorInterval(teeth, 'teeth', duration=throwDuration)), ActorInterval(teeth, 'teeth', duration=0.3), FunctionInterval(teeth.pose, extraArgs=['teeth', 1]), WaitInterval(0.7), ActorInterval(teeth, 'teeth', duration=0.9)])
        propTrack = Track([MultiTrack([Track(teethIvals), scaleTrack, hprTrack, animTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[teeth]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[teeth])])
    else:
        flyPoint = __toonFacePoint(toon, parent=battle)
        flyPoint.setY(flyPoint.getY() - 7.1)
        teethIvals.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethIvals.append(FunctionInterval(MovieUtil.removeProp, extraArgs=[teeth]))
        teethIvals.append(FunctionInterval(battle.movie.clearRenderProp, extraArgs=[teeth]))
        propTrack = Track(teethIvals)
    damageAnims = [['cringe', 0.01, 0.7, 1.2], ['conked', 0.01, 0.2, 2.1], ['conked', 0.01, 3.2]]
    dodgeAnims = [
     [
      'cringe', 0.01, 0.7, 0.2], ['duck', 0.01, 1.6]]
    toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.9, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=2.4)
    return MultiTrack([suitTrack, toonTrack, propTrack])


def doChomp(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    teeth = globalPropPool.getProp('teeth')
    propDelay = 0.8
    propScaleUpTime = 0.5
    suitDelay = 1.73
    throwDelay = propDelay + propScaleUpTime + suitDelay
    throwDuration = 0.4
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.05, 0.41, -0.54), Point3(0.0, -5.71, -51.34)]
    teethIvals = getPropAppearIntervals(teeth, suit.getRightHand(), posPoints, propDelay, Point3(3, 3, 3), scaleUpTime=propScaleUpTime)
    teethIvals.append(WaitInterval(suitDelay))
    teethIvals.append(FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[teeth]))
    teethIvals.append(FunctionInterval(teeth.wrtReparentTo, extraArgs=[battle]))
    if dmg > 0:
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        toonHeight = z + toon.getHeight()
        flyPoint = Point3(x, y + 2.7, toonHeight * 0.7)
        teethIvals.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethIvals.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y + 3.2, toonHeight * 0.7)))
        teethIvals.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y + 4.7, toonHeight * 0.5)))
        teethIvals.append(WaitInterval(0.2))
        teethIvals.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y, toonHeight + 3)))
        teethIvals.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 1.2, toonHeight * 0.7)))
        teethIvals.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y - 0.7, toonHeight * 0.4)))
        teethIvals.append(WaitInterval(0.4))
        scaleTrack = Track([(throwDelay, LerpScaleInterval(teeth, throwDuration, Point3(6, 6, 6))), WaitInterval(0.9), LerpScaleInterval(teeth, 0.2, Point3(10, 10, 10)), WaitInterval(1.2), LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO)])
        hprTrack = Track([(throwDelay, LerpHprInterval(teeth, 0.3, Point3(180, 0, 0))), WaitInterval(0.2), LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)), WaitInterval(0.6), LerpHprInterval(teeth, 0.1, Point3(0, -35, 0), startHpr=Point3(180, -35, 0))])
        animTrack = Track([(throwDelay, ActorInterval(teeth, 'teeth', duration=throwDuration)), ActorInterval(teeth, 'teeth', duration=0.3), FunctionInterval(teeth.pose, extraArgs=['teeth', 1]), WaitInterval(0.7), ActorInterval(teeth, 'teeth', duration=0.9)])
        propTrack = Track([MultiTrack([Track(teethIvals), scaleTrack, hprTrack, animTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[teeth]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[teeth])])
    else:
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        z = z + 0.2
        flyPoint = Point3(x, y - 2.1, z)
        teethIvals.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethIvals.append(WaitInterval(0.2))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.5, y - 2.5, z)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.0, y - 3.0, z + 0.4)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 1.3, y - 3.6, z)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.9, y - 3.1, z + 0.4)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x + 0.3, y - 2.6, z)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.1, y - 2.2, z + 0.4)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.4, y - 1.9, z)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.7, y - 2.1, z + 0.4)))
        teethIvals.append(LerpPosInterval(teeth, 0.2, pos=Point3(x - 0.8, y - 2.3, z)))
        teethIvals.append(LerpScaleInterval(teeth, 0.6, MovieUtil.PNT3_NEARZERO))
        hprTrack = Track([(throwDelay, LerpHprInterval(teeth, 0.3, Point3(180, 0, 0))), WaitInterval(0.5), LerpHprInterval(teeth, 0.4, Point3(80, 0, 0), startHpr=Point3(180, 0, 0)), LerpHprInterval(teeth, 0.8, Point3(-10, 0, 0), startHpr=Point3(80, 0, 0))])
        animTrack = Track([(throwDelay, ActorInterval(teeth, 'teeth', duration=3.6))])
        propTrack = Track([MultiTrack([Track(teethIvals), hprTrack, animTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[teeth]), FunctionInterval(battle.movie.clearRenderProp, extraArgs=[teeth])])
    damageAnims = [
     [
      'cringe', 0.01, 0.7, 1.2], ['spit', 0.01, 2.95, 1.47], ['spit', 0.01, 4.42, 0.07], ['spit', 0.08, 4.49, -0.07], ['spit', 0.08, 4.42, 0.07], ['spit', 0.08, 4.49, -0.07], ['spit', 0.08, 4.42, 0.07], ['spit', 0.08, 4.49, -0.07], ['spit', 0.01, 4.42]]
    dodgeAnims = [
     [
      'jump', 0.01, 0.01]]
    toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims, dodgeDelay=2.75, splicedDodgeAnims=dodgeAnims, showDamageExtraTime=1.4)
    return MultiTrack([suitTrack, toonTrack, propTrack])


def doEvictionNotice(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    paper = globalPropPool.getProp('shredder-paper')
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.04, 0.15, -1.38), Point3(6.34, -14.62, -18.02)]
    paperIvals = getPropAppearIntervals(paper, suit.getRightHand(), posPoints, 0.8, MovieUtil.PNT3_ONE, scaleUpTime=0.5)
    paperIvals.append(WaitInterval(1.73))
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.4)
    missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    paperIvals.extend(getPropThrowIntervals(attack, paper, [hitPoint], [
     missPoint], parent=battle))
    propTrack = Track(paperIvals)
    toonTrack = getToonTrack(attack, 3.4, ['conked'], 2.8, ['jump'])
    return MultiTrack([suitTrack, toonTrack, propTrack])


def doWithdrawal(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Withdrawal')
    BattleParticles.setEffectTexture(particleEffect, 'snow-particle')
    suitTrack = getSuitAnimTrack(attack)
    partTrack = getPartTrack(particleEffect, 1e-05, suitTrack.getDuration() + 1.2, [
     particleEffect, suit, 0])
    toonTrack = getToonTrack(attack, 1.2, ['cringe'], 0.2, splicedDodgeAnims=[['duck', 1e-05, 0.8]], showMissedExtraTime=0.8)
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()

    def changeColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.setColorScale, extraArgs=[Vec4(0, 0, 0, 1)]))

        return Track(ivals)

    def resetColor(parts):
        ivals = []
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            ivals.append(FunctionInterval(nextPart.clearColorScale))

        return ivals

    soundTrack = getSoundTrack('SA_withdrawl.mp3', delay=1.4, node=suit)
    if dmg > 0:
        colorIvals = []
        colorIvals.append(WaitInterval(1.6))
        colorIvals.append(FunctionInterval(battle.movie.needRestoreColor))
        colorIvals.append(MultiTrack([changeColor(headParts), changeColor(torsoParts), changeColor(legsParts)]))
        colorIvals.append(WaitInterval(2.9))
        colorIvals.extend(resetColor(headParts))
        colorIvals.extend(resetColor(torsoParts))
        colorIvals.extend(resetColor(legsParts))
        colorIvals.append(FunctionInterval(battle.movie.clearRestoreColor))
        colorTrack = Track(colorIvals)
        return MultiTrack([suitTrack, partTrack, toonTrack, soundTrack, colorTrack])
    else:
        return MultiTrack([suitTrack, partTrack, toonTrack, soundTrack])


def doJargon(attack):
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect4 = BattleParticles.createParticleEffect(file='jargonSpray')
    BattleParticles.setEffectTexture(particleEffect, 'jargon-brow', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'jargon-deep', color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'jargon-hoop', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'jargon-ipo', color=Vec4(0, 0, 0, 1))
    damageDelay = 2.2
    dodgeDelay = 1.5
    partDelay = 1.1
    partInterval = 1.2
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay + partInterval * 0, 2, [
     particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay + partInterval * 1, 2, [
     particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, partDelay + partInterval * 2, 2, [
     particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, partDelay + partInterval * 3, 1.0, [
     particleEffect4, suit, 0])
    damageAnims = []
    damageAnims.append(['conked', 0.0001, 0, 0.4])
    damageAnims.append(['conked', 0.0001, 2.7, 0.85])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.66])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.86])
    damageAnims.append(['conked', 0.0001, 0.4, 0.14])
    damageAnims.append(['conked', 0.0001, 0.4, 0.14])
    damageAnims.append(['conked', 0.0001, 0.4])
    dodgeAnims = [['duck', 0.0001, 1.2], ['duck', 0.0001, 1.3]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.6, showDamageExtraTime=0.7)
    soundTrack = getSoundTrack('SA_jargon.mp3', delay=2.1, node=suit)
    return MultiTrack([suitTrack, toonTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4])


def doMumboJumbo(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect4 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect5 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    BattleParticles.setEffectTexture(particleEffect, 'mumbojumbo-boiler', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'mumbojumbo-creative', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'mumbojumbo-deben', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'mumbojumbo-high', color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect5, 'mumbojumbo-iron', color=Vec4(1, 0, 0, 1))
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.5, 2, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.5, 2, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 3.3, 1.7, [particleEffect3, toon, 0])
    partTrack4 = getPartTrack(particleEffect4, 3.3, 1.7, [particleEffect4, toon, 0])
    partTrack5 = getPartTrack(particleEffect5, 3.3, 1.7, [particleEffect5, toon, 0])
    toonTrack = getToonTrack(attack, 3.2, ['cringe'], 2.2, ['sidestep'])
    soundTrack = getSoundTrack('SA_mumbo_jumbo.mp3', delay=2.5, node=suit)
    if dmg > 0:
        return MultiTrack([suitTrack, toonTrack, soundTrack, partTrack, partTrack2, partTrack3, partTrack4, partTrack5])
    else:
        return MultiTrack([suitTrack, toonTrack, soundTrack, partTrack, partTrack2])


def doGuiltTrip(attack):
    suit = attack['suit']
    battle = attack['battle']
    centerColor = Vec4(1.0, 0.2, 0.2, 0.9)
    edgeColor = Vec4(0.9, 0.9, 0.9, 0.4)
    powerBar1 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar2 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-90, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(90, 0, 0)
    powerBar1.setScale(5)
    powerBar2.setScale(5)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)
    suitTrack = getSuitAnimTrack(attack)

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Track([(0.7, FunctionInterval(battle.movie.needRestoreParticleEffect, extraArgs=[effect])), FunctionInterval(effect.start, extraArgs=[suit]), WaitInterval(0.4), LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)), LerpFunctionInterval(effect.setAlphaScale, fromData=1, toData=0, duration=0.4), FunctionInterval(effect.cleanup), FunctionInterval(battle.movie.clearRestoreParticleEffect, extraArgs=[effect])])
        return partTrack

    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 0.6, [
     waterfallEffect, suit, 0])
    toonTracks = getToonTracks(attack, 1.5, ['slip-forward'], 0.86, ['jump'])
    soundTrack = getSoundTrack('SA_guilt_trip.mp3', delay=1.1, node=suit)
    return MultiTrack([suitTrack, partTrack1, partTrack2, soundTrack, waterfallTrack] + toonTracks)


def doRestrainingOrder(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    paper = globalPropPool.getProp('shredder-paper')
    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(-0.04, 0.15, -1.38), Point3(6.34, -14.62, -18.02)]
    paperIvals = getPropAppearIntervals(paper, suit.getRightHand(), posPoints, 0.8, MovieUtil.PNT3_ONE, scaleUpTime=0.5)
    paperIvals.append(WaitInterval(1.73))
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.4)
    missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    paperIvals.extend(getPropThrowIntervals(attack, paper, [hitPoint], [
     missPoint], parent=battle))
    propTrack = Track(paperIvals)
    damageAnims = [
     [
      'conked', 0.01, 0.3, 0.2], ['struggle', 0.01, 0.2]]
    toonTrack = getToonTrack(attack, damageDelay=3.4, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['sidestep'])
    if dmg > 0:
        restraintCloud = BattleParticles.createParticleEffect(file='restrainingOrderCloud')
        restraintCloud.setPos(hitPoint.getX(), hitPoint.getY() + 0.5, hitPoint.getZ())
        cloudTrack = getPartTrack(restraintCloud, 3.5, 0.2, [restraintCloud, battle, 0])
        return MultiTrack([suitTrack, cloudTrack, toonTrack, propTrack])
    else:
        return MultiTrack([suitTrack, toonTrack, propTrack])


def doSpin(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 1.7
    sprayEffect = BattleParticles.createParticleEffect(file='spinSpray')
    spinEffect1 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect2 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect3 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect1.reparentTo(toon)
    spinEffect2.reparentTo(toon)
    spinEffect3.reparentTo(toon)
    height1 = toon.getHeight() * (whrandom.random() * 0.2 + 0.7)
    height2 = toon.getHeight() * (whrandom.random() * 0.2 + 0.4)
    height3 = toon.getHeight() * (whrandom.random() * 0.2 + 0.1)
    spinEffect1.setPos(Point3(0, -1.3, height1))
    spinEffect1.setHpr(Point3(0, 50, whrandom.random() * 10 + 85))
    spinEffect2.setPos(Point3(0, -1.3, height2))
    spinEffect2.setHpr(Point3(0, 50, whrandom.random() * 10 + 85))
    spinEffect3.setPos(Point3(0, -1.3, height3))
    spinEffect3.setHpr(Point3(0, 50, whrandom.random() * 10 + 85))
    spinEffect1.wrtReparentTo(battle)
    spinEffect2.wrtReparentTo(battle)
    spinEffect3.wrtReparentTo(battle)
    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    spinTrack1 = getPartTrack(spinEffect1, 2.1, 3.9, [spinEffect1, battle, 0])
    spinTrack2 = getPartTrack(spinEffect2, 2.1, 3.9, [spinEffect2, battle, 0])
    spinTrack3 = getPartTrack(spinEffect3, 2.1, 3.9, [spinEffect3, battle, 0])
    damageAnims = []
    damageAnims.append(['duck', 0.01, 0.01, 1.1])
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=0.91, dodgeAnimNames=['sidestep'], showDamageExtraTime=2.1, showMissedExtraTime=1.0)
    if dmg > 0:
        toonSpinTrack = Track([WaitInterval(damageDelay + 0.9), LerpHprInterval(toon, 0.7, Point3(-10, 0, 0)), LerpHprInterval(toon, 0.5, Point3(-30, 0, 0)), LerpHprInterval(toon, 0.2, Point3(-60, 0, 0)), LerpHprInterval(toon, 0.7, Point3(-700, 0, 0)), LerpHprInterval(toon, 1.0, Point3(-1310, 0, 0)), LerpHprInterval(toon, 0.4, toon.getHpr()), WaitInterval(0.5)])
        return MultiTrack([suitTrack, sprayTrack, toonTrack, toonSpinTrack, spinTrack1, spinTrack2, spinTrack3])
    else:
        return MultiTrack([suitTrack, sprayTrack, toonTrack])


def doLegalese(attack):
    suit = attack['suit']
    BattleParticles.loadParticles()
    sprayEffect1 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='legaleseSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect1, 'legalese-hc', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'legalese-qpq', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'legalese-vd', color=color)
    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 1.9
    dodgeDelay = 1.1
    suitTrack = getSuitTrack(attack)
    sprayTrack1 = getPartTrack(sprayEffect1, partDelay, partDuration, [
     sprayEffect1, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay + 0.8, partDuration, [
     sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay + 1.6, partDuration, [
     sprayEffect3, suit, 0])
    damageAnims = []
    damageAnims.append(['cringe', 1e-05, 0.3, 0.8])
    damageAnims.append(['cringe', 1e-05, 0.3, 0.8])
    damageAnims.append(['cringe', 1e-05, 0.3])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims, dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'], showMissedExtraTime=0.8)
    return MultiTrack([suitTrack, toonTrack, sprayTrack1, sprayTrack2, sprayTrack3])


def doPeckingOrder(attack):
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    throwDuration = 3.03
    throwDelay = 3.2
    suitTrack = getSuitTrack(attack)
    numBirds = whrandom.randint(4, 7)
    birdTracks = []
    propDelay = 1.5
    for i in range(0, numBirds):
        next = globalPropPool.getProp('bird')
        next.setScale(0.01)
        next.reparentTo(suit.getRightHand())
        next.setPos(whrandom.random() * 0.6 - 0.3, whrandom.random() * 0.6 - 0.3, whrandom.random() * 0.6 - 0.3)
        if dmg > 0:
            hitPoint = Point3(whrandom.random() * 5 - 2.5, whrandom.random() * 2 - 1 - 6, whrandom.random() * 3 - 1.5 + toon.getHeight() - 0.9)
        else:
            hitPoint = Point3(whrandom.random() * 2 - 1, whrandom.random() * 4 - 2 - 15, whrandom.random() * 4 - 2 + 2.2)
        birdTrack = Track([WaitInterval(throwDelay), FunctionInterval(battle.movie.needRestoreRenderProp, extraArgs=[next]), FunctionInterval(next.wrtReparentTo, extraArgs=[battle]), FunctionInterval(next.setHpr, extraArgs=[Point3(90, -20, -40)]), LerpPosInterval(next, 1.1, hitPoint)])
        scaleTrack = Track([WaitInterval(throwDelay), LerpScaleInterval(next, 0.15, Point3(9, 9, 9))])
        birdTracks.append(Track([MultiTrack([birdTrack, scaleTrack]), FunctionInterval(MovieUtil.removeProp, extraArgs=[next])]))

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.14, 0.21])
    damageAnims.append(['cringe', 0.01, 0.14, 0.13])
    damageAnims.append(['cringe', 0.01, 0.43])
    toonTrack = getToonTrack(attack, damageDelay=4.2, splicedDamageAnims=damageAnims, dodgeDelay=2.8, dodgeAnimNames=['sidestep'], showMissedExtraTime=1.1)
    return MultiTrack([suitTrack, toonTrack] + birdTracks)