class FuncType:
    def __init__(self, inputBytes):
        """
        field         type        description
        ----------------------------------------------------------------------------------
        form          varint7     the value for the func type constructor as defined above
        param_count   varuint32   the number of parameters to the function
        param_types   value_type* the parameter types of the function
        return_count  varuint1    the number of results from the function
        return_type   value_type? the result type of the function (if return_count is 1)
        """
        self.form        = int.from_bytes(inputBytes[0:1], byteorder='little', signed=False)
        self.param_count = int.from_bytes(inputBytes[1:2], byteorder='little', signed=False)

        # The index in the byte array of the last value of 'param_types'
        param_end_index = 2 + self.param_count
        self.param_types = []

        for i in range(self.param_count):
            self.param_types.append(inputBytes[2 + i]) 

        self.return_count = int.from_bytes(inputBytes[param_end_index:param_end_index + 1], byteorder='little', signed=False)

        self.return_type = None
        self.return_type = []
        for i in range(self.return_count):
            self.return_type.append(inputBytes[param_end_index + 1 + i])

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
        element_type    elem_type           the type of elements
        limits          resizable_limits    see ResizableLimits class
        """

class MemoryType:
    def __init__(self, inputBytes):
        """
        Field   Type                Description
        limits  resizable_limits    see ResizableLimits class
        """
        pass

class GlobalType:
    def __init__(self, inputBytes):
        """
        Field           Type        Description
        content_type    value_type  type of the value
        mutability      varuint1    0 if immutable, 1 if mutable
        """
        pass

class ResizableLimits:
    def __init__(self, inputBytes):
        """
        A packed tuple that describes the limits of a table or memory:

        Field   Type        Description
        flags   varuint1    1 if the maximum field is present, 0 otherwise
        initial varuint32   initial length (in units of table elements or Wasm pages)
        maximum varuint32?  only present if specified by flags
        """
        pass

"""
A single-byte unsigned integer indicating the kind of definition being 
imported/exported or defined:
"""
EXTERNAL_KIND_TABLE = {
    0 : 'function',
    1 : 'table',
    2 : 'memory',
    3 : 'global'
}