from constants import *

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

    def to_str(self):
        return 'FuncType: (size: {}, form: {}, param count: {}, params: {}, return count: {}, returns: {})'.format(str(self.size()), self.form, self.param_count, self.param_types, self.return_count, self.return_type)

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
        self.elementType = inputBytes[0]
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
        self.initial = None
        if self.flags == 1:
            self.initial = inputBytes[2]

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
        self.constant = CONSTANTS[inputBytes[0]]

        index = 1

        # Iterate through the expression until the end byte is met.
        # Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#function-bodies
        while index < len(inputBytes) and inputBytes[index] != 0x0b:
            index += 1

        self.literal = int.from_bytes(inputBytes[1:index], byteorder='little', signed=False)
        self._size = index + 1

    def size(self):
        return self._size

    def to_str(self):
        return 'constant: {}, literal: {}'.format(self.constant, self.literal)