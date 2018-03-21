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

        print(vars(self)) #DEBUG

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
    def __init__(self, section):
        # TODO
        pass


class DataSection(Section):
    def __init__(self, section):
        # TODO
        pass

class ElementSection(Section):
    def __init__(self, section):
        # TODO
        pass

class ExportSection(Section):
    def __init__(self, section):
        # TODO
        pass

class FunctionSection(Section):
    def __init__(self, section):
        # TODO
        pass

class GlobalSection(Section):
    def __init__(self, section):
        # TODO
        pass

class ImportSection(Section):
    def __init__(self, section):
        # TODO
        pass

class MemorySection(Section):
    def __init__(self, section):
        # TODO
        pass

class StartSection(Section):
    def __init__(self, section):
        # TODO
        pass

class TableSection(Section):
    def __init__(self, section):
        # TODO
        pass

class TypeSection(Section):
    def __init__(self, section):
        # TODO
        pass