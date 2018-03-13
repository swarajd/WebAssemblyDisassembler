import sys

# parse the file into an array of bytes
def parseFile(filename):
    wasmFile = open(filename, "r+")
    binaryArray = bytearray(wasmFile.read())
    return binaryArray

# our "main"
def disassemble(filename):
    binary = parseFile(filename)
    print(binary)

# code that's only executed if this file itself is run
if __name__ == '__main__':
    # get the filename
    wasmFileName = sys.argv[1]

    disassemble(wasmFileName)