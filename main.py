import sys
from section import *


# parse the file into an array of bytes
def parseFile(filename):
    wasmFile = open(filename, "rb")
    binaryArray = bytearray(wasmFile.read())
    return binaryArray

# our "main"
def disassemble(filename):
    binary = parseFile(filename)
    magic = binary[0:4]
    version = int.from_bytes(binary[4:8], byteorder='little')
    sectionList = makeSectionList(binary[8:])
    print(binary)

# code that's only executed if this file itself is run
if __name__ == '__main__':
    # get the filename
    wasmFileName = sys.argv[1]
    disassemble(wasmFileName)

