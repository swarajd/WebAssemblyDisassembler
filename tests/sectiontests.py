import unittest
import os, sys
sys.path.append(os.environ['CS4984_PROJECT_PATH'])
from section import *

# how to write a testcase here: https://docs.python.org/3/library/unittest.html

# an example 
class TestFunctionSection(unittest.TestCase):

    def test_parse(self):
        #TODO: add test body
        self.assertEqual(1, 1)
        pass



if __name__ == '__main__':
    unittest.main()