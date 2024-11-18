import argparse
import json
from enum import Enum


class Move(Enum):
    NAME = "name"
    TYPE = "type"
    MOVE_POWER = "movePower"
    MOVE_TIME = "moveTime"
    PP = "pp"
    DURATION = "duration"
    RANGE = "range"
    DESCRIPTION = "description"
    # optional
    HIGHER_LEVELS = "higherLevels"
    # generated (optional)
    SAVING_THROW = "savingThrown"
    BASE_DAMAGE = "baseDamage"
    LEVEL5 = "@level 5"
    LEVEL10 = "@level 10"
    LEVEL17 = "@level 17"


#####################################
############## HELPERS ##############
#####################################


def getHighestMovePower(move):
    movePowers = move['movePower'].split("/")
    keepHighestMovePower = ""
    if len(movePowers) == 1:
        keepHighestMovePower = f'@{{{movePowers[0]}_Mod}}'
    elif len(movePowers) == 2:
        keepHighestMovePower = f'{{@{{{movePowers[0]}_Mod}}, @{{{movePowers[1]}_Mod}}}}kh1'
    elif len(movePowers) == 3:
        keepHighestMovePower = f'{{@{{{movePowers[0]}_Mod}}, @{{{movePowers[1]}_Mod}}, @{{{movePowers[2]}_Mod}}}}kh1'
    else:
        raise Exception(f"Somehow {move['name']} move doesn't have Power")
    return keepHighestMovePower

# Damage: [[?{Choose Damage to Roll |
# baseDamage 1d6, 1d6 + {@{STR_Mod}&#44; @{DEX_Mod}&#125;kh1|
# level5 1d12, 1d12 + {@{STR_Mod}&#44; @{DEX_Mod}&#125;kh1} + @{Electric_STAB}]]


def getHighestMovePowerForDamage(move):
    movePowers = move['movePower'].split("/")
    keepHighestMovePower = ""
    if len(movePowers) == 1:
        keepHighestMovePower = f'@{{{movePowers[0]}_Mod}}'
    elif len(movePowers) == 2:
        keepHighestMovePower = f'{{@{{{movePowers[0]}_Mod}}&#44; @{{{movePowers[1]}_Mod}}&#125;kh1'
    elif len(movePowers) == 3:
        keepHighestMovePower = f'{{@{{{movePowers[0]}_Mod}}&#44; @{{{movePowers[1]}_Mod}}&#44; @{{{movePowers[2]}_Mod}}&#125;kh1'
    else:
        raise Exception(f"Somehow {move['name']} move doesn't have Power")
    return keepHighestMovePower


def getAttackMacro(move):
    return f'[[1d20+{getHighestMovePower(move)}+@{{ProfBonus}}]]'


def getDamageMacro(move):
    addMoveToDamageIfNeeded = ""
    if move["baseDamage"].endswith(" + MOVE"):
        move["baseDamage"] = move["baseDamage"].rstrip(" + MOVE")
        addMoveToDamageIfNeeded = f" + {getHighestMovePowerForDamage(move)}"

    selectableDamage = f'?{{Choose Damage to Roll | baseDamage {move["baseDamage"]}, {move["baseDamage"]}{addMoveToDamageIfNeeded}'
    if "@level 5" in move:
        selectableDamage += f'|level5 {move["@level 5"]}, {move["@level 5"]}{addMoveToDamageIfNeeded}'
    if "@level 10" in move:
        selectableDamage += f'|level10 {move["@level 10"]}, {move["@level 10"]}{addMoveToDamageIfNeeded}'
    if "@level 17" in move:
        selectableDamage += f'|level17 {move["@level 17"]}, {move["@level 17"]}{addMoveToDamageIfNeeded}'
    selectableDamage += "}"
    return f'[[{selectableDamage}+@{{{move["type"]}_STAB}}]] {move["type"]} damage'


def getHigherLevelsIfNeeded(move):
    higherLevels = ''
    if 'higherLevels' in move:
        # only show "Higher levels if @level # are not defined"
        higherLevels = f'\nHigher Levels: {move["higherLevels"]}' if "higherLevels" in move and not (
            '@level 5' in move or '@level 10' in move or '@level 17' in move) else ''
    return higherLevels


def getHigherLevels(move):
    higherLevels = ''
    if 'higherLevels' in move:
        # only show "Higher levels if @level # are not defined"
        higherLevels = f'\nHigher Levels: {move["higherLevels"]}' if "higherLevels" in move else ''
    return higherLevels


def buildFinalMacro(move, attackMacro="", savingThrowMacro="", damageMacro="", higherLevels=""):
    if attackMacro:
        attackMacro = f'Attack: {attackMacro}\n'
    if damageMacro:
        damageMacro = f'Damage: {damageMacro}\n'
    if savingThrowMacro:
        savingThrowMacro = f'Saving Throw: {savingThrowMacro}\n'

    return f'''{move["name"]}
Power: {move["movePower"]}
MoveTime: {move["moveTime"]}
PP: {move["pp"]}
Duration: {move["duration"]}
Range: {move["range"]}
{attackMacro}{savingThrowMacro}{damageMacro}Description: {move["description"]}{higherLevels}'''


def getSavingThrow(move):
    return f'[[8+{getHighestMovePower(move)}+@{{ProfBonus}}]]'

#####################################
############## HANDLERS #############
#####################################


def handleSavingAttack(move):
    savingThrow = getSavingThrow(move)
    damageMacro = getDamageMacro(move)
    higherLevels = getHigherLevelsIfNeeded(move)

    return buildFinalMacro(move, "", savingThrow, damageMacro, higherLevels)


def handleTargettedAttack(move):
    attackMacro = getAttackMacro(move)
    damageMacro = getDamageMacro(move)
    higherLevels = getHigherLevelsIfNeeded(move)

    return buildFinalMacro(move, attackMacro, "", damageMacro, higherLevels)


def handleSavingStatusAttack(move):
    savingThrow = getSavingThrow(move)
    higherLevels = getHigherLevelsIfNeeded(move)

    return buildFinalMacro(move, "", savingThrow, "", higherLevels)


def handleSelfTargetEffects(move):
    higherLevels = getHigherLevels(move)

    return buildFinalMacro(move, "", "", "", higherLevels)


def handleTargettedStatusAttack(move):
    attackMacro = getAttackMacro(move)
    higherLevels = getHigherLevelsIfNeeded(move)

    return buildFinalMacro(move, attackMacro, "", "", higherLevels)


#####################################
############## MAIN #################
#####################################


def process_file(file_path):
    macroList = ""
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        for move in json_data:
            macro = ""
            # is move a saving attack
            if 'savingThrow' in move and 'baseDamage' in move:
                macro = handleSavingAttack(move)
            # targetted attack
            elif 'savingThrow' not in move and 'baseDamage' in move:
                macro = handleTargettedAttack(move)
            # Saving status attacks
            elif 'savingThrow' in move and not 'baseDamage' in move:
                macro = handleSavingStatusAttack(move)
            # Self Target effects
            elif 'savingThrow' not in move and 'baseDamage' not in move and move['range'].startswith("Self"):
                macro = handleSelfTargetEffects(move)
            # targetted status attacks
            elif 'savingThrow' not in move and 'baseDamage' not in move:
                macro = handleTargettedStatusAttack(move)
            else:
                raise Exception(f'{move["name"]} is unhandled')

            macroList += macro + "\n\n" if macro != None else ""

        with open("..\\generated\\final.txt", 'w') as output_file:
            output_file.write(macroList)


def main():
    parser = argparse.ArgumentParser(description='Read a file line by line.')
    parser.add_argument('file_path', help='Path to the file to be read.')

    args = parser.parse_args()
    file_path = args.file_path

    process_file(file_path)


if __name__ == '__main__':
    main()
