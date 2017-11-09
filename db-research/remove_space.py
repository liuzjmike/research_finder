import sys


def remove_space(filename):
    with open(filename, 'r') as f:
        for line in f:
            print(','.join([s.strip() for s in line.split(',')]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./remove_spacy.py filename")
    remove_space(sys.argv[1])
