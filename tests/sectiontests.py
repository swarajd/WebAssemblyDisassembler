import unittest

# how to write a testcase here: https://docs.python.org/3/library/unittest.html

# an example 
class TestFunctionSection(unittest.TestCase):

    def test_parse(self):
        #TODO: add test body
        self.assertEqual(1, 1)
        pass



if __name__ == '__main__':
    unittest.main()