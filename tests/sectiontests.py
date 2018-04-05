import unittest
import os, sys
#dirname = os.path.dirname()
dirname = os.path.realpath(__file__)
dirname = dirname[:dirname[:dirname.rfind('/')].rfind('/')]
sys.path.append(dirname)
from section import *
from random import *
from constants import *

# how to write a testcase here: https://docs.python.org/3/library/unittest.html

# an example 
class TestFunctionSection(unittest.TestCase):

    def test_parse(self):
        #TODO: add test body
        self.assertEqual(1, 1)
        pass

class TestElementSection(unittest.TestCase):
    def test_one_elem_seg(self):
        section = Section()
        section.data = bytearray([0x00, 0x41, 0x00, 0x0b, 0x04, 0x00, 0x01, 0x03, 0x04])
        section.numTypes = 1
        section = ElementSection(section)
        self.assertEqual(section.toStr(),"(elem (i32.const 0) $f0 $f1 $f3 $f4)")
        self.assertEqual(section.numElemSegs, 1)
        self.assertEqual(len(section.elementSegs),1)
        self.assertEqual(section.elementSegs[0].index,0x00)
        self.assertEqual(section.elementSegs[0].offset, bytearray([0x41,0x00,0x0b]))
        self.assertEqual(section.elementSegs[0].numElems,0x04)
        self.assertEqual(section.elementSegs[0].elems,[0x00,0x01,0x03,0x04])
        self.assertEqual(len(section.elementSegs[0].elems),section.elementSegs[0].numElems)

class TestDataSection(unittest.TestCase):
    def test_data_section(self):
        section = Section()
        section.data = bytearray([0x00, 0x41, 0x00, 0x0b, 0x02, 0x68, 0x69])
        section.numTypes = 1
        section = DataSection(section)
        self.assertEqual(section.toStr(), "(memory (data \"hi\"))")
        self.assertEqual(section.numDataSegs,1)
        self.assertEqual(len(section.dataSegs),1)
        self.assertEqual(section.dataSegs[0].index,0x00)
        self.assertEqual(section.dataSegs[0].offset, bytearray([0x41,0x00,0x0b]))
        self.assertEqual(section.dataSegs[0].dataSize,0x02)
        self.assertEqual(section.dataSegs[0].data ,[0x68,0x69])
        self.assertEqual(len(section.dataSegs[0].data),section.dataSegs[0].dataSize)
        

class TestStartSection(unittest.TestCase):
    def test_start_section(self):
        section = Section()
        section.numTypes = 1
        section = StartSection(section)
        self.assertEqual(section.index, 1)

class TestTypeSection(unittest.TestCase):

    def test_one_func_type(self):
        section = Section()
        section.data = bytearray([0x60, 0x01, 0x7c, 0x01, 0x7c])
        section.numTypes = 1
        section = TypeSection(section)
        self.assertEqual(section.func_count, 1)
        self.assertEqual(len(section.func_types), 1)

        self.assertEqual(section.func_types[0].size(), 5)
        self.assertEqual(section.func_types[0].form, 'func')
        self.assertEqual(section.func_types[0].param_count, 1)
        self.assertEqual(section.func_types[0].param_types, ['f64'])
        self.assertEqual(section.func_types[0].return_count, 1)
        self.assertEqual(section.func_types[0].return_type, ['f64'])

    def test_multiple_func_type(self):
        section = Section()
        arr = []
        count = randint(1, 10)
        for i in range(count):
            arr += [0x60, 0x01, 0x7c, 0x01, 0x7c]
        section.data = bytearray(arr)
        section.numTypes = count
        section = TypeSection(section)
        self.assertEqual(section.func_count, count)
        self.assertEqual(len(section.func_types), count)

        for func_type in section.func_types:
            self.assertEqual(func_type.size(), 5)
            self.assertEqual(func_type.form, 'func')
            self.assertEqual(func_type.param_count, 1)
            self.assertEqual(func_type.param_types, ['f64'])
            self.assertEqual(func_type.return_count, 1)
            self.assertEqual(func_type.return_type, ['f64'])

    def test_random_num_params(self):
        section = Section()
        arr = [0x60]

        # Push the parameter count into the array
        param_count = randint(1, 20)
        arr += [param_count]

        # Push 'f64' types into the array
        for i in range(param_count):
            arr += [0x7c]

        # Push 1 return type of 'f64'
        arr += [0x01, 0x7c]
        section.data = bytearray(arr)
        section.numTypes = 1
        section = TypeSection(section)

        # The size of the function type is # of parameters + 4 bytes.
        # The 4 bytes are param_count, func, return_count, and return_type
        self.assertEqual(section.func_types[0].size(), 4 + param_count)
        self.assertEqual(section.func_types[0].form, 'func')
        self.assertEqual(section.func_types[0].param_count, param_count)
        for i in range(param_count):
            self.assertEqual(section.func_types[0].param_types[i], 'f64')
        self.assertEqual(section.func_types[0].return_count, 1)
        self.assertEqual(section.func_types[0].return_type, ['f64'])

class TestImportSection(unittest.TestCase):

    def test_one_import(self):
        section = Section()
        # The byte array represents the following import statement.
        # (import "host" "print" (func $host.print_1 (type $t1)))
        section.data = bytearray([0x04, 0x68, 0x6f, 0x73, 0x74, 0x05, 0x70, 0x72, 0x69, 0x6e, 0x74, 0x00, 0x01])
        section.numTypes = 1
        section = ImportSection(section)

        self.assertEqual(section.import_count, 1)
        self.assertEqual(section.entries[0].moduleStr, 'host')
        self.assertEqual(section.entries[0].fieldStr, 'print')
        self.assertEqual(section.entries[0].kind, 'function')
        self.assertEqual(section.entries[0].kindType, 1)

class TestGlobalSection(unittest.TestCase):

    def test_one_global_var(self):
        section = Section()
        section.data = bytearray([0x7f, 0x1, 0x41, 0x0, END_OPCODE])
        section.numTypes = 1
        section = GlobalSection(section)

        self.assertEqual(section.count, 1)
        self.assertEqual(section.globals[0].type.content_type, 'i32')
        self.assertEqual(section.globals[0].type.mutability, 1)
        self.assertEqual(section.globals[0].initialExpr.constant[0], 'i32.const')
        self.assertEqual(section.globals[0].initialExpr.literal, 0)

if __name__ == '__main__':
    unittest.main()
