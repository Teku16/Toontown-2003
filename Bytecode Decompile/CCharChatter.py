import Localizer
GREETING = 0
COMMENT = 1
GOODBYE = 2
MickeyChatter = Localizer.MickeyChatter
MinnieChatter = Localizer.MinnieChatter
GoofyChatter = Localizer.GoofyChatter
DonaldChatter = Localizer.DonaldChatter

def getChatter(charName):
    if charName == 'Mickey':
        return MickeyChatter
    else:
        if charName == 'Minnie':
            return MinnieChatter
        else:
            if charName == 'Goofy':
                return GoofyChatter
            else:
                if charName == 'Donald':
                    return DonaldChatter
                else:
                    if charName == 'Pluto':
                        return None
    return