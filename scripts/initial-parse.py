import argparse
import json
from enum import Enum


class State(Enum):
    TYPE = 1
    MOVE_POWER = 2
    MOVE_TIME = 3
    PP = 4
    DURATION = 5
    RANGE = 6
    DESCRIPTION = 7
    HIGHER_LEVELS = 8


def determain_state(line, state):
    if line.startswith("Type:"):
        return State.TYPE
    elif line.startswith("Move Power:"):
        return State.MOVE_POWER
    elif line.startswith("Move Time:"):
        return State.MOVE_TIME
    elif line.startswith("PP:"):
        return State.PP
    elif line.startswith("Duration:"):
        return State.DURATION
    elif line.startswith("Range:"):
        return State.RANGE
    elif line.startswith("Description:"):
        return State.DESCRIPTION
    elif line.startswith("Higher Levels:"):
        return State.HIGHER_LEVELS
    else:
        return state


def process_file(file_path):
    data = []
    state = None
    with open(file_path, 'r') as file:
        move_object = {}
        last_line = None
        description = ""
        higher_levels = ""
        firstPass = True
        for line in file:
            state = determain_state(line, state)
            if state == State.TYPE:
                if not firstPass:
                    description = description.strip()
                    higher_levels = higher_levels.strip()
                    if description.endswith(last_line):
                        description = description[:-len(last_line)]
                    if higher_levels.endswith(last_line):
                        higher_levels = higher_levels[:-len(last_line)]
                    move_object["description"] = description.strip()
                    if higher_levels:
                        move_object["higherLevels"] = higher_levels.strip()
                    description = ""
                    higher_levels = ""
                    data.append(move_object)
                    move_object = {}
                move_object["name"] = last_line
                move_object["type"] = line.lstrip("Type:").strip()
                firstPass = False
            elif state == State.MOVE_POWER:
                move_object["movePower"] = line.lstrip("Move Power:").strip()
            elif state == State.MOVE_TIME:
                move_object["moveTime"] = line.lstrip("Move Time:").strip()
            elif state == State.PP:
                move_object["pp"] = line.lstrip("PP:").strip()
            elif state == State.DURATION:
                move_object["duration"] = line.lstrip("Duration:").strip()
            elif state == State.RANGE:
                move_object["range"] = line.lstrip("Range:").strip()
            elif state == State.DESCRIPTION:
                if line.startswith("Description:"):
                    description += line[len("Description:"):].strip() + " "
                else:
                    description += line.strip() + " "
            elif state == State.HIGHER_LEVELS:
                if line.startswith("Higher Levels:"):
                    higher_levels += line[len("Higher Levels:"):].strip() + " "
                else:
                    higher_levels += line.strip() + " "
            last_line = line.strip()

        # gotta make sure to finalize the last object too.
        move_object["description"] = description.strip()
        if higher_levels:
            move_object["higherLevels"] = higher_levels.strip()
        data.append(move_object)

    with open("..\\generated\\initial-parse.json", 'w') as output_file:
        json.dump(data, output_file)


def main():
    parser = argparse.ArgumentParser(description='Read a file line by line.')
    parser.add_argument('file_path', help='Path to the file to be read.')

    args = parser.parse_args()
    file_path = args.file_path

    process_file(file_path)


if __name__ == '__main__':
    main()
