import sys
from section import *
from typesection import *
from importsection import *
from functionsection import *
from tablesection import *
from memorysection import *
from globalsection import *
from exportsection import *
from startsection import *
from elementsection import *
from codesection import *
from datasection import *

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

    # Parse each individual sections
    typeSection = TypeSection(sectionList[1])
    importSection = ImportSection(sectionList[2])
    functionSection = FunctionSection(sectionList[3])
    tableSection = TableSection(sectionList[4])
    memorySection = MemorySection(sectionList[5])
    globalSection = GlobalSection(sectionList[6])
    exportSection = ExportSection(sectionList[7])
    startSection = StartSection(sectionList[8])
    elementSection = ElementSection(sectionList[9])
    codeSection = CodeSection(sectionList[10])
    dataSection = DataSection(sectionList[11])

    print(binary)

# code that's only executed if this file itself is run
if __name__ == '__main__':
    # get the filename
    wasmFileName = sys.argv[1]
    disassemble(wasmFileName)

