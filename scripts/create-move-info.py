import argparse
import json
import re

damageRegex = r'([0-9]+d[0-9]+) (\+ MOVE)?'
savingThrowRegex = r'(?P<mod>(STR|DEX|CON|INT|WIS|CHA)) (?:(saving throw)|(save))'
higherLevelRegex = r'(?P<dice>([0-9]+d[0-9]+)) at level (?P<level>([0-9]+))'


def createBaseDamage(item):
    matches = re.finditer(damageRegex, item["description"])

    for match in matches:
        dice_pattern = match.group(1)
        move_pattern = " " + match.group(2) if match.group(2) else ""
        return dice_pattern+move_pattern


def handleSavingThrows(item):
    matches = re.finditer(savingThrowRegex,
                          item["description"], re.MULTILINE)

    for match in matches:
        mod = match.group("mod")
        return mod


def handleHigherLevels(item):
    matches = re.finditer(higherLevelRegex, item["higherLevels"], re.MULTILINE)

    for match in matches:
        dice = match.group("dice")
        level = match.group("level")
        item[f'@level {level}'] = dice


def process_file(file_path):
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            if len(re.findall(damageRegex, item["description"])) and item["range"] != "Self":
                item["baseDamage"] = createBaseDamage(item)
            if len(re.findall(savingThrowRegex, item["description"])):
                item["savingThrow"] = handleSavingThrows(item)
            if "higherLevels" in item:
                handleHigherLevels(item)

        with open("..\\generated\\damage-parse.json", 'w') as output_file:
            json.dump(json_data, output_file)


def main():
    parser = argparse.ArgumentParser(description='Read a file line by line.')
    parser.add_argument('file_path', help='Path to the file to be read.')

    args = parser.parse_args()
    file_path = args.file_path

    def has_json_extension(file_path):
        # Check if the file has a .json extension
        return file_path.lower().endswith(".json")

    if not has_json_extension(file_path):
        raise Exception("filepath passed in is not a json file")

    process_file(file_path)


if __name__ == '__main__':
    main()
