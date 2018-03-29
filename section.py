from type import *
from entry import *
from segments import *

class Section:
    """ This class is a generic class for each section in a .wasm file

    Attributes:
        sectionCode : int        =  the 'index' for this section
        sectionSize : int        =  the size in bytes for this section
        numTypes    : int        =  the number of elements in this section
        data        : bytearray  =  the rest of the bytes of this section
    """
    def populate(self, inputBytes):
        """
            this method populates the current section with the necessary info,
            and then returns the remaining unread bytes to be processed later

            = Parameters =
            inputBytes : bytearray = bytes of wasm file with current section

            = Return Value = 
            return     : bytearray = bytes of wasm file without current section
        """

        # one byte for section code
        self.sectionCode = int.from_bytes(inputBytes[0:1], byteorder='little', signed=False)

        # one byte for section size
        self.sectionSize = int.from_bytes(inputBytes[1:2], byteorder='little', signed=False)

        # one byte for the number of types
        self.numTypes    = int.from_bytes(inputBytes[2:3], byteorder='little', signed=False)

        # the rest of the bytes in the current section
        self.data        = inputBytes[3:self.sectionSize+2]

        # return the rest of the bytes to be processed later
        return inputBytes[self.sectionSize+2:]

def makeSectionList(inputBytes):
    """
        this method creates the section list of twelve sections

        = Parameters =
        inputBytes  : bytearray   = all of the bytes in the .wasm file

        = Return Value = 
        sectionList : bytearray[] = an array of sections processed from the 
                                    array of bytes
    """

    # 12 sections according to the spec
    sectionList = [None] * 12

    # loop through all 12 sections and populate each if exists
    for i in range (0, len(sectionList)):
        if (inputBytes != None):
            section    = Section()
            inputBytes = section.populate(inputBytes)
            sectionList[section.sectionCode] = section

    # return the generated sectionList
    return sectionList


class CodeSection(Section):
    """
    Field   Type            Description
    -----------------------------------------------------------
    count   varuint32       count of function bodies to follow
    bodies  function_body*  sequence of Function Bodies
    Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#code-section
    """
    def __init__(self, section, sectionList=None):
        self.count = section.numTypes
        inputBytes = section.data
        functionSection = sectionList[SECTION_IDS['function']]

        # If the function section is missing, then this is an invalid binary.
        if functionSection is None:
            raise ValueError('Missing function section')

        self.bodies = []
        for i in range(self.count):
            self.bodies.append(FunctionBody(inputBytes))
            inputBytes = inputBytes[self.bodies[i].size():]
            print(self.bodies[i].to_str())

class DataSection(Section):
    def __init__(self, section, sectionList=None):
        # TODO
        pass

class ElementSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.numElemSegs = section.numTypes
        self.elementSegs = []
        #Constructs array of type ElementSegment
        for i in range(self.numElemSegs):
            self.elementSegs.append(ElementSegment(inputBytes))
            inputBytes = inputBytes[self.elementSegs[i].size():]

class ExportSection(Section):
    """ This class is a generic class for an export section for wasm

    Attributes:
        exportCount : int           =  the 'index' for this section
        entries     : ExportEntry[] =  the size in bytes for this section
    """
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.exportCount = section.numTypes
        self.entries     = []
        
        for i in range(self.exportCount):
            self.entries.append(ExportEntry(inputBytes))
            inputBytes = inputBytes[self.entries[i].size():]
            print(self.entries[i].to_str())

class FunctionSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        # Defining number of functions
        self.num_functions = section.numTypes
        # Stores list of indicies into type section
        self.function_idx = []
        for i in range(self.num_functions):
            self.function_idx.append(inputBytes[i])
                    
class GlobalSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.count = section.numTypes
        self.globals = []

        for i in range(self.count):
            self.globals.append(GlobalEntry(inputBytes))
            inputBytes = inputBytes[self.globals[i].size():]

class ImportSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.import_count = section.numTypes
        self.entries = []

        # Iterate and instantiate all `n` import entries
        # Use the size of the current entry to get the index of the next function type
        for i in range(self.import_count):
            self.entries.append(ImportEntry(inputBytes))
            inputBytes = inputBytes[self.entries[i].size():]

class MemorySection(Section):
    def __init__(self, section, sectionList=None):
        # TODO
        pass

class StartSection(Section):
    def __init__(self, section, sectionList=None):
        # The start section only contains an index variable that represents 
        # the location of the start function.
        self.index = section.numTypes

class TableSection(Section):
    def __init__(self, section, sectionList=None):
        # TODO
        pass

class TypeSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.func_count = section.numTypes
        self.func_types = []

        # Iterate and instantiate all `n` function types
        # Use the size of the current function types to get the index of the next function type
        for i in range(self.func_count):
            self.func_types.append(FuncType(inputBytes))
            inputBytes = inputBytes[self.func_types[i].size():]
