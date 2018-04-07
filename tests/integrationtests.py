import unittest
import os, sys, difflib
dirname = os.path.realpath(__file__)
dirname = dirname[:dirname[:dirname.rfind('/')].rfind('/')]
sys.path.append(dirname)
import shlex, subprocess

from main import disassemble

differ = difflib.Differ()
#files = [ 'element', 'empty', 'emptymemorydata', 'factorial', 'global', 'import', 'simple', 'start', 'stuff' ]
files = [ 'empty', 'emptymemorydata', 'factorial', 'global', 'import', 'simple', 'start', 'stuff' ]

class TestDissassembly(unittest.TestCase):
    def test_all(self):
        assembledFile    = open('assembled.wasm', 'w+')
        assembledFile.close()
        assembledFile    = open('assembled.wasm', 'rb')

        for file in files: 

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
            # print(output, err)
            

            assembledFile.seek(0)
            generated_output_data = assembledFile.read()

            results = differ.compare(expected_output_data, generated_output_data)

            exp_bytes = expected_output_data
            gen_bytes = generated_output_data

            print("expected", exp_bytes)
            print("generated", gen_bytes)

            # diff = '\n'.join(results).splitlines()

            # The assertion claims that the input and output have equal number of lines
            # and that the differ found no difference, therefore should also contain the same number of lines.
            # self.assertEqual(len(diff), len(expected_output_data))
            # self.assertEqual(len(diff), len(generated_output_data))
            # self.assertEqual(len(expected_output_data), len(generated_output_data))

        assembledFile.close()
        os.remove('assembled.wasm')
        os.remove('disassembled.wat')



if __name__ == '__main__':
    unittest.main()