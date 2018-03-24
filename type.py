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
        self.param_types = int.from_bytes(inputBytes[2:param_end_index], byteorder='little', signed=False)
        self.return_count = int.from_bytes(inputBytes[param_end_index:param_end_index + 1], byteorder='little', signed=False)

        self.return_type = None
        if self.return_count > 0:
            return_end_index = self.return_count + param_end_index + 1
            self.return_type = int.from_bytes(inputBytes[param_end_index + 1:return_end_index], byteorder='little', signed=False)


    def size(self):
        """ 
        size is helper function that returns the number of bytes of this func type

        FuncType has a minimum size of 3 bytes (form, parameter count, and return count)
        The remaining bytes are dependent on the parameter and return count
        """

        self.size = 3 + self.param_count + self.return_count

    def to_str(self):
        return 'form: {}, param count: {}, params: {}, return count: {}, returns: {}'.format(self.form, self.param_count, self.param_types, self.return_count, self.return_type)
