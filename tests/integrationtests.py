import unittest
import os, sys, difflib
dirname = os.path.realpath(__file__)
dirname = dirname[:dirname[:dirname.rfind('/')].rfind('/')]
sys.path.append(dirname)
import shlex, subprocess

from main import disassemble

files = [ 'element', 'empty', 'emptymemorydata', 'factorial', 'global', 'import', 'simple', 'start', 'stuff' ]

class TestDissassembly(unittest.TestCase):
    def test_all(self):
        assembledFile    = open('assembled.wasm', 'w+')
        assembledFile.close()
        assembledFile    = open('assembled.wasm', 'rb')

        for file in files: 
            print(file)

            wasm_path = os.path.join(dirname, 'wasm_files', file, '{}.wasm'.format(file))

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

            assembledFile.seek(0)
            generated_output_data = assembledFile.read()

            exp_bytes = expected_output_data
            gen_bytes = generated_output_data

            self.assertEqual(gen_bytes, exp_bytes)


        assembledFile.close()
        os.remove('assembled.wasm')
        os.remove('disassembled.wat')

if __name__ == '__main__':
    unittest.main()