from type import *
from entry import *
from segments import *
from constants import *

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
        typeSection = sectionList[SECTION_IDS['type']]
        functionSection = sectionList[SECTION_IDS['function']]

        # If the function section is missing, then this is an invalid binary.
        if functionSection is None:
            raise ValueError('Missing function section')
        elif typeSection is None:
            raise ValueError('Missing type section')

        self.function_sig_idx = functionSection.function_idx
        self.function_signatures = typeSection.func_types

        self.bodies = []
        for i in range(self.count):
            self.bodies.append(FunctionBody(inputBytes, self.count))
            inputBytes = inputBytes[self.bodies[i].size():]

    def to_str(self):
        output = ''
        for i in range(self.count):
            sig_idx = self.function_sig_idx[i]
            signature = self.function_signatures[sig_idx]
            body = self.bodies[i].to_str()[:-1]
            output += '  (func $f{} (type $t{}) {}\n{})\n'.format(i, sig_idx, signature.to_str(named_params=True), body)
        return output

class DataSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.numDataSegs = section.numTypes
        self.dataSegs = []
        #Constructs array of type DataSegment
        for i in range(self.numDataSegs):
            self.dataSegs.append(DataSegment(inputBytes))
            inputBytes = inputBytes[self.dataSegs[i].size():]
            
    def to_str(self):
        output = ''
        for i in self.dataSegs:
            output += f"  (memory (data \"{''.join(chr(x) for x in i.data)}\"))\n"
        return output
        
class ElementSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.numElemSegs = section.numTypes
        self.elementSegs = []
        # Constructs array of type ElementSegment
        for i in range(self.numElemSegs):
            self.elementSegs.append(ElementSegment(inputBytes))
            inputBytes = inputBytes[self.elementSegs[i].size():]

    def to_str(self):
        output = ""
        for i in range(len(self.elementSegs)):
            tmpOutput = f"  (elem (i32.const {self.elementSegs[i].offset[1]})"
            for elem in self.elementSegs[i].elems:
                tmpOutput += f" $f{elem}"
            tmpOutput += ")\n"
            output += tmpOutput
        return output

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

        self.type_section = sectionList[SECTION_IDS['type']]
        if self.type_section is None:
            raise ValueError('Missing type section')

    def to_str(self):
        output = ''
        for i in range(self.exportCount):
            entry = self.entries[i]
            output += '  (export "{}" (func $f{}))\n'.format(entry.exportNameStr, entry.kindType)
        return output

class FunctionSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        # Defining number of functions
        self.num_functions = section.numTypes
        # Stores list of indicies into type section
        self.function_idx = []
        for i in range(self.num_functions):
            self.function_idx.append(inputBytes[i])

    def to_str(self):
        return ''
                    
class GlobalSection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.count = section.numTypes
        self.globals = []

        for i in range(self.count):
            self.globals.append(GlobalEntry(inputBytes))
            inputBytes = inputBytes[self.globals[i].size():]

    def to_str(self):
        output = ''

        # (global $g0 (mut i32) (i32.const 0))
        for i in range(self.count):
            entry = self.globals[i]
            mutability = ''
            if entry.type.mutability == 1:
                mutability = ' (mut {}) '.format(entry.type.content_type)
            output += '  (global $g{}{}({}))\n'.format(i, mutability, entry.initial_expr.to_str())

        return output


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

        self.type_section = sectionList[SECTION_IDS['type']]
        if self.type_section is None:
            raise ValueError('Missing type section')

    def to_str(self):
        # The function names have to be unique, so keep
        # a frequency counter for names and append its counter to ensure uniqueness.
        function_name_table = {}
        output = ''
        for i in range(self.import_count):
            entry = self.entries[i]
            function_name = '${}.{}'.format(entry.moduleStr, entry.fieldStr)
            if entry.fieldStr in function_name_table:
                function_name_table[entry.fieldStr] += 1
                function_name += '_{}'.format(function_name_table[entry.fieldStr])
            else:
                function_name_table[entry.fieldStr] = 0
            function_str = '(type $t{})'.format(entry.kindType)
            output += '  (import "{}" "{}" (func {} {}))\n'.format(entry.moduleStr, entry.fieldStr, function_name, function_str)
        return output


class MemorySection(Section):
    def __init__(self, section, sectionList=None):
        inputBytes = section.data
        self.memoryCount = section.numTypes
        self.entries = []

        for i in range(self.memoryCount):
            self.entries.append(MemoryType(inputBytes))
            inputBytes = inputBytes[self.entries[i].size():]

    def to_str(self):
        return ''

class StartSection(Section):
    def __init__(self, section, sectionList=None):
        # The start section only contains an index variable that represents 
        # the location of the start function.
        self.index = section.numTypes

    def to_str(self):
        return '  (start {})\n'.format(self.index)

class TableSection(Section):
    def __init__(self, section, sectionList=None):
        # TODO
        pass

    def to_str(self):
        return ''

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


    def to_str(self):
        output = ''

        for i in range(self.func_count):
            func_str = self.func_types[i].to_str()
            if len(func_str) == 0:
                func_str = '(func)'
            else:
                func_str = '(func {})'.format(func_str)

            output += '  (type $t{} {})\n'.format(i, func_str)
        return output
