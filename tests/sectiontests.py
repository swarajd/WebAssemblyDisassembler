import unittest
import os, sys
sys.path.append(os.environ['CS4984_PROJECT_PATH'])
from section import *
from random import *

# how to write a testcase here: https://docs.python.org/3/library/unittest.html

# an example 
class TestFunctionSection(unittest.TestCase):

    def test_parse(self):
        #TODO: add test body
        self.assertEqual(1, 1)
        pass

class TestTypeSection(unittest.TestCase):

    def test_one_func_type(self):
        section = Section()
        section.data = bytearray([0x60, 0x01, 0x7c, 0x01, 0x7c])
        section.numTypes = 1
        section = TypeSection(section)
        self.assertEqual(section.func_count, 1)
        self.assertEqual(len(section.func_types), 1)

        self.assertEqual(section.func_types[0].size(), 5)
        self.assertEqual(section.func_types[0].form, 96)
        self.assertEqual(section.func_types[0].param_count, 1)
        self.assertEqual(section.func_types[0].param_types, [124])
        self.assertEqual(section.func_types[0].return_count, 1)
        self.assertEqual(section.func_types[0].return_type, [124])

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
            self.assertEqual(func_type.form, 96)
            self.assertEqual(func_type.param_count, 1)
            self.assertEqual(func_type.param_types, [124])
            self.assertEqual(func_type.return_count, 1)
            self.assertEqual(func_type.return_type, [124])

if __name__ == '__main__':
    unittest.main()