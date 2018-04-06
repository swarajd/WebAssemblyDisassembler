import unittest
import os, sys, difflib
dirname = os.path.realpath(__file__)
dirname = dirname[:dirname[:dirname.rfind('/')].rfind('/')]
sys.path.append(dirname)
from main import disassemble

differ = difflib.Differ()
files = [ 'element', 'empty', 'emptymemorydata', 'factorial', 'global', 'import', 'simple', 'start', 'stuff' ]

class TestDissassembly(unittest.TestCase):
    def test_all(self):
        for file in files: 
            wat_path = os.path.join(dirname, 'wasm_files', file, '{}.wat'.format(file))
            wasm_path = os.path.join(dirname, 'wasm_files', file, '{}.wasm'.format(file))
            wat = open(wat_path, 'r')
            input_data = wat.read().splitlines()
            output_data = disassemble(wasm_path).splitlines()
            wat.close()

            results = differ.compare(input_data, output_data)
            diff = '\n'.join(results).splitlines()

            # The assertion claims that the input and output have equal number of lines
            # and that the differ found no difference, therefore should also contain the same number of lines.
            self.assertEqual(len(diff), len(input_data))
            self.assertEqual(len(diff), len(output_data))
            self.assertEqual(len(input_data), len(output_data))

if __name__ == '__main__':
    unittest.main()