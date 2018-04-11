import sys

from section import *

# The main section thats may be found in a wasm module.
# The list is in the order of which the sections are found in the module.
SECTION_CLASSES = [
    TypeSection,
    ImportSection,
    FunctionSection,
    TableSection,
    MemorySection,
    GlobalSection,
    ExportSection,
    StartSection,
    ElementSection,
    CodeSection,
    DataSection
]

# The order in which each section is translated into text may not be the same ordering
# in which they appear in the binary format.
TEXT_SECTION_ORDERING = [ 1, 2, 3, 6, 10, 5, 4, 11, 7, 9, 8 ]

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
    wasmFile.close()

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

    output = ''
    for idx, section_class in enumerate(SECTION_CLASSES):
        if sectionList[idx + 1] is not None:
            sectionList[idx + 1] = section_class(sectionList[idx + 1], sectionList)


    for idx in TEXT_SECTION_ORDERING:
        if sectionList[idx] is not None:
            output += sectionList[idx].to_str()

    if len(output) == 0:
        output = '(module)\n'
    else:
        output = '(module\n' + output[:-1] + ')\n'

    return output

# code that's only executed if this file itself is run
if __name__ == '__main__':

    # get the filename
    wasmFileName = sys.argv[1]

    # disassemble the file
    results = disassemble(wasmFileName)
    sys.stdout.write(results)
