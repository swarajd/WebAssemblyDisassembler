import numpy
from constants import *
from conversions import *

class FuncType:
    def __init__(self, inputBytes):
        """
        field         type        description
        ----------------------------------------------------------------------------------
        form          string      the value for the func type constructor as defined above
        param_count   varuint32   the number of parameters to the function
        param_types   string*     the parameter types of the function
        return_count  varuint1    the number of results from the function
        return_type   string?     the result type of the function (if return_count is 1)

        Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#func_type
        """
        self.form        = LANGUAGE_TYPES[int.from_bytes(inputBytes[0:1], byteorder='little', signed=False)]
        self.param_count = int.from_bytes(inputBytes[1:2], byteorder='little', signed=False)

        # The index in the byte array of the last value of 'param_types'
        param_end_index = 2 + self.param_count
        self.param_types = []

        for i in range(self.param_count):
            self.param_types.append(LANGUAGE_TYPES[inputBytes[2 + i]])

        self.return_count = int.from_bytes(inputBytes[param_end_index:param_end_index + 1], byteorder='little', signed=False)

        self.return_type = []
        for i in range(self.return_count):
            self.return_type.append(LANGUAGE_TYPES[inputBytes[param_end_index + 1 + i]])

    def size(self):
        """ 
        size is helper function that returns the number of bytes of this func type

        FuncType has a minimum size of 3 bytes (form, parameter count, and return count)
        The remaining bytes are dependent on the parameter and return count
        """
        return 3 + self.param_count + self.return_count

    def to_str(self, named_params=False):
        param_len = len(self.param_types)
        return_len = len(self.return_type)

        if param_len == 0 and return_len == 0:
            return ''

        if param_len == 0:
            params = ''
        elif named_params:
            params = ' '.join('(param $p{} {})'.format(i, x) for i, x in enumerate(self.param_types))
        else:
            params = '(param {})'.format(' '.join(self.param_types))

        if return_len == 0:
            results = ''
        else:
            results = '(result {})'.format(' '.join(self.return_type))

        padding = ''
        if param_len > 0 and return_len > 0:
            padding = ' '

        return '{}{}{}'.format(params, padding, results)

class TableType:
    def __init__(self, inputBytes):
        """
        Field           Type                Description
        elementType     elem_type           the type of elements
        limits          resizable_limits    see ResizableLimits class

        Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#table_type
        """

        # A varint7 indicating the types of elements in a table. 
        # In the MVP, only one type is available: anyfunc
        # https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#elem_type
        self.elementType = LANGUAGE_TYPES[inputBytes[0]]
        self.limits = ResizableLimits(inputBytes[1:])

    def size(self):
        return self.limits.size() + 1

class MemoryType:
    def __init__(self, inputBytes):
        """
        Field   Type                Description
        limits  resizable_limits    see ResizableLimits class

        Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#memory_type
        """
        self.limits = ResizableLimits(inputBytes)

    def size(self):
        return self.limits.size()

class GlobalType:
    def __init__(self, inputBytes):
        """
        Field           Type        Description
        content_type    value_type  type of the value
        mutability      varuint1    0 if immutable, 1 if mutable

        Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#global_type
        """
        self.content_type = LANGUAGE_TYPES[inputBytes[0]]
        self.mutability = inputBytes[1]

    def size(self):
        return 2

    def to_str(self):
        return 'GlobalType: {}, mutability = {}'.format(self.content_type, self.mutability)

class ResizableLimits:
    def __init__(self, inputBytes):
        """
        A packed tuple that describes the limits of a table or memory:

        Field   Type        Description
        flags   varuint1    1 if the maximum field is present, 0 otherwise
        initial varuint32   initial length (in units of table elements or Wasm pages)
        maximum varuint32?  only present if specified by flags

        Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#resizable_limits
        """
        self.flags = inputBytes[0]
        self.initial = inputBytes[1]
        if self.flags == 1:
            self.maximum = inputBytes[2]

    def size(self):
        if self.flags == 1:
            return 3
        else:
            return 2

class InitExpr:
    """
    Initializer expressions are evaluated at instantiation time and are currently used to:
        - define the initial value of global variables
        - define the offset of a data segment or elements segment

    In the MVP, to keep things simple while still supporting the basic needs of dynamic linking,
    initializer expressions are restricted to the following nullary operators:
        - the four constant operators; and
        - get_global, where the global index must refer to an immutable import.

    Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/Modules.md#initializer-expression
    """
    def __init__(self, inputBytes):
        self.constant = OPCODES[inputBytes[0]]

        index = 1

        # Iterate through the expression until the end byte is met.
        # Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#function-bodies
        while index < len(inputBytes) and inputBytes[index] != END_OPCODE:
            index += 1

        self.literal = int.from_bytes(inputBytes[1:index], byteorder='little', signed=False)
        self._size = index + 1

    def size(self):
        return self._size

    def to_str(self):
        return '{} {}'.format(self.constant[0], self.literal)

class FunctionBody:
    """
    Field       Type            Description
    ---------------------------------------------------------------------
    body_size   varuint32       size of function body to follow, in bytes
    local_count varuint32       number of local entries
    locals      local_entry*    local variables
    code        byte*           bytecode of the function
    end byte    0x0b,           indicating the end of the body
    
    Function bodies consist of a sequence of local variable declarations followed by bytecode instructions. 
    Instructions are encoded as an opcode followed by zero or more immediates as defined by the tables below. 
    Each function body must end with the end opcode.
    Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#function-bodies
    """
    def __init__(self, inputBytes, function_count):
        self.bodySize = inputBytes[0]
        self.localCount = inputBytes[1]
        self.locals = []

        # Shift the bytes by 2 for easier indexing in local variable for loop.
        inputBytes = inputBytes[2:]

        # Iterate and populate the local variables
        # Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#local-entry
        for i in range(self.localCount):
            count = inputBytes[i * 2]
            localType = LANGUAGE_TYPE[inputBytes[(i * 2) + 1]]

            # The locals array will be an array of tuples.
            # The tuple will be in the format of (count, localType).
            self.locals.append((count, localType))

        # Shift the bytes for easier indexing for remaining bytes.
        inputBytes = inputBytes[self.localCount * 2:]
        index = 0
        self.instructions = []
        while index < len(inputBytes) and inputBytes[index] != END_OPCODE:
            name, immediate = OPCODES[inputBytes[index]]
            index += 1
            if name == 'nop':
                pass
            elif immediate is None:
                self.instructions.append((name))
            elif immediate == 'local_index.varuint32':
                self.instructions.append((name, inputBytes[index]))
                index += 1
            elif immediate == 'value.varint32':
                # The literal value may contain an extra 0 byte.
                # Look at the import.wasm file as an example.
                # The start.wasm file has an example of a varint32 literal without an extra 0 byte.

                byte_string = bytes(inputBytes[index : index+2])
                decoded = leb128_to_int(byte_string, True)
                if isinstance(decoded, int):
                    self.instructions.append((name, decoded))
                    index += 2
                else:
                    self.instructions.append((name, decoded[0]))
                    index += 1

            elif immediate == 'value.uint64':
                literal = numpy.frombuffer(inputBytes[index : index + 8], dtype=numpy.float64)[0]
                self.instructions.append((name, literal))
                index += 8
            elif immediate == 'block_type':
                # Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#block-type
                value = inputBytes[index]
                if value == 0x40:
                    # -0x40 (i.e., the byte 0x40) indicating a signature with 0 results.
                    value = '0'
                elif name == 'block':
                    continue
                elif value in LANGUAGE_TYPES:
                    # a value_type indicating a signature with a single result
                    value = '(result {})'.format(LANGUAGE_TYPES[value])

                self.instructions.append((name, value, True))
                index += 1
            elif name == 'else':
                self.instructions.append((name, '', True))

            # call opcode
            elif immediate == 'function_index.varuint32':
                function_index = inputBytes[index]
                if function_index > function_count:
                    raise ValueError('Invalid function index: {}'.format(function_index))
                self.instructions.append((name, function_index))
                index += 1

            elif name == 'call_indirect':
                # The call_indirect operator takes a list of function arguments and as the last operand the index into the table.
                # Its reserved immediate is for future 🦄 use and must be 0 in the MVP.
                # type_index : varuint32, reserved : varuint1
                type_index = inputBytes[index]
                reserved = inputBytes[index + 1]

                index += 2
                self.instructions.append(('{} (type {})'.format(name, type_index),))
            elif immediate == 'memory_immediate':
                # Followed by two values, alignment and offset.
                index += 2
                self.instructions.append((name,))
            else:
                self.instructions.append((name,))

    def size(self):
        return self.bodySize + 1

    def to_str(self):
        output = ''
        indent = '  '
        in_block = False
        for instruction in self.instructions:
            if len(instruction) == 3 and instruction[2]:
                parsed_instruction = ' '.join([str(value) for value in instruction[:2]])
                in_block = True
                block_level = 2
            elif in_block:
                parsed_instruction = ' '.join([str(value) for value in instruction])
                block_level = 3
            else:
                parsed_instruction = ' '.join([str(value) for value in instruction])
                block_level = 2

            output += '{}{}\n'.format(indent * block_level, parsed_instruction)

        if in_block:
            output += '{}end\n'.format(indent * 2)

        return output