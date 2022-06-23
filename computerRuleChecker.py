''' One-letter-placements are counted as rows '''

from boardKeeper import BOARDSIZE


def conformsBetterRules(situation, attachments):
    for spot in situation:
        if spot in attachments:
            return True     # checks if any of the spots is an attachment location
    return False


def getMainCombo(isRowCombo, spot, occupied, situation):
    ''' Get the spots that correspond to the main combo in order '''
    locations = [spot]
    locator = spot
    if isRowCombo:
        while (((locator + 1) in occupied) or ((locator + 1) in situation)) and (locator % BOARDSIZE != (BOARDSIZE-1)):
            locator += 1
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while ((locator - 1) in occupied) and (locator % BOARDSIZE != 0):
            locator -= 1
            locations.insert(0, locator)
    else:
        while ((locator + BOARDSIZE) in occupied) or ((locator + BOARDSIZE) in situation):
            locator += BOARDSIZE
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while (locator - BOARDSIZE) in occupied:
            locator -= BOARDSIZE
            locations.insert(0, locator)
    return locations


def getSideCombo(isRowCombo, spot, occupied):
    ''' Get the spots that correspond to the side combo in order '''
    locations = [spot]
    locator = spot
    if isRowCombo:
        while (locator + BOARDSIZE) in occupied:
            locator += BOARDSIZE
            locations.append(locator)
        locator = spot
        while (locator - BOARDSIZE) in occupied:
            locator -= BOARDSIZE
            locations.insert(0, locator)
    else:
        while ((locator + 1) in occupied) and (locator % BOARDSIZE != (BOARDSIZE-1)):
            locator += 1
            locations.append(locator)
        locator = spot
        while ((locator - 1) in occupied) and (locator % BOARDSIZE != 0):
            locator -= 1
            locations.insert(0, locator)

    if locations == [spot]:
        return []
    return locations


def getAllCombos(situation, occupied, isRowCombo):
    ''' Gets combos of letters made by a valid placement for a computer '''
    combosMade = []
    mainCombo = getMainCombo(isRowCombo, situation[0], occupied, situation)
    if len(mainCombo) != 1:
        combosMade.append(mainCombo)
    # take note, the main combo comes first
    for spot in situation:
        sideCombo = getSideCombo(isRowCombo, spot, occupied)
        if sideCombo != []:
            combosMade.append(sideCombo)
    if len(combosMade) == 0:
        # for situations where a single letter is played by itself (for avoiding errors)
        combosMade.append(mainCombo)
    return combosMade   # now all of these combos must be checked in the dictionary
