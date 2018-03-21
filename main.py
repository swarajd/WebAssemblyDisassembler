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

def parseFile(filename):
    """
        this method reads the file associated with the filename and returns
        an array of bytes

        = Parameters = 
        filename    : str        = the name of the file we want to parse

        = Return Value =
        binaryArray : bytearray  = the array of bytes from the file
    """

    # the file object from opening the file
    wasmFile = open(filename, "rb")

    # the binary array obtained from reading the file stream
    binaryArray = bytearray(wasmFile.read())

    # return the binary array
    return binaryArray

def disassemble(filename):
    """
        this method disassembles the given filename's file

        = Parameters = 
        filename : str = the name of the file we want to disassemble

        = Return Value = 
        NONE
    """

    # read the file and get the byte array
    binary = parseFile(filename)

    # get the magic number
    magic = binary[0:4]

    # get the version number
    version = int.from_bytes(binary[4:8], byteorder='little')

    # generate the section list from the remaining bytes
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

    # disassemble the file
    disassemble(wasmFileName)

