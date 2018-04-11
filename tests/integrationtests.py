import unittest
import os, sys, difflib
dirname = os.path.realpath(__file__)
dirname = dirname[:dirname[:dirname.rfind('/')].rfind('/')]
sys.path.append(dirname)
import shlex, subprocess

from main import disassemble

class TestDissassembly(unittest.TestCase):
    def setUp(self):
        self.assembledFile    = open('assembled.wasm', 'w+')
        self.assembledFile.close()
        self.assembledFile    = open('assembled.wasm', 'rb')

    def tearDown(self):
        try:
            self.assembledFile.close()
            os.remove('assembled.wasm')
            os.remove('disassembled.wat')
        except FileNotFoundError:
            pass

    def test_all(self):
        test_dir = './wasm_files'
        for file in os.listdir(test_dir):
            file_path = os.path.join(test_dir, file)
            if not os.path.isdir(file_path):
                continue
            wasm_path = os.path.join(file_path, '{}.wasm'.format(file))
            self.assert_disassemble(wasm_path)

    def test_spec(self):
        test_dir = './spec/wasm'
        for file in os.listdir(test_dir):
            if not file.endswith('.wasm'):
                continue
            wasm_path = os.path.join(test_dir, file)
            print(file)
            self.assert_disassemble(wasm_path)

    def assert_disassemble(self, wasm_path):
        wasm = open(wasm_path, 'rb')
        expected_output_data  = wasm.read()
        wasm.close()

        disassembly = disassemble(wasm_path)
        disassembledFile = open('disassembled.wat', 'w')
        disassembledFile.write(disassembly)
        disassembledFile.close()

        args = shlex.split("wat2wasm -o assembled.wasm disassembled.wat ")
        process = subprocess.Popen(args, stdout=subprocess.PIPE)

        process_status = process.wait()
        (output, err) = process.communicate()

        self.assembledFile.seek(0)
        generated_output_data = self.assembledFile.read()

        exp_bytes = expected_output_data
        gen_bytes = generated_output_data

        self.assertEqual(gen_bytes, exp_bytes)

if __name__ == '__main__':
    unittest.main()