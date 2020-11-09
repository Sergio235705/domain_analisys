import sys
from file_treatment import FileTreatment

def main():
    if (len(sys.argv) != 3):
        print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("Missing an argument\nUsage: python3 file_annotation.py input.json output.csv")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        return -1

    handler = FileTreatment(sys.argv[1])
    handler.annotate(sys.argv[2])


if __name__ == "__main__":
    main()
