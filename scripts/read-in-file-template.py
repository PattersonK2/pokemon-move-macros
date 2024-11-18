import argparse


def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            print(line.strip())


def main():
    parser = argparse.ArgumentParser(description='Read a file line by line.')
    parser.add_argument('file_path', help='Path to the file to be read.')

    args = parser.parse_args()
    file_path = args.file_path

    process_file(file_path)


if __name__ == '__main__':
    main()
